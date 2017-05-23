from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle

from random import random

class Character(Image):
  def __init__(self,**kwargs):
    super(Character, self).__init__(**kwargs)
    self.char = ''

  def setChar(self,char):
    self.char = char
    ordn = ord(self.char)
    #if ordn < 32 or (ordn > 126 and ordn < 161):
    self.source = 'atlas://roguelike16x16_gs_ro/x' + str(ordn)
    #else:
    #  self.source = 'atlas://roguelike16x16_gs_ro/' + chr(ordn)
 
class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    ordn = 0
    self.size = (256,256)
    cols,rows = 16,16
    self.Chr_matrix = []
    #self.myimage = Image(source='roguelike16x16_gs_ro.png',pos=(0,0))
    #self.myimage.size = self.size
    #self.add_widget(self.myimage)
    for row in range(rows):
      self.Chr_matrix.append([])
      for col in range(cols):
        position = (col*16,(rows-row-1)*16)
        size = (16,16)
        mycolor = [random(),random(),random(),1]
        self.Chr_matrix[row].append(Character(pos=position,size=size))
        self.Chr_matrix[row][-1].setChar(chr(ordn))
        with self.canvas:
          Color(*mycolor)
          Rectangle(pos=position,size=size,texture=self.Chr_matrix[row][-1].texture)
        ordn +=1
      

class TestGraphApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  TestGraphApp().run()