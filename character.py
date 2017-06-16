#Character Classes 

#The Character is the minimal Tile Unit in the Game

from kivy.uix.image import Image

class ColorDict():
  #Diccionario de Colores
  def __init__(self,**kwargs):
    self.color_dict = {}

  def load_colors(self,filename):
    with open(filename) as f:
      seq = f.readlines()
      seq = [s.strip() for s in seq]
      for line in seq:
        line_list = [i for i in line.split(',')]
        if line_list[0][0] != '#':
          name = line_list[0]
          r = float(line_list[1])
          g = float(line_list[2])
          b = float(line_list[3])
          a = float(line_list[4])
          self.color_dict[name] = [r,g,b,a]  

  def save_color(self,filename):
    for name in self.color_dict:
      r = str(color_dict[name][0])
      g = str(color_dict[name][1])
      b = str(color_dict[name][2])
      a = str(color_dict[name][3])
      seq += name + ',' + r + ',' + g + ',' + b + ',' + a + '\n'    
    with open(filename,'w') as f: 
      f.write(seq)

Colors = ColorDict()
Colors.load_colors('colors_kivy.def')

class TextureDict():
  def __init__(self,**kwargs):
    super(TextureDict,self).__init__(**kwargs)
    self.texture_dict = {}
  
  def load_chars(self,filename):
    ordn = 0
    for ordn in range(256):
      #if ordn < 32 or (ordn > 126 and ordn < 161):
      self.texture_dict[ordn] = Image()
      self.texture_dict[ordn].source = 'atlas://'+filename+'/x' + str(ordn)
      #else:
      #  self.source = 'atlas://'+filename+'/' + chr(ordn)

Textures = TextureDict()
Textures.load_chars('roguelike16x16_gs_ro2')

class Character():
  def __init__(self,**kwargs):
    self.char = ''
    self.backcolor = Colors.color_dict['black']
    self.forecolor = Colors.color_dict['black']
    self.block = 0
    self.block_sight = 0 
    self.explored = 0

  def setChar(self,char,forecolor,backcolor,block,block_sight):
    self.char = char
    ordn = ord(self.char)
    self.forecolor = forecolor
    self.backcolor = backcolor
    self.block = block
    self.block_sight = block_sight

  def copyChar(self,Source):
    self.char = Source.char
    self.backcolor = Source.backcolor
    self.forecolor = Source.forecolor
    self.block = Source.block
    self.block_sight = Source.block_sight
    self.explored = Source.explored

class Hero(Character):
  def __init__(self,**kwargs):
    super(Character,self).__init__(**kwargs)
    self.map_position = (0,0)

  def set_map_position(self,position):
    self.map_position = position

  def update_position(self,direction):
    self.map_position = ([mypos+direc for mypos,direc in zip(self.map_position,direction)])
