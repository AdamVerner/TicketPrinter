#!/usr/bin/env python
"""


ZPL docs can be found at https://support.zebra.com/cpws/docs/zpl/zpl_manual.pdf
EZPL docs https://www.mediaform.de/fileadmin/support/handbuecher/etikettendrucker/godex/God_EZPL_PM.pdf

both should be valid, but EZPL doc should be more valid


"""

import socket
import logging
import sys
import pprint
from . import Label


class Printer(object):

    data_path = './data/'  # must end with '/'
    pp=pprint.PrettyPrinter(2)

    def __init__(self, printer_ip, printer_port=9100):
        # type: (str, int) -> None

        self.log = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        logging.debug('printer ip   = %s', printer_ip)
        logging.debug('printer port = %d', printer_port)

        self.ip = printer_ip
        self.port = printer_port

    def send(self, label):
        # type: (Label.)-> None
        """
        if you're uploading label with an image, make sure, that you've uploaded the image first
        """
        self.log.debug('sending message to : %s:%s. msh = %s', self.ip, self.port, repr(label.zpl))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((self.ip, self.port))
        s.send(label.zpl.encode())
        s.close()

    def upload_image(self, image):
        # type: (Image) -> None
        """
        """

        b = bytes('\r\n\r\n~MDELG,{name}\r\n~EB,{name},{size}\r\n'.format(name=image.name, size=len(image.data)).encode())
        b += image.data
        b += b'\r\n'

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((self.ip, self.port))
        s.send(b)
        s.close()

    def print_(self, label):
        # type: (Label)-> None
        """
        prints provided label
        """
        for img in label.images:
            self.log.debug('uploading img %s', img.name)
            self.upload_image(img)
        self.send(label)


def print_help():
    help = """
usage: python Printer.py printer_ip label_name [OPTIONS] [PARAMS]

---------------------------------------------------
[OPTIONS]
---------------------------------------------------
    
    -h    help         prints this help and exits   
    -p    printer_port
    
---------------------------------------------------
[OPTIONS]
---------------------------------------------------
    use format --param-name value
    or         --param_name
    param names should be same as in label.template
    """
    print(help)


def main():
    logging.basicConfig(level=logging.DEBUG)

    p = Printer(sys.argv[1])
    l = Label.Label(name=sys.argv[2])

    del sys.argv[0:3]

    if '-h' in sys.argv or '--help' in sys.argv:
        print_help()
        exit()
    if '-p' in sys.argv:
        param_index = sys.argv.index('-p')
        p.port = sys.argv[param_index]
        print('setting port to %d' % p.port)

        del sys.argv[param_index]
        sys.argv.remove('-p')

    for idx, param in enumerate(sys.argv):
        if param[0:1] == '--':
            param_name = param[2:].replace('-', '_')
            print(param_name, sys.argv[idx+1])
            l.set_param(param_name, sys.argv[idx+1])

    p.print_(l)


if __name__ == '__main__':
    main()
