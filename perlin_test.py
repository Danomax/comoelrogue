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
#Test Perlin Noise (SimplexNoise)

  

class MyWidget(Widget):

  def __init__(self):
    super(MyWidget, self).__init__()
    self.direction = (0,0)
    ordn = 0
    self.tilewidth = 16
    self.tileheight = 16
    self.scrmap = Map()
    self.scrmap.rows = 40
    self.scrmap.cols =60
    self.rows,self.cols = self.scrmap.rows,self.scrmap.cols
    self.scrmap_width = self.cols*self.tilewidth
    self.scrmap_height = self.rows*self.tileheight
    self.size = (self.scrmap_width,self.scrmap_height)
    self.noisemap = []
    self.NoiseMap()
    #self.scrmap.save_map('perlintest_v4.map')
    self.hero = Hero()
    myforecolor = Colors.color_dict['light_player']
    mybackcolor = Colors.color_dict['light_ground']
    self.hero.setChar('@',forecolor=myforecolor,backcolor=mybackcolor,block=1,block_sight=1)
    position = int(self.cols/2),int(self.rows/2)
    self.hero.set_map_position(position)
    self.time=0
    Clock.schedule_interval(self.update, 1.0/5.0)

  def update(self,*ignore):
    self.time += 0.01
    self.canvas.clear()
    if self.direction != (0,0):
      x,y = [pos+direc for pos,direc in zip(self.hero.map_position,self.direction)]
      if self.scrmap.Char[y][x].block==1:
        self.direction = (0,0)
      else:
        self.hero.update_position(self.direction)
    for row in range(self.rows):
      for col in range(self.cols):
        #mybackcolor = self.scrmap.Char[row][col].backcolor
        x,y=self.time+(self.noisefreq*(col/self.noiseperiod)),self.time+(self.noisefreq*row/self.noiseperiod)
        noiseval = 4* self.simplexnoise.noise2(x,y) + 2* self.simplexnoise.noise2(2*x,2*y) + 1* self.simplexnoise.noise2(4*x,4*y)
        rgbval = pow(noiseval/14+0.5,3.0)
        #rgbval = 0.5
        mybackcolor = self.biome(rgbval)
        
        #mybackcolor = [rgbval*0.5,rgbval*0.2,0.0,1]
        if self.hero.map_position[0]==col and self.hero.map_position[1]==row:
          myforecolor = self.hero.color
          mytexture = self.hero.texture
        else:
          myforecolor = self.scrmap.Char[row][col].forecolor
          mytexture = self.scrmap.Char[row][col].texture
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
      position = (map_position[0]*self.tilewidth,self.scrmap_height-((map_position[1]+1)*self.tileheight))
      Color(*backcolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight))
      Color(*forecolor)
      Rectangle(pos=position,size=(self.tilewidth,self.tileheight),texture=texture)

  def NoiseMap(self):
    self.noiseperiod = 512
    self.noisefreq = 8
    self.simplexnoise=SimplexNoise()
    self.simplexnoise.randomize(period=self.noiseperiod)
    for row in range(self.rows):
      self.scrmap.Char.append([])
      for col in range(self.cols):
        x,y=col/self.noiseperiod,row/self.noiseperiod
        noiseval = 4* self.simplexnoise.noise2(x,y) + 2* self.simplexnoise.noise2(2*x,2*y) + 1* self.simplexnoise.noise2(4*x,4*y)
        eleval = noiseval/14+0.5
        mybackcolor = self.biome(eleval)
        myforecolor = Colors.color_dict['red']
        self.scrmap.Char[row].append(Character())
        self.scrmap.Char[row][col].setChar(' ',forecolor=myforecolor,backcolor = mybackcolor,block=0,block_sight=0)

  def biome(self,elev):
    if elev < 0.15: biocolor = Colors.color_dict['seablue']
    elif (elev < 0.3): biocolor = Colors.color_dict['terrain_sand'];
    elif (elev < 0.45): biocolor = Colors.color_dict['terrain_grass'];
    elif (elev < 0.6): biocolor = Colors.color_dict['terrain_deeps'];
    elif (elev < 0.75): biocolor = Colors.color_dict['terrain_dirt']
    elif (elev < 0.9): biocolor = Colors.color_dict['terrain_rock'];
    elif (elev => 0.9): biocolor = Colors.color_dict['terrain_snow'];

class PerlinTestApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  PerlinTestApp().run()