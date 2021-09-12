import numpy as np
from skimage import io

def palette_to_colorsets(palette):
    color_sets = []
    for color in palette:
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        color_sets.append([r, g, b])
    return color_sets

def init_image(size=400):
    img = np.full((size, size, 3), 255).astype('uint8')
    return img


def address_split(address,split_size=4):
    hex = address[2:].lower()
    splits = []
    rect = []
    for idx, char in enumerate(hex):
        val = int(char, 16)
        if idx % split_size == 0:
            splits.append(rect)
            rect = []
        rect.append(val)
    splits.append(rect)
    splits = splits[1:]
    return splits


def distinct_color(c1,c2):
    if abs(c1 - c2) < 8:
        sep = 15 - (c1 + c2) / 2.
    else:
        sep = (c1 + c2) / 2.
    return sep

def h2x(h):
    return min(int(h*16),255)

def address_to_img_2(address):

    splits = address_split(address,10)
    squares = []
    sz = 40
    offset = 4
    ros = []
    gos = []
    bos = []
    for spl in splits:
        ro,go,bo,l,t,r,b,ri,gi,bi = spl
        print(ro,go,bo)
        ros.append(ro)
        gos.append(go)
        bos.append(bo)
        square = init_image(size=sz+1)
        square[:,:] = [h2x(ro),h2x(go),h2x(bo)]
        l = l+offset
        r = sz-r-offset
        t = t + offset
        b = sz-b-offset
        square[l:r+1,t:b+1] = [h2x(ri),h2x(gi),h2x(bi)]


        border_color = []
        for co,ci in [[ro,ri],[go,gi],[bo,bi]]:
            sep=distinct_color(co,ci)
            border_color.append(h2x(sep))
        print("border color",border_color)
        border_color = [255,255,255]
        square[l-1:r+1+1,t-1] = border_color
        square[l-1:r+1+1,b+1] = border_color
        square[l-1,t-1:b+1] = border_color
        square[r+1,t-1:b+1] = border_color


        squares.append(square)



    sep_colors = [255, 255, 255]
    sep_width = 1
    print("sep_colors",sep_colors)
    vbord = np.full((len(square),sep_width,3),sep_colors,dtype='uint8')
    hbord = np.full((sep_width,len(square)*2+sep_width,3), sep_colors,dtype='uint8')

    print(squares[0].shape, vbord.shape)

    img_top = np.hstack((squares[0],vbord,squares[1]))
    img_bottom = np.hstack((squares[2],vbord,squares[3]))
    img = np.vstack((img_top,hbord,img_bottom))
    io.imsave('data/' + address + '.png', img, check_contrast=False)




def address_to_img(address, palette):

    color_sets = palette_to_colorsets(palette)

    size = 400
    img = init_image(size)
    sz = size/20

    rectangles = address_split(address)

    prevleft = 0
    prevtop = 0
    prevright = size
    prevbottom = size

    for idx, rect in enumerate(rectangles):
        offset = int(idx*sz)
        color_idx = idx % len(color_sets)
        color = color_sets[color_idx]
        # color = idx*25
        # print(color)
        # left = rect[0]+offset
        # top = rect[1]+offset
        # right = size-rect[2]-offset
        # bottom = size-rect[3]-offset

        left = prevleft+rect[0]+4
        top = prevtop+rect[1]+4
        right = prevright-rect[2]-4
        bottom = prevbottom-rect[3]-4

        prevleft = left
        prevtop = top
        prevright = right
        prevbottom = bottom

        print(left,top,right,bottom, 'sizes', right-left, bottom-top)

        img[left:right,top:bottom] = color

    # print(img[100:120,100:120])
        # for x in range(left,right):
        #     for y in range(top,bottom):
        #         img[x,y,0] = 0





    io.imsave('data/'+address+'.png',img,check_contrast=False)

# address = "0xd603a49886c9B500f96C0d798aed10068D73bF7C"
address = "0x641c2fef13fb417db01ef955a54904a6400f8b07"
# address = "0x0000000000000000000000000000000000000000"
# address = "0xffffffffffffffffffffffffffffffffffffffff"
address = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
address = "0x6f69f79cea418024b9e0acfd18bd8de26f9bbe39" #cap
address = "0x032b7d93aeed91127baa55ad570d88fd2f15d589" #hodl
address = "0x6867115787080d4e95cbcb6471fa85a9458a5e43" #subvert
address = "0x000000000000000000000000000000000000dead"

palette = ['E7F2F8','74BDCB','FFA384','EFE7BC']
address_to_img_2(address)