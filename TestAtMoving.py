from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle

from random import random

#an Arroba moving on the screen

class Character(Image):
  def __init__(self,**kwargs):
    super(Character, self).__init__(**kwargs)
    self.char = ''
    self.mycolor = None

  def setChar(self,char,color):
    self.char = char
    ordn = ord(self.char)
    self.mycolor = color
    #if ordn < 32 or (ordn > 126 and ordn < 161):
    self.source = 'atlas://roguelike16x16_gs_ro/x' + str(ordn)
    #else:
    #  self.source = 'atlas://roguelike16x16_gs_ro/' + chr(ordn)

class Map():
  def __init__(self):
    self.chrmap = []
    self.cols = 0
    self.rows = 0

  def load_from_file(self,filename):
    with open(filename) as f:
      seq = f.readlines()
      seq = [s.strip() for s in seq]
      self.rows=len(seq)
      self.cols=len(seq[0])
      row=0
      for s in seq:
        self.chrmap.append([])
        for ch in s:
          self.chrmap[row].append(ch)
        row+=1
 
  def make_map_dictionary(self,rows,cols):
    ordn = 0
    for row in range(rows):
      self.chrmap.append([])
      for col in range(cols):
        if ordn < 32 or ordn > 126:
          self.chrmap[row].append(' ')
        else:
          self.chrmap[row].append(chr(ordn))
        ordn += 1
    self.cols = cols
    self.rows = rows

  def save_map(self,filename):
    seq=''
    for row in range(self.rows):
      for col in range(self.cols):
        seq += self.chrmap[row][col]
      seq+='\n'
    with open(filename,'w') as f:
      f.write(seq)


class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.scrmap = Map()
    self.scrmap.load_from_file('town.map')
    #self.scrmap.save_map('town2.map')
    self.rows,self.cols = self.scrmap.rows,self.scrmap.cols
    print(str(self.rows)+','+str(self.cols))
    self.scrmap_width = self.cols*self.tilewidth
    self.scrmap_height = self.rows*self.tileheight
    self.size = (self.scrmap_width,self.scrmap_height)
    
    #self.scrmap.save_map('map_dictionary.map')
    for row in range(self.rows):
      for col in range(self.cols):
        position = (col*self.tilewidth,(self.rows-row-1)*self.tileheight)
        mycolor = [random(),random(),random(),1]
        im = Character()
        im.setChar(self.scrmap.chrmap[row][col],color=mycolor)
        with self.canvas:
          Color(*mycolor)
          Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=im.texture)
        ordn +=1
    

class TestGraphApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  TestGraphApp().run()