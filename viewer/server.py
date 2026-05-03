from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
import os
import asyncio
import signal
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from contextlib import asynccontextmanager
from typing import Set

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# Global state for watcher
watch_queues: Set[asyncio.Queue] = set()
is_shutting_down = False


def notify_all_queues():
    global is_shutting_down
    is_shutting_down = True
    for q in list(watch_queues):
        q.put_nowait(None)


class GlobalHandler(FileSystemEventHandler):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py"):
            path = event.src_path

            def notify():
                for q in watch_queues:
                    q.put_nowait(path)

            self.loop.call_soon_threadsafe(notify)


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()

    original_sigint = signal.getsignal(signal.SIGINT)
    original_sigterm = signal.getsignal(signal.SIGTERM)

    def patched_sigint(sig, frame):
        notify_all_queues()
        if callable(original_sigint):
            original_sigint(sig, frame)

    def patched_sigterm(sig, frame):
        notify_all_queues()
        if callable(original_sigterm):
            original_sigterm(sig, frame)

    signal.signal(signal.SIGINT, patched_sigint)
    signal.signal(signal.SIGTERM, patched_sigterm)

    observer = Observer()
    observer.daemon = True
    handler = GlobalHandler(loop)
    observer.schedule(handler, SRC_DIR, recursive=True)
    observer.start()
    try:
        yield
    finally:
        notify_all_queues()
        observer.stop()
        observer.join()


app = FastAPI(debug=True, lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def get_viewer():
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r") as f:
        return f.read()


@app.get("/list-files")
async def list_files():
    src_path = Path(SRC_DIR)
    cad_path = src_path / "cad"

    files = []

    for p in src_path.glob("*.py"):
        if p.is_file():
            files.append(str(p.absolute()))

    if cad_path.exists():
        for p in cad_path.rglob("*.py"):
            if p.is_file() and "__pycache__" not in str(p):
                files.append(str(p.absolute()))

    return sorted(list(set(files)))


@app.get("/build-stl")
async def build_stl(file_path: str, force: bool = False):
    if not file_path.startswith(SRC_DIR):
        raise HTTPException(status_code=400, detail="Invalid file path")

    rel_path = os.path.relpath(file_path, SRC_DIR)
    if rel_path.startswith(".."):
        raise HTTPException(status_code=400, detail="Invalid file path")

    target_name = os.path.splitext(rel_path)[0] + ".stl"
    build_rel_path = os.path.join("build", target_name)

    cmd = ["make", "-j", str(os.cpu_count() or 1)]
    if force:
        cmd.append("-B")
    cmd.append(build_rel_path)

    async def generate():
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=PROJECT_ROOT,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            yield line.decode()

        await process.wait()
        if process.returncode != 0:
            yield f"\nERROR: Build failed with return code {process.returncode}\n"
        else:
            yield "\nSUCCESS: Build completed.\n"

    return StreamingResponse(generate(), media_type="text/plain")


@app.get("/watch")
async def watch_changes(request: Request):
    queue = asyncio.Queue()
    watch_queues.add(queue)
    try:
        while not is_shutting_down:
            if await request.is_disconnected():
                break
            try:
                # Use a timeout to allow checking for disconnect or shutdown
                changed_file = await asyncio.wait_for(queue.get(), timeout=1.0)
                if changed_file is None:
                    return {"file": None, "shutdown": True}
                return {"file": changed_file}
            except asyncio.TimeoutError:
                continue
    finally:
        if queue in watch_queues:
            watch_queues.remove(queue)
    return {"file": None, "shutdown": is_shutting_down}


@app.get("/get-stl")
async def get_stl(file_path: str):
    if not file_path.startswith(SRC_DIR):
        raise HTTPException(status_code=400, detail="Invalid file path")

    rel_path = os.path.relpath(file_path, SRC_DIR)
    if rel_path.startswith(".."):
        raise HTTPException(status_code=400, detail="Invalid file path")

    target_name = os.path.splitext(rel_path)[0] + ".stl"
    build_rel_path = os.path.join("build", target_name)
    build_abs_path = os.path.join(PROJECT_ROOT, build_rel_path)

    if not os.path.exists(build_abs_path):
        raise HTTPException(
            status_code=404,
            detail=f"STL file not found at {build_rel_path}. Please build it first.",
        )

    return FileResponse(
        path=build_abs_path,
        media_type="application/sla",
        filename=os.path.basename(build_abs_path),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=6333,
        reload=True,
        reload_dirs=[BASE_DIR],
        log_level="debug",
        app_dir=BASE_DIR,
    )
