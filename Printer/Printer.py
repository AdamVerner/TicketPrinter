#!/usr/bin/env python
"""


ZPL docs can be found at https://support.zebra.com/cpws/docs/zpl/zpl_manual.pdf
EZPL docs https://www.mediaform.de/fileadmin/support/handbuecher/etikettendrucker/godex/God_EZPL_PM.pdf

both should be valid, but EZPL doc should be more valid


"""

import socket
import logging
import sys
from Label import Label, Image


class Printer(object):

    data_path = './data/'  # must end with '/'

    def __init__(self, printer_ip, printer_port=9100):
        # type: (str, int) -> None

        self.log = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        logging.debug('printer ip   = %s', printer_ip)
        logging.debug('printer port = %d', printer_port)

        self.ip = printer_ip
        self.port = printer_port

    def send(self, label: Label):
        """
        if you're uploading label with an image, make sure, that you've uploaded the image first
        """
        self.log.debug('sending message to : %s:%s. msh = %s', self.ip, self.port, repr(label.zpl))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((self.ip, self.port))
        s.send(label.zpl.encode('utf-8'))
        s.close()

    def upload_image(self, image):
        # type: (Image) -> None
        """
        """

        b = f'\r\n\r\n~MDELG,{image.name}\r\n~EB,{image.name},{len(image.data)}\r\n'.encode('utf-8')
        b += image.data
        b += b'\r\n'

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((self.ip, self.port))
        s.send(b)
        s.close()

    def print_(self, label: Label):
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
    if len(sys.argv) != 3:
        print(f"Usage is ./{sys.argv[0]} PRINTER_HOST LABEL_PATH")
        return 1

    p = Printer(sys.argv[1])
    l = Label(name=sys.argv[2])

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
