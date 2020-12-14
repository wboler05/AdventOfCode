#!/usr/bin/env python3

import argparse, os, sys
import numpy as np
import re

import tqdm

def recurse(mask, prefix, addr_bits):
    
    if len(mask) == 0:
        return [ prefix, ]
    r = ""
    idx = 0
    for s,a in zip(mask, addr_bits):
        if s == 'X':
            left = r + '1'
            right = r + '0'
            return \
                recurse(mask[idx+1:], prefix + left, addr_bits[idx+1:]) + \
                recurse(mask[idx+1:], prefix + right, addr_bits[idx+1:])
        else:
            if s == '0':
                r += a
            else:
                r += s
            idx += 1
    return [ prefix + r, ]

def generate_address_from_mask(mask, addr):
    addr_bits = "{0:036b}".format(addr)
    address_list = recurse(mask, "", addr_bits)
    r = [ int(a, 2) for a in address_list]
    return r

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
    

    '''
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
    '''

    mask = None
    mem = {}
    #print("Memory Size: {}".format(mem.shape))
    max_address = 0
    for instruction in tqdm.tqdm(instruction_list):
        print(instruction)
        if 'mask' in instruction:
            mask = instruction['mask']
        if 'address' in instruction:
            address_list = generate_address_from_mask(mask, instruction['address'])
            #print("Address List: {}".format(address_list))
            for a in address_list:
                mem[a] = instruction['value']
    #print("Max Address: {}".format(max_address))

    #for i,m in enumerate(mem):
    #    if m > 0:
    #        print("mem[{}] = {}".format(i,m))

    memory_sum = sum(mem.values())
    print("Memory Sum: {}".format(memory_sum))

if __name__ == '__main__':
    main()