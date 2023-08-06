from datetime import datetime

from metricsportal.config.dev import DATETIME_FORMAT
from metricsportal.utils.general import string_represents_int


def pad_all_single_digits_with_zero(datetime_input):
    """ user may say '2017-3-4 10:00', but python cannot accept this...we need '2017-03-04 10:00' """
    # http://stackoverflow.com/questions/3748063/what-is-the-syntax-to-insert-one-list-into-another-list-in-python
    # >>> l = [1, 2, 3, 4, 5]
    # >>> l[2:4] = ['a', 'b', 'c'][1:3]
    # >>> l
    # [1, 2, 'b', 'c', 5]
    needed_pad = False
    for i, char in enumerate(datetime_input):
        if i == 0 and string_represents_int(char): # if at beginning
            try:
                _ = int(datetime_input[i + 1])
            except:
                return pad_all_single_digits_with_zero('0' + datetime_input)
        elif i == len(datetime_input): # if at the end
            return datetime_input
        elif  string_represents_int(char): # if somewhere in the middle
            int_fails = 0
            try:
                _ = int(datetime_input[i - 1])
            except:
                int_fails += 1
            try:
                _ = int(datetime_input[i + 1])
            except:
                int_fails += 1
            if int_fails == 2:
                return pad_all_single_digits_with_zero(datetime_input[:i] + '0' + datetime_input[i:])
    return datetime_input


def process_datetime_user_input(datetime_input):
    acceptable_formats = [
        '%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d', '%Y/%m/%d %H:%M', '%Y/%m/%d %H:%M:%S',
        '%m-%d-%Y', '%m-%d-%Y %H:%M', '%m-%d-%Y %H:%M:%S',
        '%m/%d/%Y', '%m/%d/%Y %H:%M', '%m/%d/%Y %H:%M:%S',
        '%m-%d-%y', '%m-%d-%y %H:%M', '%m-%d-%y %H:%M:%S',
        '%m/%d/%y', '%m/%d/%y %H:%M', '%m/%d/%y %H:%M:%S',
        '%b %d, %Y', '%b %d, %Y %H:%M', '%b %d, %Y %H:%M:%S', # like Jan 23, 2016
        '%b %d %Y', '%b %d %Y %H:%M', '%b %d %Y %H:%M:%S', # like Jan 23 2016
        '%B %d, %Y', '%B %d, %Y %H:%M', '%B %d, %Y %H:%M:%S', # like January 23, 2016
        '%B %d %Y', '%B %d %Y %H:%M', '%B %d %Y %H:%M:%S', # like January 23 2016
    ]
    datetime_input = pad_all_single_digits_with_zero(datetime_input)
    for this_format in acceptable_formats:
        try:
            the_datetime = datetime.strptime(datetime_input, this_format)
            return the_datetime
        except:
            pass


def get_formatted_datestring(datetime_input):
    intermediary = process_datetime_user_input(datetime_input)
    return intermediary.strftime(DATETIME_FORMAT)
