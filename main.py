import asyncio
import os
import time
from io import BytesIO

import uvicorn
import uvloop
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from src.timeout import Timeout

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI(docs_url="/docs", redoc_url=None, title='Captcha Solver API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_file(data: bytes) -> str:
    """put bytes content into a png file"""
    suffix = round(time.time())
    img = Image.open(BytesIO(data))
    img.save(f"captcha_{suffix}.png", "png", optimize=True)
    return f"captcha_{suffix}.png"


@app.post("/javdb")
async def javdb_solver(background_task: BackgroundTasks, file: UploadFile = File(...)):
    """Captcha Solver Endpoint - javdb.com"""
    # Importing here beacause after importing memory increases by 900mb to 1gb+
    # So only importing during api call
    from src.javdb.object_detection import captcha_detection
    file_name = save_file(await file.read())
    timeout = Timeout(file_name, int(os.getenv('RELOAD_DELAY', '20')))
    background_task.add_task(timeout.run)
    captcha = captcha_detection(file_name)

    return {"solved": captcha}


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ["PORT"]),
        reload=True,
        reload_dirs=["."],
        reload_excludes=["*.*"],
        reload_includes=["timeout"], # Cause reload_delay fucking doesn;t work
    )
