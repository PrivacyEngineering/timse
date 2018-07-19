#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

from app.controller import *


def scan_all_decorators(path_to_project):

    timse_content = []
    all_files = []
    output_file = open('timse_decorator_information.txt', 'w')

    for dirName, subdirList, fileList in os.walk(path_to_project):
        for fname in fileList:
            if 'timse_parser' not in fname:
                all_files.append((fname, dirName + '/' + fname))

    for file, filepath in all_files:
        print(file)
        if (file.endswith('.py')):

            line_counter = 1
            found_timse = False

            third_party_content = ''
            data_disclosed_content = ''
            purpose_content = ''
            storage_period_content = ''

            with open(filepath, 'r') as current_file:

                for current_line in current_file:

                    if ('timse.x' in current_line):
                        found_timse = True

                    if (current_line.startswith('def ')):
                        if (found_timse):
                            print('Timse decorator on method ' + current_line.replace("\n", "").replace("    ",""))
                            continue

                    if(found_timse):
                        if ('third_party=' in current_line):
                            third_party_content = re.findall("third_party='(.*?)'", current_line)[0]

                        if ('data_disclosed=' in current_line):
                            data_disclosed_content = re.findall("data_disclosed=\[(.*?)\]", current_line)[0]

                        if ('purpose=' in current_line):
                            purpose_content = re.findall("purpose=\[(.*?)\]", current_line)[0]

                        if ('storage_period=' in current_line):
                            storage_period_content = re.findall("storage_period=\[(.*?)\]", current_line)[0]

                    if ('requests.' in current_line):
                        if (found_timse):

                            timse_content.append([third_party_content, data_disclosed_content, purpose_content, storage_period_content])

                        found_timse = False

                    line_counter += 1

        output_file.write(str(timse_content))

    return [DataExchange(element[0], element[1], element[2], element[3]).get() for element in timse_content]


if __name__ == '__main__':
    test_url = 'test_case'

    scan_all_decorators(test_url)
