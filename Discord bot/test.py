import rune_interpreter as ri
import os

def getimage():
    primary = 'Inspiration'
    # primary = list[0][0]
    # secondary = list[0][1]
    # name = "glacial_augment"
    # for filename in listdir(f'./runes/{rune_convertor(primary)}'):
    #     if filename[:-4] == name:
    #         print (filename)
    print (ri.rune_convertor(primary))

getimage()
