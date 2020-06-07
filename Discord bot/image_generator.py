import os
from rune_interpreter import rune_convertor
from PIL import Image, ImageDraw, ImageFont
import requests
import io



def get_rune_list(list):
    image_list = [[], [], [], []]
    primary = list[0][0]
    secondary = list[0][1]
    image_list[0].append(f'./runes/{rune_convertor(primary)}/{rune_convertor(primary)}.png')
    image_list[0].append(f'./runes/{rune_convertor(secondary)}/{rune_convertor(secondary)}.png')


    #KEYSTONE
    for keystone in os.listdir(f'./runes/{rune_convertor(primary)}/keystones'):
        if keystone[:-4] == rune_convertor(list[1][0]):
            image_list[1].append(f'./runes/{rune_convertor(primary)}/keystones/{keystone}')
            break

    # PRIMARY
    for i in range(1, 4):
        for rune in os.listdir(f'./runes/{rune_convertor(primary)}/tiers'):
            if rune[:-4] == rune_convertor(list[1][i]):
                image_list[1].append(f'./runes/{rune_convertor(primary)}/tiers/{rune}')
                break

    # SECONDARY
    for rune_name in list[2]:
        for rune in os.listdir(f'./runes/{rune_convertor(secondary)}/tiers'):
            if rune[:-4] == rune_convertor(rune_name):
                image_list[2].append(f'./runes/{rune_convertor(secondary)}/tiers/{rune}')
                break

    for bonus in list[3]:
        image_list[3].append(bonus)

    return image_list

def generate_image(images):
    bg = (255, 0, 0, 0)
    size = (400, 600)

    header_size = 80
    keystone_size = 140
    rune_size = 90
    bonus_size = 50

    image = Image.new('RGBA', size, bg)

    #print (images)

    primary = Image.open(images[0][0])
    keystone = Image.open(images[1][0])
    rune11 = Image.open(images[1][1])
    rune12 = Image.open(images[1][2])
    rune13 = Image.open(images[1][3])

    secondary = Image.open(images[0][1])
    rune21 = Image.open(images[2][0])
    rune22 = Image.open(images[2][1])

    response = requests.get(images[3][0])
    bonus1 = Image.open(io.BytesIO(response.content))

    response = requests.get(images[3][1])
    bonus2 = Image.open(io.BytesIO(response.content))

    response = requests.get(images[3][2])
    bonus3 = Image.open(io.BytesIO(response.content))

    row_1 = 10
    row_2 = 110
    row_3 = 250
    row_4 = 360
    row_5 = 470

    primary = primary.resize((header_size, header_size))
    secondary = secondary.resize((header_size, header_size))

    keystone = keystone.resize((keystone_size, keystone_size))
    rune11 = rune11.resize((rune_size, rune_size))
    rune12 = rune12.resize((rune_size, rune_size))
    rune13 = rune13.resize((rune_size, rune_size))
    rune21 = rune21.resize((rune_size, rune_size))
    rune22 = rune22.resize((rune_size, rune_size))

    bonus1 = bonus1.resize((bonus_size, bonus_size))
    bonus2 = bonus2.resize((bonus_size, bonus_size))
    bonus3 = bonus3.resize((bonus_size, bonus_size))

    image.paste(primary, ((size[0]//2-header_size)//2, row_1))
    image.paste(keystone, ((size[0]//2-keystone_size)//2, row_2))
    image.paste(rune11, ((size[0]//2-rune_size)//2, row_3))
    image.paste(rune12, ((size[0]//2-rune_size)//2, row_4))
    image.paste(rune13, ((size[0]//2-rune_size)//2, row_5))

    image.paste(secondary, ((size[0]//2-header_size)//2+size[0]//2, row_1))
    image.paste(rune21, ((size[0]//2-rune_size)//2+size[0]//2, row_2+(keystone_size-rune_size)//2))
    image.paste(rune22, ((size[0]//2-rune_size)//2+size[0]//2, row_3))

    image.paste(bonus1, ((size[0]//2-bonus_size)//2+size[0]//2, row_4+(rune_size-bonus_size)//2))
    image.paste(bonus2, ((size[0]//2-bonus_size)//2+size[0]//2, (row_4+row_5)//2+(rune_size-bonus_size)//2))
    image.paste(bonus3, ((size[0]//2-bonus_size)//2+size[0]//2, row_5+(rune_size-bonus_size)//2))

    return image
