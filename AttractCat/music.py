from tkinter import *
from tkinter import filedialog
from pygame.locals import *
import time
import pygame
import sys
pygame.init()
 
 
def zanting():
    pygame.mixer.music.pause()
def stop():
    pygame.mixer.music.stop()
def bofang():
    pygame.mixer.music.unpause()
def callback():
    file = filedialog.askopenfilename()
    print(file)
 
 
    #file = ""  # 加上音乐路径
 
 
    print("播放音乐")
 
 
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
 
 
 
 
 
 
 
 
 
 
root = Tk()#窗口
root.title("hello,文祥欧巴啊哈哈")#标题
 
 
root.geometry("400x300+400+200")#更改大小和位置
me = Menu()#一级菜单
root.config(menu=me)#加入一级菜单
menuf = Menu(me)#二级菜单
 
 
pygame.init()
pygame.mixer.init()
 
 
 
 
l = Label(root, text="欢迎来到文祥欧巴啊哈哈的music播放器")
l.pack()
b = Button(root,text = "选择音乐",command = callback)
b.pack()
 
 
f =Button(root,text = "暂停",command = zanting)
f.pack()
bs =Button(root,text = "继续",command = bofang)
bs.pack()
bst =Button(root,text = "停止",command = stop)
bst.pack()
root.mainloop()
 
 
