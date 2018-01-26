import enum


@enum.unique
class Status(enum.IntEnum):
    ok = 0
    unknown_error = 1
    invalid_json = 2
    invalid_method = 3
    private_key_received = 4
    private_key_already_exists = 5
    key_not_found = 6
