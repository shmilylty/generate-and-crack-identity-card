#!/usr/bin/env python
# coding=utf-8
# author:4ido10n[@gmail.com]
# license:GPL v3
# blog:hackfun.org

import sys
import os
import datetime
import time
import urllib2
import json
import requests
from divison_code import divison_codes

current_date = datetime.datetime.now().strftime('%Y%m%d')
current_year = datetime.datetime.now().year
appkey = ['db6fb1f5ae343974296cece35e047218', '6d21a53c6bf995e82980c731e32af339','bbefe459287faab66731a970d9c85328', 
          'bf3dc06b9c1f1fce3c7fddf88be8ebee', 'eddcee3a76d0e5e267044bafbc5b393a', '16285d8106d1500ba77f8473dab75213']
fail_code = {
    11: '参数不正确',
    12: '商户余额不足',
    13: 'appkey不存在',
    14: 'IP被拒绝',
    20: '身份证中心维护中'
}
success_code = {
    1: '一致',
    2: '不一致',
    3: '无此身份证号码'
}


def find_ID_card(name):
    print('[~] The program is cracking the ID card number.')
    with open('probable_ID_card.txt', 'r') as card_file:
        for line in card_file:
            cardno = line[0:18]
            time.sleep(0.2)
            data = {
                'cardno': cardno,
                'name': name,
                'appkey': appkey[0]
            }
            url = 'http://api.id98.cn/api/idcard'
            request = requests.get(url, params=data)
            json_data = request.json()
            if json_data['isok'] == 0:
                print(fail_code[json_data['code']])
                exit(1)
            with open('query.log', 'a') as log_file:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log = current_time + '  ' + request.url + '  ' + cardno + \
                    '  ' + name + '  ' + success_code[json_data['code']]
                log_file.write(log)
            if json_data['isok'] == 1:
                print(
                    '[>] The program has found the id number successfully -> name:%s ID card number:%s') % (name, cardno)
                exit(0)


def generate_ID_card(divison_code, bithday, name, sex):
    print('[~] The program is creating the ID card number.')
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
            probable_ID_number = ID_card_base + check_code + '  '
            sex = '  男  '
            age = str(current_year - int(bithday[0:4])) + '  '
            province = divison_codes[divison_code[0:2] + '0000']
            city = divison_codes[divison_code[0:4] + '00']
            county = divison_codes[divison_code]
            address = province + ' ' + city + ' ' + county + ' '
            probable_ID_info = probable_ID_number + name + sex + age + address + '\n'
            probable_ID_infos += probable_ID_info
        with open('probable_ID_card.txt', 'w') as card_file:
            card_file.write(probable_ID_infos)
            card_file.close
        print('[~] The program has generated all ID numbers.')
        print('[>] Generated  ID card file: probable_ID_card.txt')
    elif sex == 'woman':
        for sequence_code in xrange(0, 1000, 2):
            ID_card_base = divison_code + bithday + str(sequence_code).zfill(3)
            checksum = 0
            for i in xrange(len(ID_card_base)):
                checksum += int(ID_card_base[i]) * factor[i]
            mod = checksum % 11
            check_code = verify_number_list[mod]
            probable_ID_number = ID_card_base + check_code + '  '
            sex = '  女  '
            age = str(current_year - int(bithday[0:4])) + '  '
            province = divison_codes[divison_code[0:2] + '0000']
            city = divison_codes[divison_code[0:4] + '00']
            county = divison_codes[divison_code]
            address = province + '  ' + city + '  ' + county + '  '
            probable_ID_info = probable_ID_number + name + sex + age + address + '\n'
            probable_ID_infos += probable_ID_info
        with open('probable_ID_card.txt', 'w') as card_file:
            card_file.write(probable_ID_infos)
            card_file.close
        print('[>] The program has generated all ID numbers -> probable_ID_card.txt')
    else:
        print('[!] Sex is invalid.')
        exit(1)


def sex_check(sex):
    if sex.isalpha() is False:
        print('[!] Please input "man" or "woman".')
        exit(1)
    if sex not in ['man', 'woman']:
        print('[!] Please input "man" or "woman".')
        exit(1)
    checked_sex = sex
    return checked_sex


def name_check(name):
    for char in name.decode('utf-8'):
        if char < u'\u4e00' or char > u'\u9fa5':
            print('[!] Please input "valid" name.')
            exit(1)
    check_name = name
    return check_name


def bithday_check(bithday):
    if bithday.isdigit() is False:
        print('[!] Please input eight "digits" bithday.')
        exit(1)
    if len(bithday) != 8:
        print('[!] Please input "eight" digits bithday.')
        exit(1)
    year = int(bithday[0:4])
    month = int(bithday[4:6])
    day = int(bithday[6:8])
    if year not in xrange(1984, current_year + 1):
        print('[!] Please valid "year".')
        exit(1)
    if month not in xrange(1, 13):
        print('[!] Please valid "month".')
        exit(1)
    if day not in xrange(1, 32):
        print('[!] Please valid "day".')
        exit(1)
    if int(bithday) > int(current_date):
        print('[!] Please input valid "bithday".')
        exit(1)
    valid_bithday = bithday
    return valid_bithday


def divison_code_check(divison_code):
    if divison_code.isdigit() is False:
        print('[!] Please input six "digits" administrative division code.')
        exit(1)
    if len(divison_code) != 6:
        print('[!] Please input "six" digits administrative division code.')
        exit(1)
    if divison_code not in divison_codes:
        print('[!] Please input "valid" six digits administrative division code.')
        exit(1)
    valid_divison_code = divison_code
    return valid_divison_code


def get_input():
    divison_code = raw_input('[*] Input administrative division codes:')
    divison_code = divison_code_check(divison_code)
    bithday = raw_input('[*] Input bithday:')
    bithday = bithday_check(bithday)
    name = raw_input('[*] Input name:')
    name = name_check(name)
    sex = raw_input('[*] Input sex (man or woman):')
    sex = sex_check(sex)
    return divison_code, bithday, name, sex


def set_coding():
    encoding = 'utf-8'
    if sys.getdefaultencoding() != encoding:
        reload(sys)
        sys.setdefaultencoding(encoding)


def main():
    set_coding()
    divison_code, bithday, name, sex = get_input()
    generate_ID_card(divison_code, bithday, name, sex)
    find_ID_card(name)

if __name__ == '__main__':
    main()
