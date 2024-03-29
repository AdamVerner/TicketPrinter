#!/usr/bin/env python
"""

"""
import os
import re
from pathlib import Path

default_path = './data/'


def get_available_names(path=default_path):
    folders = os.listdir(path)

    isdir = lambda d: os.path.isdir(path + d)
    has_label = lambda d: os.path.exists(path + d + '/label.template')

    folders = filter(isdir, folders)
    folders = filter(has_label, folders)

    return folders


def save(obj, path=default_path):
    Path(path).mkdir(parents=True, exist_ok=True)

    if isinstance(obj, Image):
        print(f'saving {os.path.join(path, obj.name + ".bmp")}')
        with open(os.path.join(path, obj.name + ".bmp") , 'wb') as f:
            f.write(obj.data)

    elif isinstance(obj, Label):
        if obj.images_uploaded:
            for image in obj.images:
                save(image, obj.path)

        else:
            print(f'saving {os.path.join(path, "label.template")}')
            with open(os.path.join(path, "label.template"), 'w') as f:
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

        self.path = os.path.join(path, name)
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
        if self.zpl[-2:] != '\r\n':
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
        if param not in self.params.keys():
            raise ValueError('param is not in list of available params')

        self.params[param] = value


    def has_param(self, param):
        return param in self.params.keys()

    @property
    def zpl(self) -> str:
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
