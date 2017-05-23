
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
  ordn = 0
  sprite_width = int(width / cols)
  sprite_height = int(height / rows)
  text = '{ \n'
  text += '  "' + imagefile + '": {\n'
  for row in range(rows):
    for col in range(cols):
      #if ordn < 32 or (ordn > 126 and ordn < 161):
      text += '    "x' + str(ordn) + '": [' + str(col*sprite_width) + ',' + str((height-((row+1)*sprite_height))) + ',' + str(sprite_width) + ',' + str(sprite_height) + ']'
      #else:
      #  text += '    "' + chr(ordn) + '": [' + str(col*sprite_width + 1) + ',' + str((height-((row+1)*sprite_height)) + 1) + ',' + str(sprite_width) + ',' + str(sprite_height) + ']'
      if row==rows-1 and col==cols-1:
        text += '\n' 
      else:
        text += ',\n' 
      ordn += 1
  text += "  } \n}"
  
  filename = imagefile[:-4] + ".atlas"
  write_atlas(filename,text)
  
make_atlas('roguelike16x16_gs_ro.png',256,256,16,16)