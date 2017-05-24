#Vector Functions 

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
  return direc