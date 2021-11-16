from __future__ import print_function
import re
from typing import List

from Label import Image, Label


def convert_data(data: bytes, preserve_label=False) -> list:
    images = get_images(data)
    if not images:
        data = data.decode('utf-8')
        if not preserve_label:
            data = convert_to_params(data)
        return [Label(zpl=data)]
    return images


def get_images(data: bytes) -> List[Image]:
    regex = rb'(~MDELG,(.*)\r\n~EB,\2,(\d+)\r\n)'
    ret = []

    headers = re.finditer(regex, data)
    starts = []
    stops = []
    lens = []
    names = []

    for match in headers:
        stops.append(match.end(0))
        starts.append(match.start(0))
        lens.append(int(match.group(3)))
        names.append(match.group(2))

    starts += [len(data)]

    for idx, itm in enumerate(stops):
        mg = data[itm: starts[idx + 1] - 2]
        print('len = %s, lens = %s' % (len(mg), lens[idx]))
        ret.append(Image(names[idx].decode('utf-8'), mg))

    return ret


def convert_to_params(data):

    regs = {
        'power_input': r'(\d\d0V ~ \d0Hz; \d\dA)',
        'power': r'(\d\d0V ~ \d\d?A \d0Hz)',
        'power_output': r'((?:max. \d{1,2}A \([\d ]*W\))|(?:max: [\d ]*W))',
        'mac': r'\b([a-fA-F0-9:]{12})\b',
        'made_in': r'(Czech Republic)',
        'ean': r'(8594185580331)',  # TODO
        'model': r'[Mm]odel:? (\d0\d[A-Z])',
        'type': r'(Modbus)',
        'device_name': r'((?:NETIO(?: 4\w?\w?\w?)?)|(?:COBRA\s\d0\d\w))',
        'version': r'(WiFi, FR)'
    }

    print('\nFOUND Following matches :')
    for name in regs.keys():

        replaceable = '{' + name + '}'

        match = re.findall(regs[name], data)
        if match:
            for m in match:
                data = data.replace(m, replaceable)
            print('\t', name, '\t', match)
    return data


