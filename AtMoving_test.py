from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock

from random import random

from vector import *
from map import *

DEBUG = True
#an Arroba moving on the screen

class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.mymap = Map()
    self.mymap.load_from_file('town_v4.map')
    self.rows,self.cols = self.mymap.rows,self.mymap.cols
    if DEBUG: print(str(self.rows)+','+str(self.cols))
    self.mymap_width = self.cols*self.tilewidth
    self.mymap_height = self.rows*self.tileheight
    self.size = (self.mymap_width,self.mymap_height)
    for row in range(self.rows):
      for col in range(self.cols):
        position = (col,row)
        myforecolor = self.mymap.Char[row][col].forecolor
        mybackcolor = self.mymap.Char[row][col].backcolor
        #mycolor = [random(),random(),random(),1]
        mytexture = Textures.texture_dict[ord(self.mymap.Char[row][col].char)].texture
        self.Draw(forecolor=myforecolor,backcolor=mybackcolor,map_position = position,texture=mytexture)
    #self.scrmap.save_map('hardbuild_v1.map')
    self.hero = Hero()
    myforecolor = Colors.color_dict['light_player']
    mybackcolor = [0,0,0,1]
    self.hero.setChar('@',forecolor=myforecolor,backcolor=mybackcolor,block=1,block_sight=1)
    position = int(self.cols/2),int(self.rows/2)
    self.hero.set_map_position(position)
    mytexture = Textures.texture_dict[ord(self.hero.char)].texture
    self.Draw(forecolor=self.hero.color,backcolor=self.hero.backcolor,map_position=self.hero.map_position,texture=mytexture)
    Clock.schedule_interval(self.update, 1.0/2.0)

  def update(self,*ignore):
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.mymap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)
    for row in range(self.rows):
      for col in range(self.cols):
        mybackcolor = self.mymap.Char[row][col].backcolor
        if self.hero.map_position[0]==col and self.hero.map_position[1]==row:
          myforecolor = self.hero.forecolor
          mytexture = Textures.texture_dict[ord(self.hero.char)].texture
        else:
          myforecolor = self.mymap.Char[row][col].forecolor
          mytexture = Textures.texture_dict[ord(self.mymap.Char[row][col].char)].texture
        self.Draw(forecolor=myforecolor,backcolor=mybackcolor,map_position=(col,row),texture=mytexture)

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
      position = (map_position[0]*self.tilewidth,self.mymap_height-((map_position[1]+1)*self.tileheight))
      Color(*backcolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight))
      Color(*forecolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=texture)

class AtMoving_testApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  AtMoving_testApp().run()