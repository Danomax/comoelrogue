from perlin import *

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
from math import pow

DEBUG = True
GAME_SPEED = 5
#Test Perlin Noise (SimplexNoise)

  

class MyWidget(Widget):

  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    ordn = 0
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self.tilewidth = 16
    self.tileheight = 16
    self.MapWidth,self.MapHeight = 200,200
    self.viewWidth,self.viewHeight = 40,30
    self.scrmap = Map()
    self.scrmap.PerlinMap(self.MapWidth,self.MapHeight)
    self.view = View(self.viewWidth,self.viewHeight,self.MapWidth,self.MapHeight)
    self.viewsize = self.tilewidth*self.view.viewcols,self.tileheight*self.view.viewrows
    self.size = self.viewsize
    #self.scrmap.save_map('perlintest_v4.map')
    self.hero = Hero()
    myforecolor = Colors.color_dict['lightplayer']
    mybackcolor = Colors.color_dict['lightground']
    self.hero.setChar('@',forecolor=myforecolor,backcolor=mybackcolor,block=1,block_sight=1)
    self.hero.set_map_position(self.scrmap.start_position)
    #self.time=0
    Clock.schedule_interval(self.update, 1.0/GAME_SPEED)

  def update(self,*ignore):
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.scrmap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)
    self.view_position = self.view.get_coordinates(self.hero.map_position)
    for row in range(self.view.viewrows):
      for col in range(self.view.viewcols):
        x,y = self.view_position[0]+col,self.view_position[1]+row
        mybackcolor = self.scrmap.Char[y][x].backcolor
        #mybackcolor = [0,0,0,1]
        if self.hero.map_position[0]==x and self.hero.map_position[1]==y:
          myforecolor = self.hero.forecolor
          mytexture = Textures.texture_dict[ord(self.hero.char)].texture
        else:
          myforecolor = self.scrmap.Char[y][x].forecolor
          mytexture = Textures.texture_dict[ord(self.scrmap.Char[y][x].char)].texture
        self.Draw(forecolor=myforecolor,backcolor=mybackcolor,view_position=(col,row),texture=mytexture)

  def on_touch_down(self, touch): 
    self.pos_ini =(touch.x, touch.y)
  
  def on_touch_up(self, touch): 
    self.pos_end = (touch.x, touch.y)
    self.direction = direction(self.pos_ini,self.pos_end)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'spacebar' or keycode[1]=='rshift':
      self.direction = (0,0)
    if keycode[1] == 'up':
      self.direction = (0,-1) 
    elif keycode[1] == 'down':
      self.direction = (0,1)
    elif keycode[1] == 'left':
      self.direction = (-1,0)
    elif keycode[1] == 'right':
      self.direction = (1,0)
    return True

  def Draw(self,forecolor,backcolor,view_position,texture):
    '''
    Dibuja el caracter seteado en texture en la pantalla
    '''
    with self.canvas:
      position = (view_position[0]*self.tilewidth,self.viewsize[1]-((view_position[1]+1)*self.tileheight))
      Color(*backcolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight))
      Color(*forecolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=texture)


class PerlinTestApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  PerlinTestApp().run()