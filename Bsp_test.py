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
GAME_SPEED = 5
#Test para probar BSP data

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
    self.mymap.BspTown(40,20)
    #self.mymap.load_from_file('bsp_v4.map')
    self.rows,self.cols = self.mymap.rows,self.mymap.cols
    self.mymap_width = self.cols*self.tilewidth
    self.mymap_height = self.rows*self.tileheight
    self.size = (self.mymap_width,self.mymap_height)
    #self.mymap.save_map('bsp_v4.map')
    self.hero = Hero()
    mycolor = Colors.color_dict['lightplayer']
    self.hero.setChar('@',forecolor=mycolor,backcolor=Colors.color_dict['black'],block=1,block_sight=1)
    position = self.mymap.start_position
    self.hero.set_map_position(position)
    Clock.schedule_interval(self.update, 1.0/GAME_SPEED)

  def update(self,*ignore):
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.mymap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)

    #for row in range(self.rows):
    #  for col in range(self.cols):
    #    mybackcolor = self.mymap.Char[row][col].backcolor
    #    if self.hero.map_position[0]==col and self.hero.map_position[1]==row:
    #      myforecolor = self.hero.forecolor
    #      mytexture = Textures.texture_dict[ord(self.hero.texture)].texture
    #    else:
    #      myforecolor = mybackcolor
    #      mytexture=Textures.texture_dict[ord(self.mymap.Char[row][col])].texture
    #    self.Draw(forecolor=myforecolor,backcolor=mybackcolor,map_position=(col,row),texture=mytexture)

    cells = self.mymap.calculate_fov(center_x=self.hero.map_position[0],center_y=self.hero.map_position[1],radius=FOV_RADIUS, is_unobstructed=self.mymap.is_unobstructed)
    for (col,row) in cells:
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

class Bsp_testApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  Bsp_testApp().run()