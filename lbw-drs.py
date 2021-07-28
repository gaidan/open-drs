from PIL import Image, ImageFilter
from datetime import datetime
from sys import argv
import colorsys
import math
import pygame

folder = argv[5]
speed = argv[6]

def HSVColor(img):
    if isinstance(img,Image.Image):
        r,g,b = img.split()
        Hdat = []
        Sdat = []
        Vdat = []
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        return Image.merge('RGB',(r,g,b))
    else:
        return None

def inRange(imgdata, lower, upper):
    newdata = []
    for pixel in imgdata:
        inrange = True
        counter = 0
        for value in pixel:
            if value > lower[counter] and value < upper[counter]:
                pass
            else:
                inrange = False
                break
            counter += 1
        if inrange:
            newdata.append((255, 255, 255))
        else:
            newdata.append((0, 0, 0))
    return newdata

def getCentreM(imgdata, size):
    w = size[0]
    h = size[1]
    data = []
    for i in range(0, len(imgdata)):
        if imgdata[i] == (255, 255, 255):
            data.append(i)
    try:
        c = data[round(len(data)/2)]
        cc = [c%w, math.floor(c/w)]
    except:
        cc = [w, h]
    return cc

def getCentre(imgdata, size):
    w = size[0]
    h = size[1]
    cc = [0, 0]
    c = 0
    for i in range(0, len(imgdata)):
        if imgdata[i] == (255, 255, 255):
            x = i%w
            y = math.floor(i/w)
            cc[0] += x
            cc[1] += y
            c += 1
    try:
        cc[0] = round(cc[0]/c)
        cc[1] = round(cc[1]/c)
    except:
        cc[0] = int(argv[2])
        cc[1] = int(argv[3])
    return cc

def dis(x0, y0, x1, y1):
    dis = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    return dis

def cleanData(imgdata, size):
    ndata = []
    for i in range(0, len(imgdata)):
        if imgdata[i] == (255, 255, 255):
            ndata.append(i)
    w = size[0]
    h = size[1]
    medianpos = []
    a = (len(imgdata))
    nndata = []
    try:
        medianpos.append(ndata[round(len(ndata)/2)]%w)
        medianpos.append(math.floor(ndata[round(len(ndata)/2)]/w))
        for i in range(0, len(ndata)):
            if dis(medianpos[0], medianpos[1], ndata[i]%w, math.floor(ndata[i]/w)) > 20:
                pass
            else:
                nndata.append(ndata[i])
    except:
        pass
    ndata = nndata
    for i in range(0, a):
        if i in ndata:
            imgdata[i] = (255, 255, 255)
        else:
            imgdata[i] = (0, 0, 0)
    return imgdata

def trackBall(imgname, option):
    image = Image.open(imgname).convert('RGB')
    image = image.filter(ImageFilter.GaussianBlur())
    if option == 'p':
        image = HSVColor(image)
        imgdata = image.getdata()
        imgdata = inRange(imgdata, (80, 132, 159), (255, 255, 255))
        if speed == 's':
            imgdata = cleanData(imgdata, image.size)
    if option == 'r':
        image = HSVColor(image)
        imgdata = image.getdata()
        imgdata = inRange(imgdata, (33, 145, 63), (43, 155, 85))
        if speed == 's':
            imgdata = cleanData(imgdata, image.size)
    if option == 'i':
        image = HSVColor(image)
        imgdata = image.getdata()
        imgdata = inRange(imgdata, (0, 120, 120), (255, 255, 255))
        if speed == 's':
            imgdata = cleanData(imgdata, image.size)
    if speed == 'f':
        centre = getCentreM(imgdata, image.size)
    else:
        centre = getCentre(imgdata, image.size)
    return centre

amount = int(argv[1])
centres = []
for i in range(1, amount+1):
    fn = "frames/%s/out-{}.jpg" % folder
    if i < 10:
        fn = fn.format("00{}".format(i))
    if i >= 10 and i < 100:
        fn = fn.format("0{}".format(i))
    else:
        fn = fn.format("{}".format(i))
    centre = trackBall(fn, argv[4])
    centres.append(centre)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("[{}] Finished calculating for {}".format(current_time, fn))

w, h = int(argv[2]), int(argv[3])

pygame.init()
screen = pygame.display.set_mode((w, h))

bgImgs = [] 
for i in range(1, amount+1):
    fn = "frames/%s/out-{}.jpg" % folder
    if i < 10:
        fn = fn.format("00{}".format(i))
    if i >= 10 and i < 100:
        fn = fn.format("0{}".format(i))
    else:
        fn = fn.format("{}".format(i))
    bgImgs.append(pygame.image.load(fn))

running = True
i = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if i-1 >= 0:
                    i -= 1
            if event.key == pygame.K_RIGHT:
                if i+1 < amount:
                    i += 1
    screen.fill((255, 255, 255))
    screen.blit(bgImgs[i], (0, 0))
    pygame.draw.circle(screen, (0, 0, 0), centres[i], 5)
    pygame.display.flip()

pygame.quit()
