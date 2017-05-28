
from character import *
from random import random, randint

BSP_MIN_SIZE = 8
ROOM_MIN_SIZE = 3
FILE_VERSION = 3

class BspNode():
  def __init__(self,depth,pos,size):
    self.depth = depth
    self.isLeaf = False
    self.pos = pos
    self.size = size
    self.leftLeaf = None
    self.rightLeaf = None
    self.split_direction = 0
    self.room_pos = (0,0)
    self.room_size = (0,0)
    self.bsp_data = 'depth,'+str(self.depth)+',pos,'+str(self.pos[0])+','+str(self.pos[1])+',size,'+str(self.size[0])+','+str(self.size[1])+'\n'
    self.room_data = ''
    self.corridor_data = ''

  def split(self,direction=0):
    self.split_direction = direction
    if direction == 0: #horizontal split
      if self.size[0] < 2*BSP_MIN_SIZE:
        self.isLeaf = True
        self.bsp_data += 'Leaf\n'
        return self.bsp_data
      else:
        self.bsp_data += 'direction,' + str(self.split_direction) +'\n'
        sep_point = randint(BSP_MIN_SIZE,self.size[0]-BSP_MIN_SIZE)
        left_size = (sep_point,self.size[1])
        left_pos = (self.pos[0],self.pos[1])
        right_size = (self.size[0]-sep_point,self.size[1])
        right_pos = (self.pos[0]+sep_point,self.pos[1])
        self.bsp_data += 'sep point,'+str(sep_point)+'\n'
    else: #vertical split
      if self.size[1] < 2*BSP_MIN_SIZE:
        self.isLeaf = True
        self.bsp_data += 'Leaf\n'
        return self.bsp_data
      else:
        self.bsp_data += 'direction,' + str(self.split_direction) +'\n'
        sep_point = randint(BSP_MIN_SIZE,self.size[1]-BSP_MIN_SIZE)
        left_size = (self.size[0],sep_point)
        left_pos = (self.pos[0],self.pos[1])
        right_size = (self.size[0],self.size[1]-sep_point)
        right_pos = (self.pos[0],self.pos[1]+sep_point)
        self.bsp_data += 'sep point,'+str(sep_point)+'\n'
    self.isLeaf = False
    self.leftLeaf = BspNode(self.depth+1,left_pos,left_size)
    self.rightLeaf = BspNode(self.depth+1,right_pos,right_size)
    dir = randint(0,1)
    self.bsp_data += self.leftLeaf.split(direction=dir)
    dir = randint(0,1)
    self.bsp_data += self.rightLeaf.split(direction=dir)
    return self.bsp_data

  def create_room(self,map,FloorType):
    if not self.isLeaf:
      self.room_data += self.leftLeaf.create_room(map,FloorType)
      self.room_data += self.rightLeaf.create_room(map,FloorType)
    else:
      self.room_size = (randint(ROOM_MIN_SIZE,self.size[0]-2),randint(ROOM_MIN_SIZE,self.size[1]-2))
      self.room_pos = (randint(self.pos[0]+1,self.pos[0]+self.size[0]-self.room_size[0]-1),randint(self.pos[1]+1,self.pos[1]+self.size[1]-self.room_size[1]-1))
      self.room_data += 'room,roompos,'+str(self.room_pos[0])+','+str(self.room_pos[1])+',roomsize,'+str(self.room_size[0])+','+str(self.room_size[1])+'\n'
      WallType = Character()
      WallType.setChar('#',color=[0,0,random(),1],block=1,block_sight=1)
      map.put_rectangle(self.pos,self.size,WallType)
      
      map.put_rectangle(self.room_pos,self.room_size,FloorType)
    return self.room_data

  def create_corridors(self,map,FloorType):
    #find Leafs and make a corridor between them
    if not self.isLeaf:
      (leftpos,leftsize,left_data) = self.leftLeaf.create_corridors(map,FloorType)
      self.corridor_data += left_data
      (rightpos,rightsize,right_data) = self.rightLeaf.create_corridors(map,FloorType)
      self.corridor_data += right_data
      if self.split_direction == 0:
        #corredor horizontal
        start_y = randint(leftpos[1],leftpos[1]+leftsize[1])
        end_y = randint(rightpos[1],rightpos[1]+rightsize[1])
        if leftpos[0]+leftsize[0] < rightpos[0]:
          middle_x = randint(leftpos[0]+leftsize[0],rightpos[0])
        else:
          middle_x = leftpos[0]+leftsize[0]
        map.put_h_line(leftpos[0]+leftsize[0],middle_x,start_y,FloorType)
        map.put_v_line(middle_x,start_y,end_y,FloorType)
        map.put_h_line(middle_x,rightpos[0],end_y,FloorType)
        self.corridor_data += 'hcorridor,starty,'+str(start_y)+',endy,'+str(end_y)+',middlex,'+str(middle_x)+'\n'
      elif self.split_direction == 1:
        #corredor vertical
        start_x = randint(leftpos[0],leftpos[0]+leftsize[0])
        end_x = randint(rightpos[0],rightpos[0]+rightsize[0])
        if leftpos[1]+leftsize[1] < rightpos[1]:
          middle_y = randint(leftpos[1]+leftsize[1],rightpos[1])
        else:
          middle_y = leftpos[1]+leftsize[1]
        map.put_v_line(start_x,leftpos[1]+leftsize[1],middle_y,FloorType)
        map.put_h_line(start_x,end_x,middle_y,FloorType)
        map.put_v_line(end_x,middle_y,rightpos[1],FloorType)
        self.corridor_data += 'vcorridor,startx,'+str(start_x)+',endx,'+str(end_x)+',middley,'+str(middle_y)+'\n'
      return(self.leftLeaf.room_pos,self.leftLeaf.room_size,self.corridor_data)
    else:
      return(self.room_pos,self.room_size,self.corridor_data)

  def get_center_position(self):
    if self.isLeaf:
      return (int(self.room_pos[0]+(self.room_size[0]/2)),int(self.room_pos[1]+(self.room_size[1]/2)))
    else:
      choose = randint(0,1)
      if choose == 0:
        return self.leftLeaf.get_center_position()
      else:
        return self.rightLeaf.get_center_position()

class Map():
  def __init__(self):
    self.Char=[]
    self.cols = 0
    self.rows = 0
    self.start_position = (0,0)
    self.bsp_data = ''

  def put_rectangle(self,pos,size,CharType):
    for row in range(size[1]):
      for col in range(size[0]):
          self.Char[row+pos[1]][col+pos[0]] = CharType

  def put_v_line(self,x,y_ini,y_end,CharType):
    if y_ini < y_end+1:
      for row in range(y_ini,y_end+1):
        self.Char[row][x] = CharType
    else:
      for row in range(y_end,y_ini+1):
        self.Char[row][x] = CharType

  def put_h_line(self,x_ini,x_end,y,CharType):
    if x_ini < x_end+1:
      for col in range(x_ini,x_end+1):
        self.Char[y][col] = CharType
    else:
      for col in range(x_end,x_ini+1):
        self.Char[y][col] = CharType


  def BspTown(self,width,height):
    '''
    The Town, created by BSP
    '''
    self.rows = height
    self.cols = width
    pos = (0,0)
    self.start_position = (int(width/2),int(height/2))
    BspTree = BspNode(depth=0,pos=pos,size=(width,height))
    dir = randint(0,1)
    self.bsp_data += BspTree.split(direction=dir)
    for row in range(height):
      self.Char.append([])
      for col in range(width):
        WallType = Character()
        WallType.setChar(char='#',color=[0.5,0.25,0,1],block=1,block_sight=1)
        self.Char[row].append(WallType)
    FloorType = Character()
    FloorType.setChar(char='.',color=[0,0.7,0,1],block=0,block_sight=0)
    self.bsp_data += 'rooms\n' + BspTree.create_room(self,FloorType)
    CorridorType = Character()
    CorridorType.setChar(char=',',color=[0.7,0,0,1],block=0,block_sight=0)
    self.bsp_data += 'corridors\n' + BspTree.create_corridors(self,CorridorType)[2]
    self.start_position = BspTree.get_center_position()

  def load_from_file(self,filename):
    with open(filename) as f:
      st=f.readline().strip()
      head = st.split(',')
      file_ver = int(head[0])
      if file_ver != FILE_VERSION:
        print('error: incompatible version of map file')
        return False
      self.rows,self.cols = int(head[1]),int(head[2])
      self.start_position = int(head[3]),int(head[4])
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
          block_data = int(seq[row+2*self.rows][col])
          block = block_data%2
          block_sight = int(block_data/2)
          self.Char[row][-1].setChar(char,color,block,block_sight)
      for s in seq[3*self.rows:]:
        self.bsp_data += s + '\n'
      print(self.bsp_data)
      return True

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
    seq=str(FILE_VERSION)+','+str(self.rows)+','+str(self.cols)+','+str(self.start_position[0])+','+str(self.start_position[1])+'\n'
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
        seq += str(self.Char[row][col].block+2*self.Char[row][col].block_sight)
      seq+='\n'
    seq+='bspdata:\n'+self.bsp_data
    with open(filename,'w') as f:
      f.write(seq)