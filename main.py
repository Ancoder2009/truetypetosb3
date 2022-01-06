from PIL import Image, ImageDraw, ImageFont
import os
import json
import zipfile
import io
import time
import sys
import random
from hashlib import md5

current_width_dump = []

def render(dir : str, path : str, chars : str):
    """if not os.path.exists(dir):
        os.mkdir(dir)"""
    width_dump = ""
    if not os.path.exists(path):
        raise FileNotFoundError("File \"" + path + "\"")
    font = ImageFont.truetype(path, size=28)
    letters = dict()
    progress = 0
    for i in chars:
        sys.stdout.write("\r" + "Copying letter " + i)
        progress += 1
        image = Image.new(mode="RGBA", size=(50, 50), color=None)
        width_dump += str(font.getsize(i)[0]) + "\n"
        draw = ImageDraw.Draw(image)
        draw.text((12.5, 12.5), i, fill="black", font=font)
        #names = {"/": "fw_slash", "\\": "bw_slash", ":": "colon", "*": "astrick", "?": "qmark", "\"": "quotation", "<": "ar", ">": "al", "|": "straight"}
        #if i in "/\:*?\"<>|":
            #image.save(dir + "/" + names[i] + ".png", format="png")
        #else:
            #image.save(dir + "/" + i + ".png", format="png")
        buffer = io.BytesIO()
        image.save(buffer, format="png")
        letters[i] = buffer.getvalue()
    open("width_dump.txt", 'w').write(width_dump)
    global current_width_dump
    current_width_dump = width_dump.split("\n")
    return letters

def createSprite(ttf, chars, return_bytes):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    newsprite = {"isStage":False,"name":ttf.split('.')[0],"variables":{},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[],"sounds":[],"volume":100,"layerOrder":1,"visible":True,"x":0,"y":0,"size":100,"direction":90,"draggable":False,"rotationStyle":"all around"}
    costumes = []
    pngdata = render(None, ttf, chars)
    newsprite["lists"][chars[random.randint(1, len(chars) - 1)]] = ["width_dump", current_width_dump]
    for i in pngdata:
        md5id = md5(pngdata[i]).hexdigest()
        costumes.append({"assetId":md5id,"name":i,"bitmapResolution":2,"md5ext":md5id + ".png","dataFormat":"png","rotationCenterX":25,"rotationCenterY":25})
        file = open("temp/" + md5id + ".png", 'w')
        file = open("temp/" + md5id + ".png", 'wb')
        file.write(pngdata[i])
        newsprite["costumes"] = costumes
    open("temp/sprite.json", 'w').write(json.dumps(newsprite))
    zip = zipfile.ZipFile(ttf.split(".")[0] + ".sprite3", 'w')
    data = None
    if return_bytes:
        data = io.BytesIO()
        zip = zipfile.ZipFile(data, 'w')
    for file in os.listdir("temp"):
        filepath = os.path.join(file)
        sys.stdout.write("\r" + "Creating Asset: temp/" + filepath)
        zip.write("temp/" + filepath)

    for file in os.listdir("temp"):
        filepath = os.path.join(file)
        sys.stdout.write("\r" + "Cleaning Up: temp/" + filepath)
        os.remove("temp/" + filepath)
    os.removedirs("temp")
    print("\n")
    if return_bytes:
        return data
    
def inject(sb3, ttf, chars, return_bytes):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    zipfile.ZipFile(sb3).extractall("temp")
    pjson = json.load(open("temp/project.json", 'r'))
    newsprite = {"isStage":False,"name":ttf.split('.')[0],"variables":{},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[],"sounds":[],"volume":100,"layerOrder":1,"visible":True,"x":0,"y":0,"size":100,"direction":90,"draggable":False,"rotationStyle":"all around"}
    costumes = []
    pngdata = render(None, ttf, chars)
    newsprite["lists"][chars[random.randint(1, len(chars) - 1)]] = ["width_dump", current_width_dump]
    for i in pngdata:
        md5id = md5(pngdata[i]).hexdigest()
        costumes.append({"assetId":md5id,"name":i,"bitmapResolution":2,"md5ext":md5id + ".png","dataFormat":"png","rotationCenterX":25,"rotationCenterY":25})
        file = open("temp/" + md5id + ".png", 'w')
        file = open("temp/" + md5id + ".png", 'wb')
        file.write(pngdata[i])
    newsprite["costumes"] = costumes
    pjson["targets"].append(newsprite)
    open("temp/project.json", 'w').write(json.dumps(pjson))
    zip = zipfile.ZipFile(ttf.split(".")[0] + ".sb3", 'w')
    data = None
    if return_bytes:
        data = io.BytesIO()
        zip = zipfile.ZipFile(data, 'w')
    for file in os.listdir("temp"):
        filepath = os.path.join(file)
        sys.stdout.write("\r" + "Injecting: temp/" + filepath)
        zip.write("temp/" + filepath)

    for file in os.listdir("temp"):
        filepath = os.path.join(file)
        sys.stdout.write("\r" + "Cleaning Up: temp/" + filepath)
        os.remove("temp/" + filepath)
    os.removedirs("temp")
    print("\n")
    if return_bytes:
        return data

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+`1234567890-={}[];':\"., "
    
#render("OpenSans", "OpenSans.ttf", chars)
#print("Font is rendered!")
#inject("project_input.sb3", "Karla-Bold.ttf", chars)
#bts = createSprite("SFpro.OTF", chars, True)
#print(bts.getvalue())
#print("Injected font!")