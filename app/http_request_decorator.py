#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def add_string_to_content(func):
    def func_wrapper(*args, **kwargs):
        return "a request was done at {0}".format(func(*args, **kwargs))
    return func_wrapper

def x(third_party_content = "", data_disclosed_content = [], purpose_content = [], storage_period_content = []):
    def get_request_url(func):

        def func_wrapper(url, *args, **kwargs):
            """
            # TODO: find out, how developers provide the url to their funtions
            # TODO: find out how to parse code to properly find out, when and how a request was made

            print(url)

            if 'http' in str(url):
                # TODO: do something with zweck

                timse_function()
                return "request url: " + str(url) + "\n" + str(func(url, *args, **kwargs))
            else:
                # TODO: return original output without changing anything
                return "why " + str(func(url, *args, **kwargs))
            """
            if (third_party_content == "" or data_disclosed_content == [] or purpose_content == [] or storage_period_content == []):
                print('Field missing ')
            else:
                print()
            return True

        return func_wrapper
    return get_request_url
