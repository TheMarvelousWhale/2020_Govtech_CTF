# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:18:23 2020

@author: hoang
"""

import pandas as pd

data_NEC = pd.read_csv("./nec_data.csv")

def pulse(data):
    """
    We read in salae data, then convert command field it into ascii
    NEC IR relies on the space between pulses to encode the bit
    They send data using burst of 562.5µs, followed by x ms space, which is extremely helpful for decoding
    There are 4 type of space
    1. 18.37microsec - this is for one pulse within the burst 
    2. 562 microsec - this is for bit 0
    3. 1.6875milisec - this is for bit 1
    4. 4.5 milisec - this is for the leading command

    Parameters
    ----------
    data : TYPE  data from salae 1.2.18, which has time stamp of each transition 
        DESCRIPTION.

    Returns
    -------
    None.

    """
    start = False
    add,cmd,count = b'',b'',0                          #we use count to extract only the command part (ignore first 16 address bits)
    for i in range(len(data)-1):
        #I have removed the part that process the address portion.
        #You can simply add it in using count < 16 in the appropriate space
        pulse= data.iloc[i+1,0]-data.iloc[i,0]
        if pulse < 20e-05:      #short pulse within the burst, ignore
            continue
        elif (pulse > 0.55e-3 and pulse < 1.68e-3):  #bit 0's space
            if start == True and count >=16:
                cmd += b'0'
            count += 1
        elif pulse > 1.68e-3 and pulse < 4.2e-3:     #bit 1's space
            if start == True and count >=16:
                cmd += b'1'
            count +=1 
        elif pulse > 4.2e-3 and pulse < 1:          #lead's space
            start = True
        else:
            if cmd != b'':                         #space between messages
                print(chr(int(cmd[0:8],2))+chr(int(cmd[8:16],2)),end='')
            add,cmd,count= b'',b'', 0
            start = False


# def int2bytes(i):
#     hex_string = '%x' % i
#     n = len(hex_string)
#     return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
        
# def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
#     n = int(bits, 2)
#     return int2bytes(n).decode(encoding, errors)
        
if __name__=="__main__":
    pulse(data_NEC.head(100000))