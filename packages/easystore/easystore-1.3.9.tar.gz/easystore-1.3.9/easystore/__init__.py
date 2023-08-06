"""
This is the easystore that keeps configurations from multiple services in
a single store location. Uses a redis like interface, ideal to replace redis
with easystore.
"""
import os
import json


class DiskStore(object):
    """Initialize the DiskStore."""

    def __init__(self, storpath='/var/lib/easystore'):
        self.storpath = storpath
        self.__create_storpath()

    def getpath(self):
        return self.storpath

    def __create_storpath(self):
        try:
            if not os.path.exists(self.storpath):
                os.makedirs(self.storpath)
        except Exception:
            raise Exception("Issue with store path, check permissions")

    def setpath(self, storpath='/var/lib/easystore'):
        self.storpath = storpath
        self.__create_storpath()

    def hset(self, filename, keyname, kvdata):
        # TODO: count the number of arguments and raise error
        # TODO: Check if storpath ends with a / and re-eval below
        filepath = self.storpath + "/" + filename + "/" + keyname
        try:
            directory = os.path.dirname(filepath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(filepath) as json_file:
                json_data = json.load(json_file)
            json_data[keyname] = kvdata
        except IOError:
            json_data = dict()
            json_data[keyname] = kvdata

        with open(filepath, 'w') as json_file:
            json.dump(json_data, json_file)

    def set(self, filename, kvdata):
        # TODO: count the number of arguments and raise error
        # TODO: Check if storpath ends with a / and re-eval below
        filepath = self.storpath + "/" + filename
        try:
            json_data = kvdata
            with open(filepath, 'w') as json_file:
                json.dump(json_data, json_file)
        except IOError:
            return None

    def hget(self, filename, keyname):
        # TODO: count the number of arguments and raise error
        filepath = self.storpath + "/" + filename + "/" + keyname
        try:
            directory = os.path.dirname(filepath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(filepath) as json_file:
                json_data = json.load(json_file)
        except IOError:
            return None
        try:
            return json_data[keyname]
        except KeyError:
            return None

    def hdel(self, filename, keyname):
        # TODO: count the number of arguments and raise error
        filepath = self.storpath + "/" + filename + "/" + keyname
        try:
            with open(filepath) as json_file:
                json_data = json.load(json_file)
        except IOError:
            return None
        try:
            with open(filepath) as json_file:
                json_data = json.load(json_file)
            if os.path.isfile(filepath):
                os.remove(filepath)
            return json_data
        except KeyError:
            return None

    def get(self, filename):
        # TODO: count the number of arguments and raise error
        filepath = self.storpath + "/" + filename
        try:
            with open(filepath) as json_file:
                json_data = json.load(json_file)
        except IOError:
            return None
        try:
            return json_data
        except KeyError:
            return None

    def hmget(self, filename, storekeys):
        # TODO: count the number of arguments and raise error
        filepath = self.storpath + "/" + filename
        try:
            values = []
            for i in storekeys:
                directory = os.path.dirname(filepath + '/' + i)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(filepath + '/' + i) as json_file:
                    json_data = json.load(json_file)
                    values.append(json_data[i])
            return values
        except IOError:
            return None

    def hmset(self, filename, storekeys):
        # TODO: count the number of arguments and raise error
        # TODO: Check if storpath ends with a / and re-eval below
        filepath = self.storpath + "/" + filename
        try:
            for i in storekeys:
                directory = os.path.dirname(filepath + '/' + i)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(filepath + '/' + i, 'w') as json_file:
                    json.dump({i: storekeys[i]}, json_file)
        except IOError:
            return None

    def hgetall(self, filename):
        # TODO: count the number of arguments and raise error
        filepath = self.storpath + "/" + filename
        try:
            onlyfiles = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]
            json_dict = {}
            for i in onlyfiles:
                with open(filepath + '/' + i) as json_file:
                    json_data = json.load(json_file)
                    json_dict.update(json_data)
        except IOError:
            return None
        except OSError:
            return None
        if len(json_dict) > 0:
            return json_dict
        else:
            return None
