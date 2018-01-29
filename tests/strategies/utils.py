from hypothesis import strategies

from messy.keys import to_file_name

messages = strategies.text().map(str.encode)
# there are 0x110000 codes in unicode starting from 0,
# so max code is 0x110000 - 1 == 0x10ffff
max_unicode_character = '\U0010ffff'
# supposed that "length of ``to_file_name`` function values in bytes"
# is a non-decreasing function
max_name_symbol_length = len(to_file_name(max_unicode_character).encode())
# according to https://serverfault.com/a/9548
max_file_name_length = 255
max_name_length = max_file_name_length // max_name_symbol_length
names = strategies.text(min_size=1,
                        max_size=max_name_length)
