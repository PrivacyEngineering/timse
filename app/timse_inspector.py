#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import datetime

def parse_file_missing(file, filepath, filename, container):
    container['file'] = filepath

    request_alias = 'requests'

    line_counter = 1
    found_timse = False
    insert_timse = False
    one_request = False

    with open(filepath, 'r') as current_file:

        print('\nFile ' + file + ':')

        for current_line in current_file:

            if ('import requests as' in current_line):
                request_alias = re.findall('import requests as (.*?)', current_line)[0]
                print('new alias for requests: ' + request_alias)

            if ('timse.x' in current_line):
                found_timse = True

            if (request_alias + '.' in current_line):
                if (not found_timse):
                    filename.append({"line": line_counter,
                                      "code": current_line.replace("\n", "").replace("    ", "")})
                    print('Line ' + str(line_counter) + ', missing decorator for request: ' + current_line.replace("\n", "").replace("    ", ""))
                    insert_timse = True
                else:
                    one_request = True

                found_timse = False

            line_counter += 1

        container["missing_timse"] = filename

    if (not insert_timse):
        if (one_request):
            print('All requests are decorated.')
        else:
            print('No requests to decorate found.')


    return container, line_counter


def scan_all_missing(path_to_project, file_postfix = ''):

    result_jsons = []
    all_files = []
    output_file = open('timse_inspector_result' + file_postfix + '.json', 'w')
    start = datetime.datetime.now()
    total_files = 0
    total_relevant_files = 0
    total_line_count = 0

    for dirName, subdirList, fileList in os.walk(path_to_project):
        for fname in fileList:
            if 'timse_inspector' not in fname:
                all_files.append((fname, dirName + '/' + fname))

    for file, filepath in all_files:
        container = {}
        filename = []
        total_files += 1

        if (file.endswith('.py')):
            if 'timse_inspector' in file:
                continue

            total_relevant_files += 1
            container, line_count = parse_file_missing(file, filepath, filename, container)
            total_line_count += line_count

            result_jsons.append(container)



    result = json.dumps(result_jsons, indent= 4)
    output_file.write(result)
    delta = datetime.datetime.now() - start

    print('\nTotal number of files: ' + str(total_files) +
          '\nTotal number of relevant files: ' + str(total_relevant_files) +
          '\nTotal number of lines checked: ' + str(total_line_count) +
          '\nElapsed time to inspect every relevant file: ' + str(delta))
    return result_jsons # will be made accessible via the external API

if __name__ == '__main__':
    test_url = '/home/linh/Documents'

    scan_all_missing(test_url, '_Documents')
