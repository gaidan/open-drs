import cv2
import math
import pygame
import numpy as np
from PIL import Image
from sys import argv
import datetime

frames = int(argv[1])
folder = argv[2]
mode = argv[3]

def getName(i, folder):
    output = "frames/%s/out-{}.jpg" % folder
    if (i < 10):
        output = output.format("00%d" % i)
    if (i >= 10 and i < 100):
        output = output.format("0%d" % i)
    if (i >= 100):
        output = output.format("%d" % i)
    print(output)
    return output

def distance(x0, y0, x1, y1):
    dis = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    return dis

def cleanData(imgdata, size):
    ndata = []
    for i in range(0, len(imgdata)):
        if imgdata[i] != (0, 0, 0):
            ndata.append(i)
    w = size[0]
    h = size[1]
    medianpos = []
    a = (len(imgdata))
    nndata = []
    try:
        medianpos.append(ndata[int(round(len(ndata)/2))]%w)
        medianpos.append(math.floor(ndata[int(round(len(ndata)/2))]/w))
        for i in range(0, len(ndata)):
            if distance(medianpos[0], medianpos[1], ndata[i]%w, math.floor(ndata[i]/w)) > 30:
                pass
            else:
                nndata.append(ndata[i])
    except Exception as e:
        print(e)
    ndata = nndata
    nnndata = []
    for i in range(0, a):
        if i in ndata:
            nnndata.append(imgdata[i])
        else:
            nnndata.append((0, 0, 0))
    return nnndata

sz = [int(argv[4].split("x")[0]),int(argv[4].split("x")[1])]

def track(imgname, (a, b, c), (d, e, f), cutoff):
    image = cv2.imread(imgname)
    lower = np.array([a, b, c])
    upper = np.array([d, e, f])
    image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(image,image, mask= mask)
    cv2.imwrite("temp.jpg", output)
    image = Image.open("temp.jpg").convert('RGB')
    imgdata = image.getdata()
    w, h = image.size
    avgx, avgy = 0, 0
    count = 0
    # imgdata = cleanData(imgdata, image.size)
    ndata = []
    for i in range(0, len(imgdata)-1):
        if imgdata[i] != (0, 0, 0):
            ndata.append(i)
            count += 1
    nndata = []
    # print(count)
    try:
        middlex = int(ndata[int(round(len(ndata)/2))]%w)
        middley = int(math.floor(ndata[int(round(len(ndata)/2))]/w))
    except:
        middlex = 0
        middley = 0
    for i in range(0, len(ndata)):
        x = int(ndata[i]%w)
        y = int(round(math.floor(ndata[i])/w))
        dis = distance(middlex, middley, x, y)
        if distance(middlex, middley, x, y) > 50:
            pass
        else:
            nndata.append(ndata[i])
    try:
        count = 0
        avgx = 0
        avgy = 0
        for i in range(0, len(nndata)):
            x = int(nndata[i]%w)
            y = int(round(math.floor(nndata[i])/w))
            avgx += x
            avgy += y
            count += 1
        avgx = avgx / count
        avgy = avgy / count
        # avgx = int(nndata[int(round(len(nndata)/2))]%w)
        # avgy = int(math.floor(nndata[int(round(len(nndata)/2))]/w))
    except Exception as e:
        avgx = 0
        avgy = 0
    if count < cutoff:
        avgx = 0
        avgy = 0
        count = 0
    return avgx, avgy

centres = []
bgImgs = []

for i in range(1, frames+1):
    fn = getName(i, folder)
    ax, ay = 0, 0
    #try:
    if mode == 'r':
        ax, ay = track(fn, (155, 150, 74), (179, 255, 255), int(argv[5]))
    if mode == 'p':
        ax, ay = track(fn, (80, 132, 159), (255, 255, 255), int(argv[5]))
    #except Exception as e:
    #    print(e)
    #    ax = 0
    #    ay = 0
    bgImgs.append(pygame.image.load(fn))
    centres.append((int(round(ax)), int(round(ay))))
    print ("[{}] Finished calculating {}".format(datetime.datetime.now().strftime("%H:%M:%S"), fn))

pygame.init()
screen = pygame.display.set_mode(sz)

running = True
i = 0

playcount = 0
playing = 0

while running:
    if playing:
        if playcount % 5 == 0:
            playcount = 0
            if i+1 < frames:
                i+=1
            else:
                playing = 0
        playcount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if i-1 >= 0:
                    i -= 1
            if event.key == pygame.K_RIGHT:
                if i+1 < frames:
                    i += 1
            if event.key == pygame.K_p:
                if playing==0:
                    playing = 1
                elif playing==1:
                    playing = 0
    screen.fill((255, 255, 255))
    screen.blit(bgImgs[i], (0, 0))
    pygame.draw.circle(screen, (0, 0, 0), centres[i], 5)
    pygame.display.flip()

pygame.quit()
