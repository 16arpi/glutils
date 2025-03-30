import csv
import sys
import copy

class Enricher:

    def __init__(self, fieldnames, source=sys.stdin, export=sys.stdout):
        self._new_columns = fieldnames
        self._source = open(source) if type(source) == str else source
        self._export = open(export) if type(source) == str else export

    def __enter__(self):
        self._reader = csv.DictReader(self._source)
        self._fieldnames = self._reader.fieldnames + self._new_columns
        self._writer = csv.DictWriter(self._export, fieldnames=self._fieldnames)

        self._writer.writeheader()
        return self

    def __iter__(self):
        for row in self._reader:
            self._current_row = row
            yield row

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._source.close()
        self._export.close()

    def writerow(self, data):
        new_dict = copy.deepcopy(self._current_row)
        if type(data) == list and len(data) == len(self._new_columns):
            sup_dict = {k: v for (k, v) in zip(self._new_columns, data)}
            new_dict.update(sup_dict)
            self.log(new_dict)
            self._writer.writerow(new_dict)
        elif type(data) == dict:
            new_dict.update(data)
            self.log(new_dict)
            self._writer.writerow(new_dict)
        else:
            raise Exception("Not a valid list or dict")

    def log(self, *values):
        print(*values, file=sys.stderr)

