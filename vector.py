#Vector Functions 

import math
import colorsys 

def distance_square(p,q):
  '''
  devuelve la distancia al cuadrado entre dos puntos
  '''
  dx = p[0] - q[0]
  dy = p[1] - q[1]
  return (dx ** 2 + dy ** 2)

def distance(p,q):
  return math.sqrt(distance_square(p,q))

def sigmoid(value,gain=1):
  '''
  Funcion Sigmoide
  '''
  #en 0, la funcion retorna (casi) gain, en 1 retorna 0.5gain, en 2 retorna (casi) 0
  return gain/(1.0+math.exp(3*(float(value)-1.0)))

def gauss(value, center_level, dev):
  '''
  Funcion Campana Gauss
  '''
  f_value = float(value)
  f_center_level = float(center_level)
  #devuelve un 1 en el nivel central
  return math.exp(-(f_value-f_center_level)*(f_value-f_center_level)/(2*dev))

def decay(gain,x,decayment,curve='power'):
  '''
  funcion que devuelve el valor disminuido segun una curva
  '''
  if curve=='power':
    return int(math.floor(math.pow(gain,1-(x/decayment))))
  elif curve=='lineal':
    return int(math.floor((gain-x)/decayment))

def direction(pos_ini,pos_end):
  '''
  define la direccion dadas las diferencias entre las posiciones iniciales y finales
  del movimiento touch. 
  '''
  dx = pos_end[0]-pos_ini[0]
  dy = pos_end[1]-pos_ini[1]
  if dx>=0 and dx>= abs(dy):
    direc=(1,0)
  elif dy>=0 and dy>=abs(dx):
    direc=(0,-1)
  elif dx<0 and abs(dx)>=abs(dy):
    direc=(-1,0)
  elif dy<0 and abs(dy)>=abs(dx):
    direc=(0,1)
  elif dx==0 and dy==0:
    direc=(0,0)
  return direc

def lerp_color(color1,color2,value,start_value,end_value):
  '''
  linear interpolation between 2 colores rgba
  '''
  rgb1 = color1[0:3]
  alpha1 = color1[3:]
  color1hsv =  list(colorsys.rgb_to_hsv(rgb1[0],rgb1[1],rgb1[2]))+alpha1
  rgb2 = color2[0:3]
  alpha2 = color2[3:]
  color2hsv = list(colorsys.rgb_to_hsv(rgb2[0],rgb2[1],rgb2[2]))+alpha2  
  cl = []
  for c,d in zip(color1hsv,color2hsv):
    cl += [c*(end_value-value)+d*(value-start_value)/(end_value-start_value)]
  cl_rgb = colorsys.hsv_to_rgb(cl[0],cl[1],cl[2])
  return list(cl_rgb)+cl[3:]        

