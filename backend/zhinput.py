import json


class ZHInputException(Exception):
    def __init__(self, key):
        super(ZHInputException, self).__init__()
        self.key = key


class ZHInputKeyNotExist(ZHInputException):
    def __init__(self, key):
        super(ZHInputKeyNotExist, self).__init__(key)


class ZHInputNotFloat(ZHInputException):
    def __init__(self, key, value):
        super(ZHInputNotFloat, self).__init__(key)
        self.value = value


class ZHInputNotInt(ZHInputException):
    def __init__(self, key, value):
        super(ZHInputNotInt, self).__init__(key)
        self.value = value


class ZHInputStringNotLongEnough(ZHInputException):
    def __init__(self, key, value):
        super(ZHInputStringNotLongEnough, self).__init__(key)
        self.value = value


class ZHInputStringTooShort(ZHInputException):
    def __init__(self, key, value):
        super(ZHInputStringNotLongEnough, self).__init__(key)
        self.value = value

class ZHInputEnumNotExists(ZHInputException):
    def __init__(self, key, value):
        super(ZHInputEnumNotExists, self).__init__(key)
        self.value = value


class ZHInputNotJSONString(ZHInputException):
    def __init__(self, key, value):
        super(ZHInputNotJSONString, self).__init__(key)
        self.value = value


def all_exists(data, key_list):
    for key in key_list:
        if key not in data:
            raise ZHInputKeyNotExist(key)


def as_float(data, key, default=0.0):
    if key in data:
        try:
            return float(data[key])
        except ValueError:
            raise ZHInputNotFloat(key, data[key])
    return default


def as_int(data, key, default=0):
    if key in data:
        try:
            return int(data[key])
        except ValueError:
            raise ZHInputNotInt(key, data[key])
    return default


def as_string(data, key, min_length=0, max_length=None, default=''):
    if key in data:
        if len(data[key]) < min_length:
            raise ZHInputStringNotLongEnough(key, data[key])
        if max_length:
            if len(data[key]) > max_length:
                raise ZHInputStringTooShort(key, data[key])
        return data[key]
    return default


def as_enum(data, key, enum_list, default_enum_index=0):
    if key in data:
        if data[key] not in enum_list:
            raise ZHInputEnumNotExists(key, data[key])
        return data[key]
    return enum_list[default_enum_index]


def as_bool(data, key, true_value='true', default=False):
    if key in data:
        if data[key] == true_value:
            return True
        else:
            return False
    return default

def as_json(data, key, default=None):
    if key in data:
        try:
            return json.loads(data[key])
        except ValueError:
            raise ZHInputNotJSONString(key, data[key])
    if default is None:
        return {}
    return default


def filter_by_list(data, filter_list):
    result = {}
    for d in data:
        if d in filter_list:
            result[d] = data[d]
    return result
