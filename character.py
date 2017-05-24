#Character Classes 

#The Character is the minimal Tile Unit in the Game

from kivy.uix.image import Image

class Character(Image):
  def __init__(self,**kwargs):
    super(Character, self).__init__(**kwargs)
    self.char = ''
    self.color = []
    self.block = 0
    self.block_sight = 0 

  def setChar(self,char,color,block,block_sight):
    self.char = char
    ordn = ord(self.char)
    self.color = color
    #if ordn < 32 or (ordn > 126 and ordn < 161):
    self.source = 'atlas://roguelike16x16_gs_ro/x' + str(ordn)
    #else:
    #  self.source = 'atlas://roguelike16x16_gs_ro/' + chr(ordn)
    self.block = block
    self.block_sight = block_sight

  def setColor(self,color):
    self.color = color

  def setBlock(self,block):
    self.block = block

  def setBlock_Sight(self,block_sight):
    self.block_sight = block_sight

class Hero(Character):
  def __init__(self,**kwargs):
    super(Character,self).__init__(**kwargs)
    self.map_position = (0,0)

  def set_map_position(self,position):
    self.map_position = position

  def update_position(self,direction):
    self.map_position = ([mypos+direc for mypos,direc in zip(self.map_position,direction)])
