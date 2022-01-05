from PIL import Image, ImageDraw, ImageFont
import os
import json
import zipfile
import io
from hashlib import md5

def render(dir : str, path : str, chars : str):
    """if not os.path.exists(dir):
        os.mkdir(dir)"""
    if not os.path.exists(path):
        raise FileNotFoundError("File \"" + path + "\"")
    font = ImageFont.truetype(path, size=28)
    letters = dict()
    for i in chars:
        image = Image.new(mode="RGBA", size=(50, 50), color=None)
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
    return letters

def inject(sb3, ttf, chars):
    if not os.path.exists("temp"):
        os.mkdir("temp")
    zipfile.ZipFile(sb3).extractall("temp")
    pjson = json.load(open("temp/project.json", 'r'))
    newsprite = {"isStage":False,"name":"/","variables":{},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[],"sounds":[],"volume":100,"layerOrder":0,"tempo":60,"videoTransparency":50,"videoState":"on","textToSpeechLanguage":None}
    costumes = []
    pngdata = render(None, ttf, chars)
    for i in pngdata:
        md5id = md5(pngdata[i]).hexdigest()
        costumes.append({"assetId":md5id,"name":"","bitmapResolution":1,"md5ext":md5id+".png","dataFormat":"png","rotationCenterX":0,"rotationCenterY":0})
        file = open("temp/" + md5id + ".png", 'w')
        file = open("temp/" + md5id + ".png", 'wb')
        file.write(pngdata[i])
    newsprite["costumes"] = costumes
    pjson["targets"].append(newsprite)

    zip = zipfile.ZipFile("output.sb3", 'w')
    for root, directories, files in os.walk("temp"):
        for filename in files:
            filepath = os.path.join(root, filename)
            zip.write(filepath)
    
    

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+`1234567890-={}[];':\"'1234567890"
    
#render("OpenSans", "OpenSans.ttf", chars)
#print("Font is rendered!")
inject("project_input.sb3", "OpenSans.ttf", chars)
print("Injected font!")