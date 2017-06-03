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
    self.tilewidth = 32
    self.tileheight = 32
    self.scrmap = Map()
    self.scrmap.BspTown(100,100)
    self.scrmap.save_map('bsp_v4.map')
    self.viewcols,self.viewrows = (40,20)
    self.viewwidth,self.viewheight = self.tilewidth*self.viewcols,self.tileheight*self.viewrows
    self.size = (self.viewwidth,self.viewheight)
    self.hero = Hero()
    mycolor = Colors.color_dict['light_player']
    self.hero.setChar('@',forecolor=mycolor,backcolor=Colors.color_dict['black'],block=1,block_sight=1)
    self.hero.set_map_position(self.scrmap.start_position)
    #if DEBUG:print('startpos:' + str(self.hero.map_position[0])+','+str(self.hero.map_position[1]))
    self.view_position = self.get_coordinates()
    #if DEBUG:print('viewpos' + str(self.view_position[0])+','+str(self.view_position[1]))
    Clock.schedule_interval(self.update, 1.0/2.0)

  def get_coordinates(self):
    if self.hero.map_position[0] < self.viewcols/2:
      x = 0
    elif self.hero.map_position[0] >= self.scrmap.cols - (self.viewcols/2):
      x = self.scrmap.cols - self.viewcols
    else:
      x = self.hero.map_position[0] - self.viewcols/2
    if self.hero.map_position[1] < self.viewrows/2:
      y = 0
    elif self.hero.map_position[1] >= self.scrmap.rows - (self.viewrows/2):
      y = self.scrmap.rows - self.viewrows
    else:
      y = self.hero.map_position[1] - self.viewrows/2
    return int(x),int(y)

  def update(self,*ignore):
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.scrmap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)
    self.view_position = self.get_coordinates()
    for row in range(self.viewrows):
      for col in range(self.viewcols):
        x,y = self.view_position[0]+col,self.view_position[1]+row
        mybackcolor = self.scrmap.Char[y][x].backcolor
        if self.hero.map_position[0]==x and self.hero.map_position[1]==y:
          myforecolor = self.hero.forecolor
          mytexture = self.hero.texture
        else:
          myforecolor = mybackcolor
          mytexture=self.scrmap.Char[y][x].texture
        self.Draw(forecolor=myforecolor,backcolor=mybackcolor,view_position=(col,row),texture=mytexture)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    self.direction = direction(self.pos_ini,self.pos_end)

  def Draw(self,forecolor,backcolor,view_position,texture):
    '''
    Dibuja el caracter seteado en texture en la pantalla
    '''
    with self.canvas:
      position = (view_position[0]*self.tilewidth,self.viewheight-((view_position[1]+1)*self.tileheight))
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