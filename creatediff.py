# -*- coding= utf-8 -*-

import argparse
from bs4 import BeautifulSoup
import codecs
from datetime import datetime
import difflib
from glob import glob
import lxml.html
import math
from os.path import join, relpath, abspath, exists
import re
import sys
from tqdm import tqdm
from collections import OrderedDict

def create_diff(args):
    abs_ref_csv_path = abspath(args.referenced_csv_path)
    abs_com_csv_path = abspath(args.compared_csv_path)
    abs_output_path = abspath(args.output_path)
    print('referenced file path: ' + abs_ref_csv_path)
    print('compared file path: ' + abs_com_csv_path)
    print('Output dir: ' + abs_output_path)
    if(not exists(abs_ref_csv_path)):
        print(abs_ref_csv_path, 'is not exist.')
        return
    if(not exists(abs_com_csv_path)):
        print(abs_com_csv_path, ' is not exist.')
        return
    if(not exists(abs_output_path)):
        print(abs_output_path, 'is not exist.')
        return
  
    if args.c:
        print('Create the diff file(s) in CSV format')
    else:
        print('Create the diff file(s) in html format')
    ref_set = set(relpath(x, abs_ref_csv_path)
    for x in glob(join(abs_ref_csv_path, 'CSQ*')))
    com_set = set(relpath(x, abs_com_csv_path)
    for x in glob(join(abs_com_csv_path, 'CSQ*')))
    intersection_set = ref_set.intersection(com_set)
    ref_only_set = ref_set.difference(com_set)
    com_only_set = com_set.difference(ref_set)
    ok_list = list()
    ng_list = list()
  
    allfilenum = len(intersection_set) + len(ref_only_set) + len(com_only_set)
    progress = 0
  
    # get diff of intersection_set
    if len(intersection_set) != 0:
        with tqdm(intersection_set, ncols=100) as pbar:
            for i, input_file in enumerate(pbar):
                pbar.set_postfix(OrderedDict(current=input_file))
                abs_ref_csv_file = join(abs_ref_csv_path, input_file)
                abs_com_csv_file = join(abs_com_csv_path, input_file)
                if args.c == False:
                    filename = input_file.replace('csv', 'html')
                else:
                    filename = input_file
                referenced_msg = readcsv(abs_ref_csv_file, args.c)
                compared_msgs = readcsv(abs_com_csv_file, args.c)
                try:
                    output_file = join(abs_output_path, filename)
                    f = codecs.open(output_file, 'w', 'utf-8')
                    if args.c == False:
                        html = create_diff_html(referenced_msg, compared_msgs)
                        try:
                            f.write(html)
                        except:
                            ng_list.append(input_file)
                            continue
                    else:
                        # csv format
                        csv = create_diff_csv(referenced_msg, compared_msgs)
                        for i in csv:
                            try:
                                f.write(i)
                            except:
                                ng_list.append(input_file)
                                continue
                except OSError as err:
                    print(err)
                finally:
                    f.close()
                    ok_list.append(input_file)
  
    # referenced only
    if len(ref_only_set) != 0:
        with tqdm(ref_only_set, ncols=100) as pbar:
            for i, input_file in enumerate(pbar):
                pbar.set_postfix(OrderedDict(current=input_file))
                abs_ref_csv_file = join(abs_ref_csv_path, input_file)
                if args.c == False:
                    filename = input_file.replace('csv', 'html')
                else:
                    filename = input_file
                referenced_msg = readcsv(abs_ref_csv_file, args.c)
                compared_msgs = ''
                try:
                    output_file = join(abs_output_path, filename)
                    f = codecs.open(output_file, 'w', 'utf-8')
                    if args.c == False:
                        html = create_diff_html(referenced_msg, compared_msgs)
                        try:
                            f.write(html)
                        except:
                            ng_list.append(input_file)
                            continue
                    else:
                        # csv format
                        csv = create_diff_csv(referenced_msg, compared_msgs)
                        for i in csv:
                            try:
                                f.write(i)
                            except:
                                ng_list.append(input_file)
                                continue
                except OSError as err:
                    print(err)
                finally:
                    f.close()
                    ok_list.append(input_file)
  
    # compared only
    if len(com_only_set) != 0:
        with tqdm(com_only_set, ncols=100) as pbar:
            for i, input_file in enumerate(pbar):
                pbar.set_postfix(OrderedDict(current=input_file))
                abs_com_csv_file = join(abs_com_csv_path, input_file)
                if args.c == False:
                    filename = input_file.replace('csv', 'html')
                else:
                    filename = input_file
                referenced_msg = ''
                compared_msgs = readcsv(abs_com_csv_file, args.c)
                try:
                    output_file = join(abs_output_path, filename)
                    f = codecs.open(output_file, 'w', 'utf-8')
                    if args.c == False:
                        html = create_diff_html(referenced_msg, compared_msgs)
                        try:
                            f.write(html)
                        except:
                            ng_list.append(input_file)
                            continue
                    else:
                        # csv format
                        csv = create_diff_csv(referenced_msg, compared_msgs)
                        for i in csv:
                            try:
                                f.write(i)
                            except:
                                ng_list.append(input_file)
                                continue
                except OSError as err:
                    print(err)
                finally:
                    f.close()
                    ok_list.append(input_file)
  
    sys.stderr.write('\n')
    sys.stderr.flush()
    print('Succeeded:')
    print(ok_list)
    print('Failed:')
    print(ng_list)

def create_diff_html(referenced_msg, compared_msgs):
    hd = difflib.HtmlDiff(wrapcolumn=80)
    html = hd.make_file(referenced_msg, compared_msgs)
    return html

def create_diff_csv(referenced_msg, compared_msgs):
    hd = difflib.HtmlDiff()
    html = hd.make_file(referenced_msg, compared_msgs)
    lines = parse_side_by_side(html)
    csvlist = []
    for i in range(0, len(lines), 2):
        if lines[i].text == '':
            origline = ','
        else:
            origline = lines[i].text
        if lines[i + 1].text == '':
            revline = ','
        else:
            revline = lines[i + 1].text
            L = []
            L.append(origline.replace('\xa0', '\x20'))
            L.append(',')
            L.append(revline.replace('\xa0', '\x20'))
            L.append('\n')
            csvlist.append(''.join(L))
    return csvlist

def parse_side_by_side(html):
    soup = BeautifulSoup(html, "lxml")
    nowrap = soup.find_all('td', nowrap='nowrap')
    return nowrap


def readcsv(path, iscsv):
    list = []
    if iscsv:
        for line in open(path):
            list.append(line)
    else:
        for line in open(path):
            line = line.strip('"')
            list.append(line.replace('"', '', 4))
    return list