filename = 'colors.txt'
f = open(filename, 'r')
s = f.readline() #desecha la primera linea
color_dict = {}
while not s == '':
  s = f.readline()
  if s == '': break
  if s[0] != '#':
    line_list = [i for i in s.split(',')]
    name = line_list[0]
    r = int(line_list[1])
    g = int(line_list[2])
    b = int(line_list[3])
    color_dict[name] = [r,g,b]

color_dark_wall = color_dict['color_darkbrick']
color_light_wall = color_dict['color_brick']
color_dark_ground = color_dict['color_darkdust']
color_light_ground = color_dict['color_dust']
color_player = color_dict['color_flesh']
color_npc = color_dict['color_darkflesh']
color_white = color_dict['color_white']
color_black = color_dict['color_black']

filename = 'colors_kivy.def'
seq = ''
for name in color_dict:
  r = float(color_dict[name][0]/255.0)
  g = float(color_dict[name][1]/255.0)
  b = float(color_dict[name][2]/255.0)
  a = float(1)
  seq += name + ',' + str(r) + ',' + str(g) + ',' + str(b) + ',' + str(a) + '\n'    
with open(filename,'w') as f: 
  f.write(seq)