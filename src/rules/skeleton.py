# skeleton.py
# Author: Valtyr Farshield

import os
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class Skeleton(object):

    def __init__(self):
        self.file_name = "skeleton.txt"
        self.json_file_name = "skeleton.json"

    def __str__(self):
        output = ""
        return output

    def process_km(self, killmail):
        pass

    def additional_processing(self, directory):
        pass

    def preprocess_output(self, dictionary):
        del dictionary["file_name"]
        del dictionary["json_file_name"]
        return dictionary

    def output_results(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_full_path = os.path.join(directory, self.file_name)
        json_file_full_path = os.path.join(directory, self.json_file_name)
        with open(file_full_path, 'w') as f_out:
            f_out.write(str(self))
        with open(json_file_full_path, 'w') as f_out:
            dictionary = self.preprocess_output(self.__dict__)
            f_out.write(json.dumps(self.__dict__, cls=SetEncoder, indent=4, separators=(',', ': ')))
        self.additional_processing(directory)
