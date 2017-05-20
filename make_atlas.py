
'''
make Atlas. Define un nuevo archivo atlas dada la imagen, las dimensiones y el numero de 
sprites en forma matricial
'''

def write_atlas(file_path, text):
  '''
  Write the atlas file.
  '''
  with open(file_path,"w",encoding="utf8") as current_file:
    current_file.write(text)

def make_atlas(imagefile, width, height, rows,cols):
  ord = 0
  sprite_width = int(width / cols)
  sprite_height = int(height / rows)
  text = '{ \n'
  text += '  "' + imagefile + '": {\n'
  for row in range(rows):
    for col in range(cols):
      #if ord<32 or (ord>126 and ord < 161): 
      text += '    "x' + str(ord) + '": [' + str(col*sprite_width + 1) + ',' + str(row*sprite_height + 1) + ',' + str(sprite_width) + ',' + str(sprite_height) + '], \n' 
      #else:
      #  text += '    "' + chr(ord) + '": [' + str(col*sprite_width + 1) + ',' + str(row*sprite_height + 1) + ',' + str(sprite_width) + ',' + str(sprite_height) + '], \n' 
      ord += 1
  text += "  } \n}"
  
  filename = imagefile[:-4] + ".atlas"
  write_atlas(filename,text)
  
make_atlas('roguelike16x16_gs_ro.png',256,256,16,16)