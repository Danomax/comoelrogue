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
GAME_SPEED = 5

#FOV Test

class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.mymap = Map()
    #self.mymap.load_from_file('town_v4.map')
    #self.mymap.load_from_file('bsp_v4.map')
    self.viewWidth,self.viewHeight = 40,30
    self.mymap.BspTown(100,100)
    #self.mymap.save_map('bsp_v4.map')
    self.view = View(self.viewWidth,self.viewHeight,self.mymap.cols,self.mymap.rows)
    self.viewsize = self.tilewidth*self.view.viewcols,self.tileheight*self.view.viewrows
    self.size = self.viewsize
    self.hero = Hero()
    mycolor = Colors.color_dict['lightplayer']
    self.hero.setChar('@',forecolor=mycolor,backcolor=Colors.color_dict['black'],block=1,block_sight=1)
    self.hero.set_map_position(self.mymap.start_position)
    self.torchcolor = Colors.color_dict['lightground']
    self.time = 0
    Clock.schedule_interval(self.update, 1.0/GAME_SPEED)

  def update(self,*ignore):
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.mymap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)
    self.view_position = self.view.get_coordinates(self.hero.map_position)
    Cells = self.mymap.calculate_fov(center_x=self.hero.map_position[0],center_y=self.hero.map_position[1],radius=FOV_RADIUS, is_unobstructed=self.mymap.is_unobstructed)
    self.view.update_torch()
    for row in range(self.view.viewrows):
      for col in range(self.view.viewcols):
        x,y = self.view_position[0]+col,self.view_position[1]+row
        #si x,y esta en Cells, se calcula luminosidad (alpha+lerp(lightcolor))
        if (x,y) in Cells:
          mytexture = Textures.texture_dict[ord(self.mymap.Char[y][x].char)].texture
          lum_value = self.view.get_alpha(focus=self.hero.map_position,point=(x,y),radius=FOV_RADIUS)
          if lum_value > self.mymap.Char[y][x].explored:
            self.mymap.Char[y][x].explored = lum_value           
          myforecolor = lerp_color(self.mymap.Char[y][x].forecolor,self.torchcolor,lum_value,0,1)
          #myforecolor = myforecolor[0:3] + [myalpha]
          #mybackcolor = self.mymap.Char[y][x].backcolor
          mybackcolor = lerp_color(self.mymap.Char[y][x].backcolor,self.torchcolor,lum_value,0,1)
          mybackcolor = mybackcolor[0:3] + [0.4 + (0.6*lum_value)]
          if self.hero.map_position[0]==x and self.hero.map_position[1]==y:
            mytexture = Textures.texture_dict[ord(self.hero.char)].texture
            myforecolor = self.hero.forecolor
          self.Draw(forecolor=myforecolor,backcolor=mybackcolor,view_position=(col,row),texture=mytexture)
        else:
          if self.mymap.Char[y][x].explored > 0:
            mytexture = Textures.texture_dict[ord(self.mymap.Char[y][x].char)].texture
            mybackcolor = self.mymap.Char[y][x].backcolor[0:3]+[0.4]
            myforecolor = self.mymap.Char[y][x].forecolor
            if self.hero.map_position[0]==x and self.hero.map_position[1]==y:
              mytexture = Textures.texture_dict[ord(self.hero.char)].texture
              myforecolor = self.hero.forecolor
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
    elif keycode[1] == 'up':
      self.direction = (0,-1) 
    elif keycode[1] == 'down':
      self.direction = (0,1)
    elif keycode[1] == 'left':
      self.direction = (-1,0)
    elif keycode[1] == 'right':
      self.direction = (1,0)
    #print (keycode[1])
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

class Fov_testApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  Fov_testApp().run()