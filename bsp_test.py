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
#Test para probar BSP data

class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.scrmap = Map()
    self.scrmap.BspTown(40,20)
    #self.scrmap.load_from_file('bsp_v4.map')
    self.rows,self.cols = self.scrmap.rows,self.scrmap.cols
    self.scrmap_width = self.cols*self.tilewidth
    self.scrmap_height = self.rows*self.tileheight
    self.size = (self.scrmap_width,self.scrmap_height)
    self.scrmap.save_map('bsp_v4.map')
    self.hero = Hero()
    mycolor = Colors.color_dict['light_player']
    self.hero.setChar('@',color=mycolor,block=1,block_sight=1)
    position = self.scrmap.start_position
    self.hero.set_map_position(position)
    Clock.schedule_interval(self.update, 1.0/2.0)

  def update(self,*ignore):
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.scrmap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)

    for row in range(self.rows):
      for col in range(self.cols):
        backcolor = self.scrmap.Char[row][col].color
        if self.hero.map_position[0]==col and self.hero.map_position[1]==row:
          forecolor = self.hero.color
          mytexture = self.hero.texture
        else:
          forecolor = backcolor
          mytexture=self.scrmap.Char[row][col].texture
        self.Draw(forecolor,backcolor,map_position=(col,row),texture=mytexture)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    self.direction = direction(self.pos_ini,self.pos_end)

  def Draw(self,forecolor,backcolor,map_position,texture):
    '''
    Dibuja el caracter seteado en texture en la pantalla
    '''
    with self.canvas:
      position = (map_position[0]*self.tilewidth,self.scrmap_height-((map_position[1]+1)*self.tileheight))
      Color(*backcolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight))
      Color(*forecolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=texture)

class BspTestApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  BspTestApp().run()