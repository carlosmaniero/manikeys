from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
import os
import asyncio
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = FastAPI(debug=True)

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")


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
        for p in cad_path.glob("*.py"):
            if p.is_file():
                files.append(str(p.absolute()))

    return sorted(files)


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
            stderr=asyncio.subprocess.STDOUT
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
async def watch_changes():
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    class Handler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory and event.src_path.endswith(".py"):
                loop.call_soon_threadsafe(queue.put_nowait, event.src_path)

    handler = Handler()
    observer = Observer()
    observer.schedule(handler, SRC_DIR, recursive=True)
    observer.start()

    try:
        changed_file = await queue.get()
        return {"file": changed_file}
    finally:
        observer.stop()
        observer.join()


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
        raise HTTPException(status_code=404, detail=f"STL file not found at {build_rel_path}. Please build it first.")

    return FileResponse(
        path=build_abs_path,
        media_type="application/sla",
        filename=os.path.basename(build_abs_path)
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
