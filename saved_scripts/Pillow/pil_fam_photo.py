from PIL import Image, ImageFilter
from PIL.ImageFilter import CONTOUR, EDGE_ENHANCE

img1 = Image.open('taryn.jpeg')
img2 = Image.open('ben_n_jw.jpeg')
img1.resize((200,200))
img2.resize((200,200))
new_img = Image.new('RGB', (2 * img1.size[0],img1.size[1]))
new_img.paste(img1)
new_img.paste(img2,(img1.size[0],0))
another_img = new_img.filter(CONTOUR).filter(EDGE_ENHANCE)

#new_img.save('family_photo.jpeg')
another_img.save('another_image.jpeg')
another_img.show()



###########using Numpy arrays#####
from PIL import Image
import numpy as np
img = Image.open('img.png').resize((600,500))
arrays = np.asarray(img)
new_array = arrays.clip(min=None,max=100)
new_img = Image.fromarray(new_array)
new_img.save('array_image.jpeg')
new_img.show()
##########alpha_composite######
from PIL import Image

img = Image.open('taryn.jpeg').convert('RGBA')
img1 = Image.open('img.png').convert('RGBA').resize(img.size)
#print(img1.mode,img.mode)
img.alpha_composite(img1, dest=(300,300), source=(300,300))
img.show()
##########convert to 'p', palatte adaptive and croping######
from PIL import Image

img = Image.open('taryn.jpeg').convert('P', palette=1, colors=20)
img1 = Image.open('img.png').convert('RGBA').resize(img.size)

width,height = img.size

crop_img = img.crop((200,170,500,800))
crop_img.save('taryn_crp.png')

#####created a family photo using paste method and above code for image processing######
from PIL import Image

img = Image.open('taryn.jpeg').convert('P', palette=1, colors=20).resize((350,650))
img1 = Image.open('ben_n_jw.jpeg').convert('P', palette=1, colors=15).resize((600,600))
crop_img = img.crop((80,60,220,650))
crop_img.save('taryn_crp.png')
taryn = Image.open('taryn_crp.png').resize((140,490))
img1.paste(taryn, (50,50))
img1.save('blended_family.png')
img1.show()
