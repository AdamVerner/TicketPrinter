#!/usr/bin/env python
"""

"""
import os
import re
from TesterController.Libs.utils import dynamic_path

default_path = dynamic_path('./data/', __file__)


def get_available_names(path=default_path):
    folders = os.listdir(path)

    isdir = lambda d: os.path.isdir(path + d)
    has_label = lambda d: os.path.exists(path + d + '/label.template')

    folders = filter(isdir, folders)
    folders = filter(has_label, folders)

    return folders


def save(obj, path=default_path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if isinstance(obj, Image):
        with open(path + obj.name + '.bmp', 'wb') as f:
            print('saving to : %s' % path + obj.name + '.bmp')
            f.write(obj.data)
    elif isinstance(obj, Label):
        if obj.images_uploaded:
            for image in obj.images:
                save(image, obj.path)
        else:
            with open(path + 'label.template', 'wb') as f:
                f.write(obj.raw_zpl)


class Label(object):

    template = ''
    images_uploaded = False

    def __init__(self, name=None, zpl=None, images=None, path=default_path):
        """
        priorities when loading:
            1. zpl
            2. name

        :param name: where to look for label
        :param zpl: source code
        :param path: path to save to / look for
        """

        self.images = []
        self.params = {}

        if not name and not zpl:
            raise TypeError('neither name nor source was specified')

        # preserve type
        if not name:
            name = ''

        self.path = path + '/' +  name + '/'
        self.name = name

        if zpl:
            self.zpl = zpl
        else:
            with open(self.path + 'label.template', 'r') as tmplt:
                self.zpl = tmplt.read()

        # verify that correct line feeding is used
        if '\r\n' not in self.zpl:
            self.zpl = self.zpl.replace('\n', '\r\n')

        # make sure there is empty line on the end
        if self.zpl[-2:] is not '\r\n':
            self.zpl += '\r\n'

        for param in re.findall(r'{([^\s]*)}', self.zpl):
            self.params[param] = ''
        if not zpl:
            self.load_images()

        if images:
            self.images = images

    def shape(self):
        """
        returns shape of label in format (width, height)
        """
        re_h = r'\^Q([0-9,]*)'
        re_w = r'\^W([0-9,]*)'

        height = re.findall(re_h, self.raw_zpl)[0]
        width = re.findall(re_w, self.raw_zpl)[0]

        return width, height

    def load_images(self):
        files = os.listdir(self.path)

        is_bmp = lambda img: img[-4:].lower() == '.bmp'
        bmps = filter(is_bmp, files)

        # remove file type
        for bmp in bmps:
            with open(self.path + bmp, 'rb') as f:
                self.images.append(Image(bmp[:-4], f.read()))

    def set_param(self, param, value):
        # type: (str, str)-> None
        print('setting param to %s' % param)
        print('value' + value)
        if param not in self.params.keys():
            raise ValueError('param is not in list of available params')

        self.params[param] = value

    def has_param(self, param):
        return param in self.params.keys()
    
    @property
    def zpl(self):
        data = self.raw_zpl
        for param in self.params.keys():
            replaceable = '{' + param + '}'
            data = data.replace(replaceable, self.params[param])
        return data

    @zpl.setter
    def zpl(self, value):
        self.raw_zpl = value

    def set_image(self, param, image):
        # type: (str, bytes)-> None
        self.images.append(Image(param, image))
        pass


class Image(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data


def main():
    pass


if __name__ == '__main__':
    main()
