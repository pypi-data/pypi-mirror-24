from datetime import datetime


def string_represents_int(s):
    try:
        int(s)
        return True
    except:
        return False


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


def generate_acceptable_formats():
    HOUR_MINUTE_FORMAT = "%H:%M"
    HOUR_MINUTE_SECOND_FORMAT = "%H:%M:%S"
    day_formats = [
        '%Y-%m-%d',  # like: "2016-01-23"
        '%Y/%m/%d',  # like: "2016/01/23"
        '%m-%d-%Y',  # like: "01-23-2016"
        '%m/%d/%Y',  # like: "01/23/2016"
        '%m-%d-%y',  # like: "01-23-16"
        '%m/%d/%y',  # like: "01/23/16"
        '%b %d, %Y', # like: "Jan 23, 2016"
        '%b %d %Y',  # like: "Jan 23 2016"
        '%B %d, %Y', # like: "January 23, 2016"
        '%B %d %Y',  # like: "January 23 2016"
        '%d %B %Y',  # like: "23 January 2016"
        '%d %B, %Y', # like: "23 January, 2016"
    ]
    all_formats = []
    for this_format in day_formats:
        all_formats.append(this_format)
        all_formats.append(this_format + " " + HOUR_MINUTE_FORMAT)
        all_formats.append(this_format + " " + HOUR_MINUTE_SECOND_FORMAT)
    return all_formats


def text_to_datetime(datetime_input):
    acceptable_formats = generate_acceptable_formats()
    datetime_input = pad_all_single_digits_with_zero(datetime_input)
    for this_format in acceptable_formats:
        try:
            the_datetime = datetime.strptime(datetime_input, this_format)
            return the_datetime
        except:
            pass
