import math
import os

from PIL import Image, ImageDraw


def ToSRGB(c):
    if c <= 0.0031308:
        return c * 12.92
    return 1.055 * math.pow(c, 1 / 2.4) - 0.055


def covert(path, outPath):
    img_src = Image.open(path)
    w, h = img_src.size
    img_dis = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img_dis)
    r, g, b, a = img_src.getpixel((1, 1))
    for x in range(w):
        for y in range(h):
            r, g, b, a = img_src.getpixel((x, y))
            r = r / 255.0
            g = g / 255.0
            b = b / 255.0
            sr = ToSRGB(r)
            sg = ToSRGB(g)
            sb = ToSRGB(b)
            sr = round(sr * 255.0)
            sg = round(sg * 255.0)
            sb = round(sb * 255.0)
            draw.point((x, y), fill=(sr, sg, sb, a))
    img_dis.save(outPath, 'TGA')


if __name__ == '__main__':
    root = 'D:\\PC\\Desktop\\ff\\FFDFD\\XX'
    for root, dirs, files in os.walk(root, topdown=False):
        for f in files:
            if f.endswith('.tga'):
                name = f.split('.')[0]
                outPath = root + "\\" + name + "_Gamma.tga"
                srcPath = root + "\\" + f
                covert(srcPath, outPath)
