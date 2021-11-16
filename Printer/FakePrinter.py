#!/usr/bin/env python
from __future__ import print_function
import socket
import sys
import DataConverter
import Label


def print_help():
    help = """
usage: python FakePrinter.py [OPTIONS]

---------------------------------------------------
[OPTIONS]
---------------------------------------------------
    
    -h    help         prints help and exits
    -o    output       folder to write the file to
    -p    port         port to listen to
    -i    interface    interface to listen to
    -n    project_name name of folder to save to 
    """
    print(help)


def main():
    output = './data/'
    port = 9100
    interface = '0.0.0.0'  # listen on all interfaces
    preserve_label = False

    if '-h' in sys.argv:
        print_help()
        exit()
    if '-o' in sys.argv:
        output = sys.argv[sys.argv.index('-o') + 1]
        print('setting output    to: %s' % output)
    if '-p' in sys.argv:
        port = str(sys.argv[sys.argv.index('-p') + 1])
        print('setting port      to: %s' % port)
    if '-i' in sys.argv:
        interface = sys.argv[sys.argv.index('-i') + 1]
        print('setting interface to: %s' % port)
    if '-n' in sys.argv:
        project_name = sys.argv[sys.argv.index('-n') + 1]
        output += project_name
        print('setting project name to: %s' % project_name)
    if '--preserve-label' in sys.argv:
        preserve_label = True
    else:
        print('WARNING: automatic parameter detection is still under testing')

    print(f"listening on {interface}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((interface, port))

        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                # noinspection PyStringFormat
                print("connection made by: %s:%d" % addr)

                data = b''
                while True:
                    new_data = conn.recv(512)
                    data += new_data
                    if not new_data:
                        break

                converted = DataConverter.convert_data(data, preserve_label=preserve_label)
                for x in converted:
                    Label.save(x, path=output)

                if isinstance(converted[0], Label.Label):
                    break

if __name__ == '__main__':
    sys.argv.append('--preserve-label option')
    main()
