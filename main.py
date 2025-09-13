#!/usr/bin/env python

# downloader
#
# Test with:
# curl -X POST http://localhost:8000/download -H "Content-Type: application/json" -d '{"url":"https://www.youtube.com/watch?v=h6rkauDhDUM"}'

import subprocess
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# -------- Config --------
DOWNLOAD_DIR = Path("/mnt/DVR/youtube")

# -------- API Models --------
class DownloadRequest(BaseModel):
    url: str

# -------- FastAPI App --------
app = FastAPI()

@app.post("/download")
async def download_video(request: DownloadRequest):
    url = request.url
    try:
        # Run yt-dlp as a subprocess
        cmd = [
            "yt-dlp",
            "-4",
            "--min-sleep-interval", "5",
            "--max-sleep-interval", "10",
            "--write-subs",
            "--write-auto-subs",
            "--sub-lang", "en.*",
            "--format", "bv*+ba",
            "--paths", str(DOWNLOAD_DIR),
            url
        ]
        print(cmd)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"yt-dlp failed: {e}")
    return {"status": "success", "url": url}

# -------- Entrypoint --------
if __name__ == "__main__":
    # Run as a daemon with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
