
from character import *
from random import random, randint

BSP_MIN_SIZE = 6
ROOM_MIN_SIZE = 4

class BspNode():
  def __init__(self):
    self.isLeaf = True
    self.pos = 0
    self.size = 0
    self.leftLeaf = None
    self.rightLeaf = None
    self.depth = 0

  def split(self,direction=0):
    if direction == 0: #horizontal split
      if self.size[0] < 2*BSP_MIN_SIZE:
        self.isLeaf = True
        print('Leaf:pos'+str(self.pos[0])+','+str(self.pos[1])+'size'+str(self.size[0])+','+str(self.size[1]))
        return False
      else:
        sep_point = randint(BSP_MIN_SIZE,self.size[0]-BSP_MIN_SIZE)
        print('horiz:'+str(sep_point))
        left_size = (sep_point,self.size[1])
        left_pos = (self.pos[0],self.pos[1])
        right_size = (self.size[0]-sep_point,self.size[1])
        right_pos = (self.pos[0]+sep_point,self.pos[1])
    else: #vertical split
      if self.size[1] < 2*BSP_MIN_SIZE:
        self.isLeaf = True
        print('Leaf:pos'+str(self.pos[0])+','+str(self.pos[1])+'size'+str(self.size[0])+','+str(self.size[1]))
        return False
      else:
        sep_point = randint(BSP_MIN_SIZE,self.size[1]-BSP_MIN_SIZE)
        print('vert:'+str(sep_point))
        left_size = (self.size[0],sep_point)
        left_pos = (self.pos[0],self.pos[1])
        right_size = (self.size[0],self.size[1]-sep_point)
        right_pos = (self.pos[0],self.pos[1]+sep_point)
    self.isLeaf = False
    self.leftLeaf = BspNode()
    self.leftLeaf.depth = self.depth+1
    self.leftLeaf.pos = left_pos
    self.leftLeaf.size = left_size
    self.rightLeaf = BspNode()
    self.rightLeaf.depth = self.depth+1
    self.rightLeaf.pos = right_pos
    self.rightLeaf.size = right_size
    dir = randint(0,1)
    self.leftLeaf.split(direction=dir)
    dir = randint(0,1)
    self.rightLeaf.split(direction=dir)
    return True

  def create_room(self,map,FloorType):
    if not self.isLeaf:
      self.leftLeaf.create_room(map,FloorType)
      self.rightLeaf.create_room(map,FloorType)
    else:
      room_size = (randint(ROOM_MIN_SIZE,self.size[0]-2),randint(ROOM_MIN_SIZE,self.size[1]-2))
      room_pos = (randint(self.pos[0]+1,self.pos[0]+self.size[0]-room_size[0]),randint(self.pos[1]+1,self.pos[1]+self.size[1]-room_size[1]))
      for row in range(room_size[1]):
        for col in range(room_size[0]):
          map[row+room_pos[1]][col+room_pos[0]] = FloorType

class Map():
  def __init__(self):
    self.Char=[]
    self.cols = 0
    self.rows = 0

  def BspTown(self,width,height):
    self.rows = height
    self.cols = width
    pos = (0,0)
    BspTree = BspNode()
    BspTree.pos = pos
    BspTree.size = (width,height)
    dir = randint(0,1)
    BspTree.split(direction=dir)
    for row in range(height):
      self.Char.append([])
      for col in range(width):
        WallType = Character()
        WallType.setChar(char='#',color=[0.5,0.25,0,1],block=1,block_sight=1)
        self.Char[row].append(WallType)
    FloorType = Character()
    FloorType.setChar(char=' ',color=[0,0,0,1],block=0,block_sight=0)
    BspTree.create_room(self.Char,FloorType)

  def load_from_file(self,filename):
    with open(filename) as f:
      st=f.readline().strip()
      a = st.find(',')
      self.rows,self.cols = int(st[:a]),int(st[-a:])
      seq = f.readlines()
      seq = [s.strip() for s in seq]
      row=0
      for row in range(self.rows):
        self.Char.append([])
        for col in range(self.cols):
          self.Char[row].append(Character())
          char = seq[row][col]
          cl = seq[row+self.rows].split(',') #lista de linea en ','
          color = [float(ci) for ci in cl[4*col:(4*(col+1))]] 
          block = int(seq[row+2*self.rows][col])
          block_sight = block
          self.Char[row][-1].setChar(char,color,block,block_sight)

  def make_map_dictionary(self,rows,cols):
    ordn = 0
    for row in range(rows):
      self.Char.append([])
      for col in range(cols):
        self.Char[row].append(Character())
        mycolor = [random(),random(),random(),1]
        if ordn < 32 or ordn > 126:
          self.Char[row][-1].setChar(char=' ',block=0)
        else:
          self.Char[row].append(Character())
          self.Char[row][-1].setChar(char=chr(ordn),color=mycolor,block=1,block_sight=1)
        ordn += 1
    self.cols = cols
    self.rows = rows

  def save_map(self,filename):
    seq=str(self.rows)+','+str(self.cols)+'\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += self.Char[row][col].char
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.Char[row][col].color[0]) + ','
        seq += str(self.Char[row][col].color[1]) + ','
        seq += str(self.Char[row][col].color[2]) + ','
        seq += str(self.Char[row][col].color[3]) + ','
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.Char[row][col].block)
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.Char[row][col].block_sight)
      seq+='\n'

    with open(filename,'w') as f:
      f.write(seq)