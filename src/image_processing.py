'''
Change log:
    1. changed description for method set_image in class MyImage
    2. clarified task - can change the class location in the Skeleton

'''
import matplotlib.pyplot as plt
from typing import TypeVar  # can add whatever you like
import numpy as np
import matplotlib.image as mpimg
import imageio as im

chooseReturn = TypeVar('T')


# Use the following as a Skeleton

class MyImage(object):
    def __init__(self, image_name):
        self.address = image_name
        self.img_array = im.v2.imread(self.address)
        self.image = im.imwrite(self.address, self.img_array)

    def set_image(self, image_name: str) -> None:
        self.address = image_name
        self.img_array = im.v2.imread(self.address)
        self.image = im.imwrite(self.address, self.img_array)

    def get_image(self) -> None:
        self.image = im.v2.imread(self.address)
        plt.imshow(self.image)
        plt.show()
    def get_array(self):
        return self.img_array


class MyImageTHN(MyImage):
    def change_TH_num(self, num: int) -> None:
        new_mat = np.zeros(self.img_array.shape, dtype = int)
        new_mat[self.img_array < num] = 0
        new_mat[self.img_array>=num] = 255
        self.img_array = new_mat
        self.image = im.imwrite(self.address, self.img_array)
        return None


class MyImageTHP(MyImage):

    def change_TH_per(self, per: int) -> None:
        new_mat = np.zeros(self.img_array.shape, dtype=int)
        new_mat[self.img_array < per] = 0
        new_mat[self.img_array/255*100 >= per] = 255
        self.img_array = new_mat
        self.image = im.imwrite(self.address, self.img_array)
        return None


class MyImagePolar(MyImage):

    def change_polar(self, pol_num: int) -> chooseReturn:
        if pol_num == 1:
            gradient = np.linspace(0, 255, 256)
            image = np.tile(gradient, (256, 1))
            inverted_image = 255 - image
            return image


m1 = MyImagePolar('newest.png')
m1.get_image()
new_image = m1.change_polar(1)
plt.imshow(new_image)
plt.show()
