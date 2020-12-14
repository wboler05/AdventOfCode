#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    args = parser.parse_args()

    data = None
    with open(args.input_filename, 'r') as ifile:
        data = ifile.read().split('\n')
        data = [d for d in data if len(d) > 0]

    re_mask = r"^(?:mask = )(?P<mask>[X10]+)$"
    re_mem = r"^(?:mem\[(?P<address>[\d]+)\] = (?P<value>[\d]+))$"

    instruction_list = list()
    for d in data:
        m = re.search(re_mask, d)
        if m is not None:
            mask = m.group('mask')
            instruction_list.append({'mask':mask})
        else:
            m = re.search(re_mem, d)
            if m is not None:
                addr = int(m.group('address'))
                val = int(m.group('value'))
                instruction_list.append({'address': addr, 'value': val})
            else:
                print("Welp, don't know what you're looking for: {}".format(d), file=sys.stderr)
    

    def apply_mask(value, mask):
        bit_str = list('{0:036b}'.format(value))
        #print("Before: {}".format(bit_str))
        for i,bit in enumerate(mask):
            if bit == '1':
                bit_str[i] = '1'
            elif bit == '0':
                bit_str[i] = '0'
        #print("After: {}".format(bit_str))
        return int('0b' + ''.join(bit_str), 2)

    mask = None
    mem = np.zeros(2**16).astype(np.uint64)
    print("Memory Size: {}".format(mem.shape))
    max_address = 0
    for instruction in instruction_list:
        print(instruction)
        if 'mask' in instruction:
            mask = instruction['mask']
        if 'address' in instruction:
            mem[instruction['address']] = apply_mask(instruction['value'], mask)
    #print("Max Address: {}".format(max_address))

    #for i,m in enumerate(mem):
    #    if m > 0:
    #        print("mem[{}] = {}".format(i,m))

    memory_sum = sum(mem)
    print("Memory Sum: {}".format(memory_sum))

if __name__ == '__main__':
    main()