from PIL import ImageDraw, Image, ImageFont
import numpy as np
from random import randint


def lst_generator(img):
    data = img.getdata()
    lst = []
    for tups in data:
        for nums in tups:
            if nums == 255:
                lst.append(nums)
            elif nums < 255:
                nums = randint(0,100)
                lst.append(nums)
    return lst


def img_resize(ran_gen_img):
    height,width = ran_gen_img.size
    return (int(height*2.75),int(width*2.75))


img = Image.open('dog1.png')
new_data = lst_generator(img)
ran_array = np.asarray(new_data, dtype='uint8').reshape((213,241,4))
ran_img = Image.fromarray(ran_array)
ran_img.save('ran_gen_color.png')
#####above rgb random value generator#####

ran_gen_img = Image.open('ran_gen_color.png')
orig_img = Image.open('dog1.png')
resized_nums = img_resize(ran_gen_img)
resized_img = ran_gen_img.resize((resized_nums[0],resized_nums[1]))
orig_resized = orig_img.resize((int(resized_nums[0]//3.5),int(resized_nums[1]//3.5)))
resized_img.paste(orig_resized, (0,resized_nums[1]-orig_resized.size[1]))
resized_img.save('resized_and_pasted.png')
for_font_img = Image.open('resized_and_pasted.png')
draw = ImageDraw.Draw(for_font_img)
font = ImageFont.truetype(font=r'c:\windows\fonts\BRADHITC.TTF',size=25)
draw.text((25,0),'Jdubz_Anon',fill=128,font=font)
for_font_img.save('finished_final_image.png')
