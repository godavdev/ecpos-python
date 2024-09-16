"""PLUGIN TICKET"""
import sys
import base64
from io import BytesIO
from multiprocessing import freeze_support
from escpos.printer import Win32Raw
from escpos.capabilities import get_profile
from PIL import Image
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from pydantic import BaseModel

sys.stdout = open('logs.txt', 'w', encoding='utf-8')

class DataImage(BaseModel):
    """IMAGE CLASS"""

    base: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    """HELLO ROUTE"""
    return "ichiban.team"


@app.post("/")
def print_ticket_data(data_image: DataImage):
    """PRINT TICKET ROUTE"""
    if data_image.base.startswith("data:image/png;base64,"):
        data_image.base = data_image.base.replace("data:image/png;base64,", "")
    image_data = base64.b64decode(data_image.base)
    image = Image.open(BytesIO(image_data))
    width, height = image.size
    aspect = width / height
    resized_image = image.resize((576, int(576 / aspect)))
    tp = Win32Raw()
    tp.profile = get_profile("RP-F10-80mm")
    tp.open()
    tp.image(img_source=resized_image)
    tp.cut()
    tp.close()
    return {}


if __name__ == "__main__":
    freeze_support()
    run(app, port=4321, reload=False, workers=1)
