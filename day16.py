from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *
from numpy import product, array
import re
import sys
from timeit import default_timer as timer

version_sum = 0

def get_value(index, inp, v, t, in_operator):
    start = index - 6
    val = ''
    done = False
    while not done:
        done = True if inp[index:index+1] == '0' else False
        val += inp[index+1:index+5]
        index += 5
    val = int(val, 2)
    if not in_operator:
        index += 4 - (index - start) % 4
    return index, {'val': [val], 'v': v, 't': t}


def get_operator(index, inp, v, t):
    length_id = inp[index]
    vals = []
    if length_id == '0':
        subpacket_end = int(inp[index+1:index+16], 2) + index + 16
        index += 16
        while index < subpacket_end:
            index, val = get_packet(index, inp, True)
            vals.append(val)
    else:
        subpackets = int(inp[index+1:index+12], 2)
        index += 12
        for i in range(subpackets):
            index, val = get_packet(index, inp, True)
            vals.append(val)
    return index, {'val': vals, 'v': v, 't': t}


def get_packet(index, inp, in_operator):
    global version_sum

    if index > (len(inp) - 5) or int(inp[index:], 2) == 0:
        index = len(inp)
        return index, None

    # packet
    v = int(inp[index:index+3], 2)
    index += 3
    version_sum += v

    # type
    t = int(inp[index:index+3], 2)
    index += 3

    # literal value
    if t == 4:
        return get_value(index, inp, v, t, in_operator)
    else:
        return get_operator(index, inp, v, t)


def evaluate(packet):
    type = packet['t']
    if type == 0:
        return sum([evaluate(p) for p in packet['val']])
    if type == 1:
        res = evaluate(packet['val'][0])
        if len(packet['val']) == 1:
            return res
        else:
            for v in [evaluate(p) for p in packet['val'][1:]]:
                res *= v
            return res
    if type == 2:
        return min([evaluate(p) for p in packet['val']])
    if type == 3:
        return max([evaluate(p) for p in packet['val']])
    if type == 4:
        return packet['val'][0]
    if type == 5:
        return 1 if evaluate(packet['val'][0]) > evaluate(packet['val'][1]) else 0
    if type == 6:
        return 1 if evaluate(packet['val'][0]) < evaluate(packet['val'][1]) else 0
    if type == 7:
        return 1 if evaluate(packet['val'][0]) == evaluate(packet['val'][1]) else 0


def main(inp, is_real):
    global version_sum
    version_sum = 0
    h = inp.strip()
    inp = bin(int(h, 16))[2:].zfill(len(h) * 4)
    index = 0
    index, packet = get_packet(index, inp, False)
    print(evaluate(packet))
    print(f'sum: {version_sum}')


sample_input = r"""
9C0141080250320F1802104A08
"""

real_input = r"""
6051639005B56008C1D9BB3CC9DAD5BE97A4A9104700AE76E672DC95AAE91425EF6AD8BA5591C00F92073004AC0171007E0BC248BE0008645982B1CA680A7A0CC60096802723C94C265E5B9699E7E94D6070C016958F99AC015100760B45884600087C6E88B091C014959C83E740440209FC89C2896A50765A59CE299F3640D300827902547661964D2239180393AF92A8B28F4401BCC8ED52C01591D7E9D2591D7E9D273005A5D127C99802C095B044D5A19A73DC0E9C553004F000DE953588129E372008F2C0169FDB44FA6C9219803E00085C378891F00010E8FF1AE398803D1BE25C743005A6477801F59CC4FA1F3989F420C0149ED9CF006A000084C5386D1F4401F87310E313804D33B4095AFBED32ABF2CA28007DC9D3D713300524BCA940097CA8A4AF9F4C00F9B6D00088654867A7BC8BCA4829402F9D6895B2E4DF7E373189D9BE6BF86B200B7E3C68021331CD4AE6639A974232008E663C3FE00A4E0949124ED69087A848002749002151561F45B3007218C7A8FE600FC228D50B8C01097EEDD7001CF9DE5C0E62DEB089805330ED30CD3C0D3A3F367A40147E8023221F221531C9681100C717002100B36002A19809D15003900892601F950073630024805F400150D400A70028C00F5002C00252600698400A700326C0E44590039687B313BF669F35C9EF974396EF0A647533F2011B340151007637C46860200D43085712A7E4FE60086003E5234B5A56129C91FC93F1802F12EC01292BD754BCED27B92BD754BCED27B100264C4C40109D578CA600AC9AB5802B238E67495391D5CFC402E8B325C1E86F266F250B77ECC600BE006EE00085C7E8DF044001088E31420BCB08A003A72BF87D7A36C994CE76545030047801539F649BF4DEA52CBCA00B4EF3DE9B9CFEE379F14608
"""


if len(sample_input.strip()) > 0:
    print("sample:")
    start = timer()
    main(sample_input, False)
    end = timer()
    print(f'sample: {(end-start)*1000_000:.0f}μs ({(end-start)*1000:.0f}ms)')


print("real:")
start = timer()
main(real_input, True)
end = timer()
print(f'sample: {(end-start)*1000_000:.0f}μs ({(end-start)*1000:.0f}ms)')
