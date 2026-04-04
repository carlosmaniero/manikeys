from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import os
from pathlib import Path

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
        log_level="debug",
        app_dir=BASE_DIR,
    )
