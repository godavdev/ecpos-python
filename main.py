"""WADAWD"""

from multiprocessing import freeze_support
from escpos.printer import Win32Raw
from escpos.capabilities import get_profile
from PIL import Image
from fastapi import FastAPI
from uvicorn import run
from pydantic import BaseModel


class Body(BaseModel):
    data: str


app = FastAPI()


@app.get("/")
def hello():
    """HELLO ROUTE"""
    return "ichiban.team"


@app.post("/")
def print_ticket_data(body: Body):
    """PRINT TICKET ROUTE"""
    image = Image.open(body.data)
    width, height = image.size
    aspect = width / height
    new = image.resize((576, int(576 / aspect)))
    tp = Win32Raw()
    tp.profile = get_profile("RP-F10-80mm")
    tp.open()
    tp.image(img_source=new)
    tp.cut()
    tp.close()
    return "ichiban.team"


if __name__ == "__main__":
    freeze_support()
    run(app, port=4321, reload=False, workers=1)
