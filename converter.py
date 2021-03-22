from PIL import Image
import pyheif
import sys
import os
from datetime import datetime


def convert_to_jpeg(user, my_dir):
    way = my_dir
    extension = os.path.splitext(my_dir)[-1].lower()
    if extension == ".heic":
        heif_file = pyheif.read(way)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        os.remove(way)
        image.save("data/"+user + "_"+str(datetime.now())+'.jpg', "JPEG")
        return "Готово"
    else:
        try:
            im = Image.open(way)
            rgb_im = im.convert('RGB')
            rgb_im.save("data/"+user + "_"+str(datetime.now())+'.jpg')
            os.remove(way)
            return "Готово"
        except:
            return "Ты точно отправил фото?"
