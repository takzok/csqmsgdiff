# -*- coding=utf-8 -*-

import codecs
import os
from os.path import abspath, join
import re
import warnings
import lxml.html

from tqdm import tqdm
from bs4 import BeautifulSoup
from collections import OrderedDict

def scrape_html(args):
    files = os.listdir(args.input_path)
    with tqdm(files, ncols=100) as pbar:
        for i, htmlfile in enumerate(pbar):
            pbar.set_postfix(OrderedDict(current=htmlfile))
            try:
                absolutepath = abspath(join(os.getcwd(), join(args.input_path, htmlfile)))
                f = open(absolutepath)
                src = f.read()
                f.close()
            except:
                print('file open error.')
                continue
            try:
                soup = BeautifulSoup(src.encode('utf-8'), 'lxml')
                parser_selector(soup, args.mq_version, args.output_path)
            except:
                import traceback
                traceback.print_exc()
        print('Complete.')

def parser_selector(soup, ver, path):
    if ver == '910':
        parse_mq_910(soup, ver, path)
    if ver == '900':
        parse_mq_900(soup, ver, path)
    if ver == '800':
        parse_mq_800(soup, ver, path)

def parse_mq_910(soup, ver, path):
    # html structure is same as V800 manual.
    parse_mq_800(soup, ver, path)

def parse_mq_900(soup, ver, path):
    # html structure is same as V800 manual.
    parse_mq_800(soup, ver, path)

def parse_mq_800(soup, ver, path):
    # build output file path & file open
    file_name = []
    file_name.append(path)
    file_name.append('/')
    # In version V9.0.0 MQ Service Provider message(CSQZ) is added.
    prefix = re.findall(
        r'(CSQ[BCEHIJMNOPQRTUVWXYZ012359]{1})', soup.find('title').text)
    file_name.append(prefix[0])
    file_name.append('.csv')
    try:
        f = codecs.open(''.join(file_name), 'w', 'utf-8')
        try:
            # write header infomation
            f.write('message: ' + soup.find('title').text + '\n')
            f.write('version: ' + ver + '\n')
            f.write("message ID,message" + '\n')
            # scraping html
            tag = soup.find_all(['dt', 'dd'])
            list = [""] * 2
            position = 0
            for i in tag:
                txt = i.get_text()
                if i.name == 'dt':
                    # scrape messageID
                    if re.search(r'(CSQ[BCEHIJMNOPQRTUVWXYZ012359]{1}[0-9]{3})', txt):
                        if list[0] != "":
                            # write message ID and message description and clear list when new message ID is comming.
                            f.write(','.join(list) + '\n')
                            list = [""] * 2
                        position = 1
                        list[0] = wrapper(txt)
                        continue
                    else:
                        position = -1
                        continue
                # scrape message description
                elif i.name == 'dd':
                    if position == 1:
                        txt = txt.strip()
                        list[position] = wrapper(format_message(txt))
                        continue
            # write last message ID and message description.
            f.write(','.join(list) + '\n')
        except IOError as e:
            print('Cannot open "{0}"'.format(''.join(file_name)))
            print(' e:[{0}]'.format(e))
        finally:
            f.close()
    except IOError as e:
        print('Cannot open "{0}"'.format(''.join(file_name)))
        print(' errNo.:{0} msg:{1}'.format(e.errno, e.strerror))

# deprecated (Documentation for MQ V7.1 and V7.0.1 has been removed from Knowledge center.)
def parse_mq_710(soup, ver, path):
    warn_msg = "`parse_mq_710` is deprecated and will be removed."
    warnings.warn(warn_msg, UserWarning)
    # print('<< output file open >>')
    # build output file path & file open
    file_name = []
    file_name.append(path)
    file_name.append('/')
    prefix = re.findall(
        r'(CSQ[BCEHIJMNOPQRTUVWXY012359]{1})', soup.find('title').text)
    file_name.append(prefix[0])
    file_name.append('.csv')
    try:
        f = codecs.open(''.join(file_name), 'w', 'utf-8')
        try:
            f.write('message' + soup.find('title').text + '\n')
            f.write('version' + ver + '\n')
            f.write("message ID,message" + '\n')
            # scraping href tag
            fname = get_individual_source(soup)
            list = [""] * 2
            # scraping individual message description
            tag = soup.find_all('span', class_='ulchildlinktext')
            position = 0
            for i in tag:
                txt = i.get_text()
                re.search(
                    r'(CSQ[BCEHIJMNOPQRTUVWXY012359]{1}[0-9n]{3})([\\s]{0,}[:]{1}[\\s]{0,})(.*)', txt)

                txt = format_message(txt)
                msg_id = re.findall(r'(CSQ.{1}[0-9n]{3}[A-Z]{1})', txt)
                if len(msg_id) == 0:
                    continue
                list[0] = wrapper(msg_id[0])
                message = re.findall(r'(\:.*)', txt)
                if len(message) == 0:
                    message = re.sub(
                        r'(CSQ.{1}[0-9n]{3}[A-Z]{1})', '', txt)
                    list[1] = wrapper(message[2:])
                else:
                    list[1] = wrapper(message[0][2:])
                f.write(','.join(list) + '\n')
                list = [""] * 2
        except IOError as e:
            print('Cannot open "{0}"'.format(''.join(file_name)))
            print(' e:[{0}]'.format(e))
        finally:
            f.close()
    except IOError as e:
        print('Cannot open "{0}"'.format(''.join(file_name)))
        print(' errNo.:{0} msg:{1}'.format(e.errno, e.strerror))


def parse_mq_701(soup, ver, path):
    # html structure is same as V710 manual.
    warn_msg = "`parse_mq_701` is deprecated and will be removed."
    warnings.warn(warn_msg, UserWarning)
    parse_mq_710(soup, ver, path)

def wrapper(str):
    # output text may contains comma, so all text must be quoted not to be recognized
    # as a separator in .csv file.
    str = '"' + str + '"'
    return str

def format_message(message_description):
    # remove trademark
    message_description = message_description.replace('\\xc3\\x82', '')
    message_description = message_description.replace('\\xc2\\xae', '')
    message_description = message_description.replace('\\xe2\\x84\\xa2', '')

    # remove CRLF
    message_description = message_description.replace('\\r\\n', '')
    message_description = message_description.replace('\\x0d', '')
    message_description = message_description.replace('\\x0a', ' ')
    message_description = message_description.replace('\\x84', '')
    message_description = message_description.replace('\\n', ' ')
    # remove extra blanks
    message_description = re.sub(r'\s{2,}', ' ', message_description)
    message_description = re.sub(r'\s$', '', message_description)
    # remove leading blanks
    message_description = re.sub(r'^\s', '', message_description)
    # replace soft blank
    message_description = message_description.replace('\\xc2\\xa0', ' ')
    # replace symbol
    # similar to hyphen
    message_description = message_description.replace('\\xe2\\x80\\x91', '-')
    message_description = message_description.replace('\\xe2\\x80\\x92', '-')
    message_description = message_description.replace('\\xe2\\x80\\x93', '-')
    message_description = message_description.replace('\\xe2\\x88\\x92', '-')
    # similar to single quote
    message_description = message_description.replace('\\xe2\\x80\\x98', '\'')
    message_description = message_description.replace('\\xe2\\x80\\x99', '\'')
    message_description = message_description.replace('\\xe2\\x80\\x9b', '\'')
    # Three dot leader
    message_description = message_description.replace('\xe2\x80\xa6', '...')
    return message_description


def get_individual_source(soup):
    # get html where the tag contains <a class="xref=">
    fname = soup.find_all('a', class_='xref')
    return fname