from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock

from random import random,randint

from vector import *
from map import *

DEBUG = True
#Stress the Application on animating the screen

#El resultado mas importante de Stress es que SE DEBE
#limpiar el canvas en cada iteracion de update para no
#saturar la memoria

class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.scrmap = Map()
    self.scrmap.rows,self.scrmap.cols = 40,60
    self.rows,self.cols = self.scrmap.rows,self.scrmap.cols
    self.scrmap_width = self.cols*self.tilewidth
    self.scrmap_height = self.rows*self.tileheight
    self.size = (self.scrmap_width,self.scrmap_height)
    for row in range(self.rows):
      self.scrmap.Char.append([])
      for col in range(self.cols):
        position = (col,row)
        mycolor = [random(),random(),random(),1]
        self.scrmap.Char[row].append(Character())
        ordn = randint(0,255)
        myblock = randint(0,1)
        myblock_sight = randint(0,1)
        self.scrmap.Char[row][-1].setChar(char=chr(ordn),color=mycolor,block=myblock,block_sight=myblock_sight)
        mytexture = self.scrmap.Char[row][-1].texture
        self.Draw(color=mycolor,map_position = position,texture=mytexture)
 
    Clock.schedule_interval(self.update, 1.0/5.0)

  def update(self,*ignore):
    self.canvas.clear()
    for row in range(self.rows):
      for col in range(self.cols):
        mycolor = [random(),random(),random(),1]
        ordn = randint(0,255)
        myblock = randint(0,1)
        myblock_sight = randint(0,1)
        self.scrmap.Char[row][col].setChar(char=chr(ordn),color=mycolor,block=myblock,block_sight=myblock_sight)
        mytexture = self.scrmap.Char[row][col].texture
        self.Draw(color=mycolor,map_position=(col,row),texture=mytexture)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)

  def Draw(self,color,map_position,texture):
    '''
    Dibuja el caracter seteado en texture en la pantalla
    '''
    with self.canvas:
      Color(*color)
      position = (map_position[0]*self.tilewidth,self.scrmap_height-((map_position[1]+1)*self.tileheight))
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=texture)

class StressApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  StressApp().run()