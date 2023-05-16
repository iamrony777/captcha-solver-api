import asyncio
import os
import time
from io import BytesIO

import uvicorn
import uvloop
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import imghdr
from src.rucaptcha.prediction import captcha_detection

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


@app.post("/solve")
async def captcha_solver(background_task: BackgroundTasks, file: UploadFile = File(...)):
    """Captcha Solver Endpoint"""
    file_name = save_file(await file.read())
    captcha = captcha_detection(file_name)

    return {"solved": captcha}


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
