
from character import *
from random import random, randint
from perlin import *
from vector import *
import time
import rpas  #FOV algorythm 

BSP_MIN_SIZE = 8
ROOM_MIN_SIZE = 3
FOV_RADIUS = 10
FILE_VERSION = 4

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

  def create_room(self,map):
    if not self.isLeaf:
      self.room_data += self.leftLeaf.create_room(map)
      self.room_data += self.rightLeaf.create_room(map)
    else:
      self.room_size = (randint(ROOM_MIN_SIZE,self.size[0]-2),randint(ROOM_MIN_SIZE,self.size[1]-2))
      self.room_pos = (randint(self.pos[0]+1,self.pos[0]+self.size[0]-self.room_size[0]-1),randint(self.pos[1]+1,self.pos[1]+self.size[1]-self.room_size[1]-1))
      self.room_data += 'room,roompos,'+str(self.room_pos[0])+','+str(self.room_pos[1])+',roomsize,'+str(self.room_size[0])+','+str(self.room_size[1])+'\n'
      map.put_rectangle(self.room_pos,self.room_size)
    return self.room_data

  def create_corridors(self,map):
    if self.isLeaf:
      return self.corridor_data
    else:
      #obtiene la Leaf mas a la derecha del hijo izquierdo y vice versa
        RightestLeaf = self.leftLeaf.get_leaf('right')
        LeftestLeaf = self.rightLeaf.get_leaf('left')
        if self.split_direction == 0:
          #corredor horizontal
          start_y = randint(RightestLeaf.room_pos[1],RightestLeaf.room_pos[1]+RightestLeaf.room_size[1])
          end_y = randint(LeftestLeaf.room_pos[1],LeftestLeaf.room_pos[1]+LeftestLeaf.room_size[1])
          middle_x = randint(RightestLeaf.room_pos[0]+RightestLeaf.room_size[0],LeftestLeaf.room_pos[0])
          map.put_h_line(RightestLeaf.room_pos[0]+RightestLeaf.room_size[0],middle_x,start_y)
          map.put_v_line(middle_x,start_y,end_y)
          map.put_h_line(middle_x,LeftestLeaf.room_pos[0],end_y)
          self.corridor_data += 'hcorridor,starty,'+str(start_y)+',endy,'+str(end_y)+',middlex,'+str(middle_x)+'\n'
        elif self.split_direction ==1:
          start_x = randint(RightestLeaf.room_pos[0],RightestLeaf.room_pos[0]+RightestLeaf.room_size[0])
          end_x = randint(LeftestLeaf.room_pos[0],LeftestLeaf.room_pos[0]+LeftestLeaf.room_size[0])
          middle_y = randint(RightestLeaf.room_pos[1]+RightestLeaf.room_size[1],LeftestLeaf.room_pos[1])
          map.put_v_line(start_x,RightestLeaf.room_pos[1]+RightestLeaf.room_size[1],middle_y)
          map.put_h_line(start_x,end_x,middle_y)
          map.put_v_line(end_x,middle_y,LeftestLeaf.room_pos[1])
          self.corridor_data += 'vcorridor,startx,'+str(start_x)+',endx,'+str(end_x)+',middley,'+str(middle_y)+'\n'
        self.corridor_data += self.leftLeaf.create_corridors(map)
        self.corridor_data += self.rightLeaf.create_corridors(map)
        return self.corridor_data

  def get_center_position(self,direction):
    if self.isLeaf:
      return (int(self.room_pos[0]+(self.room_size[0]/2)),int(self.room_pos[1]+(self.room_size[1]/2)))
    else:
      if direction == 'left':
        return self.leftLeaf.get_center_position('left')
      elif direction == 'right':
        return self.rightLeaf.get_center_position('right')
      if direction=='random':
        choose = randint(0,1)
        if choose == 0:
          return self.leftLeaf.get_center_position('random')
        else:
          return self.rightLeaf.get_center_position('random')

  def get_leaf(self,direction):
    '''obtiene una hoja dependiendo de direction
    direction = 'left','right','random'
    '''
    if self.isLeaf:
      return self
    else:
      if direction == 'left':
        return self.leftLeaf.get_leaf('left')
      elif direction == 'right':
        return self.rightLeaf.get_leaf('right')
      elif direction == 'random':
        choose = randint(0,1)
        if choose == 0:
          return self.leftLeaf.get_leaf('random')
        elif choose == 1:
          return self.rightLeaf.get_leaf('random')

class View():
  def __init__(self,cols,rows,map_cols,map_rows):
    self.viewcols = cols
    self.viewrows = rows
    self.mapcols = map_cols
    self.maprows = map_rows
    noiseperiod = 256
    noisefreq = 1
    self.torchnoise = SimplexNoise()
    self.torchnoise.randomize(period=noiseperiod)
    self.torchview = [0,0]

  def get_alpha(self,focus,point,radius):
    '''
    obtiene el nivel de alpha dependiendo de la distancia al foco y el ruido torchnoise
    '''
    #se mueve ligeramente el focus (titileo)
    a = self.torchnoise.noise2(self.torchview[0],self.torchview[0])
    b = self.torchnoise.noise2(self.torchview[1],self.torchview[1])
    focus = [focus[0]+0.5*a,focus[1]+0.5*b]
    dist = distance(focus,point)
    dist += self.torchnoise.noise2(self.torchview[0],self.torchview[1])
    ratio = 2 * (dist / (radius)) # a igual distancia del radius el ratio debe valer 2  
    sig = sigmoid(value=ratio,gain=1)
    return sig

  def update_torch(self):
    direction = [random(),random()]
    self.torchview = [t+0.2*d for t,d in zip(self.torchview,direction)]

  def get_coordinates(self,position):
    '''obtiene las coordenadas de la vista dada la posicion del objeto
    en position y el tamano del mapa en cols,rows
    '''
    if position[0] < self.viewcols/2:
      x = 0
    elif position[0] >= self.mapcols - (self.viewcols/2):
      x = self.mapcols - self.viewcols
    else:
      x = position[0] - self.viewcols/2
    if position[1] < self.viewrows/2:
      y = 0
    elif position[1] >= self.maprows - (self.viewrows/2):
      y = self.maprows - self.viewrows
    else:
      y = position[1] - self.viewrows/2
    return int(x),int(y)

class Map():
  def __init__(self):
    self.Char=[]
    self.Back=[]
    self.cols = 0
    self.rows = 0
    self.start_position = (0,0)
    self.bsp_data = ''
    self.fov = rpas.FOVCalc()
    # FOV settings parameters; middle restrictive
    self.fov.NOT_VISIBLE_BLOCKS_VISION = True
    self.fov.RESTRICTIVENESS = 1
    self.fov.VISIBLE_ON_EQUAL = True

  def is_unobstructed(self,x,y):
    try:
      if self.Char[int(y)][int(x)].block_sight == 1:
        return False
      else:
        return True  
    except IndexError:
        return False

  def calculate_fov(self,center_x,center_y,radius, is_unobstructed):
    cells = self.fov.calc_visible_cells_from(center_x, center_y, radius, is_unobstructed)
    return cells

  def put_rectangle(self,pos,size):
    for row in range(size[1]):
      for col in range(size[0]):
          self.Char[row+pos[1]][col+pos[0]].copyChar(self.Back[row+pos[1]][col+pos[0]])

  def put_v_line(self,x,y_ini,y_end):
    if y_ini < y_end+1:
      for row in range(y_ini,y_end+1):
        self.Char[row][x].copyChar(self.Back[row][x])
    else:
      for row in range(y_end,y_ini+1):
        self.Char[row][x].copyChar(self.Back[row][x])

  def put_h_line(self,x_ini,x_end,y):
    if x_ini < x_end+1:
      for col in range(x_ini,x_end+1):
        self.Char[y][col].copyChar(self.Back[y][col])
    else:
      for col in range(x_end,x_ini+1):
        self.Char[y][col].copyChar(self.Back[y][col])
  
  
  def PerlinTwoColor(self,width,height,color1,color2):
    '''
    genera un mapa en self.Back con ruido Perlin entre 2 colores
    '''
    noiseperiod = 256
    noisefreq = 8
    colornoise=SimplexNoise()
    colornoise.randomize(period=noiseperiod)
    octaves = 4
    self.Back = []
    for row in range(height):
      self.Back.append([])
      for col in range(width):
        x,y=noisefreq*col/noiseperiod,noisefreq*row/noiseperiod
        noiseval = 0
        for octave in range(octaves):
          val = 2**octave
          noiseval += (2*octaves/val)*colornoise.noise2(val*x,val*y)
        noiseval = pow(noiseval/(2**octaves-1)+0.5,1.0)
        mybackcolor = lerp_color(color1,color2,noiseval,0,1)
        myChar = Character()
        myChar.setChar(char=' ',forecolor = Colors.color_dict['black'],backcolor=mybackcolor,block=0,block_sight=0)
        self.Back[row].append(myChar)


  def PerlinMap(self,width,height):
    noiseperiod = 256
    noisefreq = 2
    self.heightnoise=SimplexNoise()
    self.heightnoise.randomize(period=noiseperiod)
    self.climatenoise=SimplexNoise()
    self.climatenoise.randomize(period=noiseperiod)
    octaves = 4
    for row in range(height):
      self.Char.append([])
      for col in range(width):
        x,y=noisefreq*col/noiseperiod,noisefreq*row/noiseperiod
        heightval = 0
        climateval = 0
        for octave in range(octaves):
          val = 2**octave
          heightval += (2*octaves/val)*self.heightnoise.noise2(val*x,val*y)
          climateval += (2*octaves/val)*self.climatenoise.noise2(val*x,val*y)
        heightval = pow(heightval/(2**octaves-1)+0.5,3.0)
        climateval = pow(climateval/(2**octaves-1)+0.5,3.0)
        mybackcolor = self.biome2(heightval,climateval)
        myforecolor = Colors.color_dict['red']
        self.Char[row].append(Character())
        self.Char[row][col].setChar(' ',forecolor=myforecolor,backcolor = mybackcolor,block=0,block_sight=0)
    self.start_position = int(width/2),int(height/2)

  def biome1(self,elev):
    if elev < 0.05: biocolor = Colors.color_dict['terrain_deeps']
    elif (elev < 0.1): biocolor = Colors.color_dict['terrain_shallow']
    elif (elev < 0.3): biocolor = Colors.color_dict['terrain_sand']
    elif (elev < 0.5): biocolor = Colors.color_dict['terrain_grass']
    elif (elev < 0.7): biocolor = Colors.color_dict['terrain_dirt']
    elif (elev < 0.9): biocolor = Colors.color_dict['terrain_rock']
    elif (elev >= 0.9): biocolor = Colors.color_dict['terrain_snow']
    return [bio+(elev%0.2-0.2) for bio in biocolor]

  def biome2(self,heightval,climateval):
    e = heightval
    m = climateval
    if (e < 0.075): biocolor = Colors.color_dict['terrain_deeps']
    elif (e < 0.15): biocolor = Colors.color_dict['terrain_shallow']
  
    elif (e > 0.7):
      if (m < 0.1): biocolor = Colors.color_dict['terrain_sand']
      elif (m < 0.2): biocolor = Colors.color_dict['terrain_shore']
      elif (m < 0.5): biocolor = Colors.color_dict['terrain_grass']
      else: biocolor = Colors.color_dict['terrain_snow']

    elif (e > 0.5):
      if (m < 0.33): biocolor = Colors.color_dict['terrain_sand']
      elif (m < 0.66): biocolor = Colors.color_dict['forestgreen']
      else: biocolor = Colors.color_dict['snow']

    elif (e > 0.3):
      if (m < 0.16): biocolor = Colors.color_dict['terrain_dirt']
      elif (m < 0.50): biocolor = Colors.color_dict['palegreen']
      elif (m < 0.83): biocolor = Colors.color_dict['olivegreen']
      else: biocolor = Colors.color_dict['seagreen']

    else:
      if (m < 0.16): biocolor = Colors.color_dict['dust']
      elif (m < 0.33): biocolor = Colors.color_dict['terrain_rock']
      elif (m < 0.66): biocolor = Colors.color_dict['wheat']
      else: biocolor = Colors.color_dict['snow']
    
    return [bio + (e*0.15) for bio in biocolor]
    #return biocolor

  def BspTown(self,width,height):
    '''
    The Town, created by BSP
    '''
    a_time = time.clock()
    self.rows = height
    self.cols = width
    pos = (0,0)
    self.start_position = (int(width/2),int(height/2))
    BspTree = BspNode(depth=0,pos=pos,size=(width,height))
    dir = randint(0,1)
    self.bsp_data += BspTree.split(direction=dir)
    b_time = time.clock()
    color1 = Colors.color_dict['darkbrick']
    color2 = Colors.color_dict['darkmetal']
    self.PerlinTwoColor(width,height,color1,color2)
    for row in range(height):
      self.Char.append([])
      for col in range(width):
        WallType = Character()
        #mybackcolor = color1
        mybackcolor = self.Back[row][col].backcolor
        WallType.setChar(char=' ',forecolor=Colors.color_dict['black'],backcolor=mybackcolor,block=1,block_sight=1)
        self.Char[row].append(WallType)
    c_time = time.clock()
    color1 = Colors.color_dict['darkground']
    color2 = Colors.color_dict['darkgreen']
    self.PerlinTwoColor(width,height,color1,color2)
    self.bsp_data += 'rooms\n' + BspTree.create_room(self)
    self.bsp_data += 'corridors\n' + BspTree.create_corridors(self)
    d_time = time.clock()
    self.start_position = BspTree.get_center_position('random')
    e_time = time.clock()
    print(str(a_time)+',\n'+str(b_time)+',\n'+str(c_time)+',\n'+str(d_time)+',\n'+str(e_time))

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
      #seq = [s.strip() for s in seq]
      row=0
      for row in range(self.rows):
        self.Char.append([])
        for col in range(self.cols):
          self.Char[row].append(Character())
          char = seq[row][col]
          fcl = seq[row+self.rows].split(',') #lista de linea en ','
          forecolor = [float(ci) for ci in fcl[4*col:(4*(col+1))]]
          bcl = seq[row+2*self.rows].split(',') #lista de linea en ','
          backcolor = [float(ci) for ci in bcl[4*col:(4*(col+1))]]
          block_data = int(seq[row+3*self.rows][col])
          block = block_data%2
          block_sight = int(block_data/2)
          self.Char[row][-1].setChar(char,forecolor,backcolor,block,block_sight)
      for s in seq[(4*self.rows+1):]:
        self.bsp_data += s + '\n'
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
        seq += str(self.Char[row][col].forecolor[0]) + ','
        seq += str(self.Char[row][col].forecolor[1]) + ','
        seq += str(self.Char[row][col].forecolor[2]) + ','
        seq += str(self.Char[row][col].forecolor[3]) + ','
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.Char[row][col].backcolor[0]) + ','
        seq += str(self.Char[row][col].backcolor[1]) + ','
        seq += str(self.Char[row][col].backcolor[2]) + ','
        seq += str(self.Char[row][col].backcolor[3]) + ','
      seq+='\n'
    for row in range(self.rows):
      for col in range(self.cols):
        seq += str(self.Char[row][col].block+2*self.Char[row][col].block_sight)
      seq+='\n'
    seq+='bspdata:\n'+self.bsp_data
    with open(filename,'w') as f:
      f.write(seq)