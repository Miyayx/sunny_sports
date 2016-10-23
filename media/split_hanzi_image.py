# -*- coding:utf-8 -*-
from PIL import Image
import os
import codecs

def yStart(grey):
    m,n = grey.size
    for j in xrange(n):
        for i in xrange(m):
            if grey.getpixel((i,j)) == 0:
                return j
def yEnd(grey):
    m,n = grey.size
    for j in xrange(n-1,-1,-1):
        for i in xrange(m):
            if grey.getpixel((i,j)) == 0:
                return j

def xStart(grey):
    m,n = grey.size
    for i in xrange(m):
        for j in xrange(n):
            if grey.getpixel((i,j)) == 0:
                return i
def xEnd(grey):
    m,n = grey.size
    for i in xrange(m-1,-1,-1):
        for j in xrange(n):
            if grey.getpixel((i,j)) == 0:
                return i
def xBlank(grey):
    m,n = grey.size
    blanks = []
    for i in xrange(m):
        for j in xrange(n):
            if grey.getpixel((i,j)) == 0:
                break
        if j == n-1:
            blanks.append(i)
    return blanks

def yBlank(grey):
    m,n = grey.size
    blanks = []
    for j in xrange(n):
        for i in xrange(m):
            if grey.getpixel((i,j)) == 0:
                break
        if i == m-1:
            blanks.append(j)
    return blanks

def getWordsList():
    f = codecs.open('hanzi-6000.dat', 'r', 'utf-8')
    line = f.read().strip('\n').strip()
    wordslist = list(line)
    print wordslist
    f.close()
    return wordslist

count = 0
wordslist = []
def getWordsByBlank(img,path):
    '''根据行列的空白取图片，效果不错'''
    global count
    global wordslist
    grey = img.split()[0]   
    xblank = xBlank(grey)
    yblank = yBlank(grey)   
    print 'xblank', xblank, len(xblank)
    print 'yblank', yblank, len(yblank)
    #连续的空白像素可能不止一个，但我们只保留连续区域的第一个空白像素和最后一个空白像素，作为文字的起点和终点
    xblank = [xblank[i] for i in xrange(len(xblank)) if i == 0 or i == len(xblank)-1 or not (xblank[i]==xblank[i-1]+1 and xblank[i]==xblank[i+1]-1)]
    yblank = [yblank[i] for i in xrange(len(yblank)) if i == 0 or i == len(yblank)-1 or not (yblank[i]==yblank[i-1]+1 and yblank[i]==yblank[i+1]-1)]    

    for i in xrange(len(xblank)-1, 0, -1):
        if xblank[i]-xblank[i-1] < 150:
            xblank.pop(i)
    print 'xblank', xblank, len(xblank)

    for i in xrange(len(yblank)-1, 0, -1):
        if yblank[i]-yblank[i-1] < 8:
            yblank.pop(i)
    print 'yblank', yblank, len(yblank)
        
    for j in xrange(0, len(yblank)):
        for i in xrange(0, len(xblank)-1):
            area = (xblank[i],yblank[j],xblank[i]+185,yblank[j]+185)#这里固定字的大小是32个像素
            #area = (xblank[i*2],yblank[j*2],xblank[i*2+1],yblank[j*2+1])
            word = img.crop(area)           

            #datas = word.getdata()
            #newData = []
            #for item in datas:
            #    if item[0] == 255 and item[1] == 255 and item[2] == 255:
            #        newData.append((255, 255, 255, 0))
            #    else:
            #        newData.append(item)
            #word.putdata(newData)
            #背景变透明
            word = word.convert("RGBA")
            pixdata = word.load()
            for y in xrange(word.size[1]):
                for x in xrange(word.size[0]):
                    if pixdata[x, y] == (255, 255, 255, 255):
                        pixdata[x, y] = (255, 255, 255, 0)
            #word.save(path+wordslist[count]+'.png')
            word.save(path+str(count)+'.png')
            count += 1
            if count >= len(wordslist):
                return

def getWordsFormImg(imgName,path):
    png = Image.open(imgName,'r')
    img = png.convert('1')
    grey = img.split()[0]
    #先剪出文字区域
    area = (xStart(grey)-20,yStart(grey)-1,xEnd(grey)+20,yEnd(grey))
    img = img.crop(area)    
    img.save(path+'whole.png')
    getWordsByBlank(img,path)

def getWords():
    global wordslist
    wordslist = getWordsList()
    imgs = ["hanzi-6000-{:0>2d}.png".format(i) for i in range(1, 14)]
    imgs = ["hanzi-6000-{:0>3d}.png".format(i) for i in range(1, 168)]
    for img in imgs:        
        img = os.path.join('hanzi-6000-picture/', img)
        getWordsFormImg(img,'hanzi/')
        break

if __name__ == "__main__":
    getWords()
