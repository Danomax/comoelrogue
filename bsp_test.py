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
    self.scrmap.BspTown(40,20)
    self.rows,self.cols = self.scrmap.rows,self.scrmap.cols
    self.scrmap_width = self.cols*self.tilewidth
    self.scrmap_height = self.rows*self.tileheight
    self.size = (self.scrmap_width,self.scrmap_height)
    for row in range(self.rows):
      for col in range(self.cols):
        position = (col,row)
        mycolor = self.scrmap.Char[row][col].color
        #mycolor = [random(),random(),random(),1]
        mytexture = self.scrmap.Char[row][col].texture
        block = self.scrmap.Char[row][col].block
        self.Draw(color=mycolor,map_position = position,texture=mytexture)
   

    self.scrmap.save_map('bsp.map')
    self.hero = Hero()
    mycolor = [1,1,1,1]
    self.hero.setChar('@',color=mycolor,block=1,block_sight=1)
    position = int(self.cols/2),int(self.rows/2)
    self.hero.set_map_position(position)
    self.Draw(color=self.hero.color,map_position=self.hero.map_position,texture=self.hero.texture)
    Clock.schedule_interval(self.update, 1.0/2.0)

  def update(self,*ignore):
    self.canvas.clear()
    for row in range(self.rows):
      for col in range(self.cols):
        mycolor = self.scrmap.Char[row][col].color
        mytexture = self.scrmap.Char[row][col].texture
        self.Draw(color=mycolor,map_position=(col,row),texture=mytexture)
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.scrmap.Char[y][x].block==1:
        self.direction = (0,0)
        self.Draw(color=self.hero.color,map_position=self.hero.map_position,texture=self.hero.texture)
      else:
        self.hero.update_position(self.direction)
        #self.direction = (0,0)
        self.Draw(color=self.hero.color,map_position=self.hero.map_position,texture=self.hero.texture)
    else:
      self.Draw(color=self.hero.color,map_position=self.hero.map_position,texture=self.hero.texture)

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

class BspTestApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  BspTestApp().run()