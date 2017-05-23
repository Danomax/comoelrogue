from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock

from random import random

DEBUG = True
#an Arroba moving on the screen

def direction(pos_ini,pos_end):
  '''
  define la direccion dadas las diferencias entre las posiciones iniciales y finales
  del movimiento touch. 
  '''
  dx = pos_end[0]-pos_ini[0]
  dy = pos_end[1]-pos_ini[1]
  if dx>=0 and dx>= abs(dy):
    direc=(1,0)
  elif dy>=0 and dy>=abs(dx):
    direc=(0,1)
  elif dx<0 and abs(dx)>=abs(dy):
    direc=(-1,0)
  elif dy<0 and abs(dy)>=abs(dx):
    direc=(0,-1)
  return direc

class Character(Image):
  def __init__(self,**kwargs):
    super(Character, self).__init__(**kwargs)
    self.char = ''
    self.mycolor = None
    self.block = 0 

  def setChar(self,char,color,block):
    self.char = char
    ordn = ord(self.char)
    self.mycolor = color
    #if ordn < 32 or (ordn > 126 and ordn < 161):
    self.source = 'atlas://roguelike16x16_gs_ro/x' + str(ordn)
    #else:
    #  self.source = 'atlas://roguelike16x16_gs_ro/' + chr(ordn)
    self.block = block

class Hero(Character):
  def __init__(self,**kwargs):
    super(Character,self).__init__(**kwargs)
    self.map_position = (0,0)

  def set_map_position(self,position):
    self.map_position = position

  def update_position(self,direction):
    self.map_position = ([mypos+direc for mypos,direc in zip(self.map_position,direction)])

class Map():
  def __init__(self):
    self.chrmap = []
    self.blockmap = []
    self.colormap = []
    self.Character=[]
    self.cols = 0
    self.rows = 0

  def load_from_file(self,filename):
    with open(filename) as f:
      st=f.readline().strip()
      a = st.find(',')
      self.rows,self.cols = int(st[:a]),int(st[-a:])
      seq = f.readlines()
      seq = [s.strip() for s in seq]
      row=0
      for s in seq:
        self.chrmap.append([])
        for ch in s:
          self.chrmap[row].append(ch)
        row+=1
      for s in seq:
        self.colormap.append([])
        cl = lista de s en ','
        for col in cl:
          color = 
          self.chrmap[row].append(ch)
        row+=1
      for s in seq:
        self.blockmap.append([])
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
    seq=str(self.rows)+','+str(self.cols)+'\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += self.chrmap[row][col]
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.colormap[row][col][0]) + ','
        seq += str(self.colormap[row][col][1]) + ','
        seq += str(self.colormap[row][col][2]) + ','
        seq += str(self.colormap[row][col][3]) + ','
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.blockmap[row][col])
      seq+='\n'

    with open(filename,'w') as f:
      f.write(seq)


class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.scrmap = Map()
    self.scrmap.load_from_file('town.map')
    self.rows,self.cols = self.scrmap.rows,self.scrmap.cols
    if DEBUG: print(str(self.rows)+','+str(self.cols))
    self.scrmap_width = self.cols*self.tilewidth
    self.scrmap_height = self.rows*self.tileheight
    self.size = (self.scrmap_width,self.scrmap_height)
    for row in range(self.rows):
      self.scrmap.colormap.append([])
      self.scrmap.blockmap.append([])
      self.scrmap.Character.append([])
      for col in range(self.cols):
        position = (col,(self.rows-row-1))
        mycolor = [random(),random(),random(),1]
        self.scrmap.colormap[row].append(mycolor)
        self.scrmap.blockmap[row].append(0)
        self.scrmap.Character[row].append(Character())
        self.scrmap.Character[row][-1].setChar(self.scrmap.chrmap[row][col],color=mycolor,block=0)
        self.Draw(color=mycolor,map_position = position,texture=self.scrmap.Character[row][-1].texture)
        ordn +=1

    self.scrmap.save_map('town2.map')
    self.hero = Hero()
    mycolor = [1,1,1,1]
    self.hero.setChar('@',color=mycolor,block=1)
    position = int(self.cols/2),int(self.rows/2)
    self.hero.set_map_position(position)
    self.Draw(color=self.hero.color,map_position=self.hero.map_position,texture=self.hero.texture)
    Clock.schedule_interval(self.update, 1.0/2.0)

  def update(self,*ignore):
    if self.direction != (0,0):
      x,y = self.hero.map_position
      mycolor = self.scrmap.colormap[y][x]
      mytexture = self.scrmap.Character[y][x].texture
      self.Draw(color=mycolor,map_position=(x,y),texture=mytexture)
      self.hero.update_position(self.direction)
      self.direction = (0,0)
      self.Draw(color=self.hero.color,map_position=self.hero.map_position,texture=self.hero.texture)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    self.direction = direction(self.pos_ini,self.pos_end)

  def Draw(self,color,map_position,texture):
    '''
    Dibuja el caracter seteado en texture en la pantalla
    '''
    with self.canvas:
      Color(*color)
      position = (map_position[0]*self.tilewidth,map_position[1]*self.tileheight)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=texture)

class TestGraphApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  TestGraphApp().run()