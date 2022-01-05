from PIL import Image, ImageDraw, ImageFont
import os

def render(dir : str, path : str, chars : str):
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(path):
        raise FileNotFoundError("File \"" + path + "\"")
    font = ImageFont.truetype(path, size=28)
    for i in chars:
        image = Image.new(mode="RGBA", size=(50, 50), color=None)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), i, fill="black", font=font)
        names = {"/": "fw_slash", "\\": "bw_slash", ":": "colon", "*": "astrick", "?": "qmark", "\"": "quotation", "<": "ar", ">": "al", "|": "straight"}
        if i in "/\:*?\"<>|":
            image.save(dir + "/" + names[i] + ".png", format="png")
        else:
            image.save(dir + "/" + i + ".png", format="png")

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+`1234567890-={}[];':\"'1234567890"
    
render("OpenSans", "OpenSans.ttf", chars)