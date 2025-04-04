import csv
import sys
import copy

class Enricher:

    def __init__(self, fieldnames, source=sys.stdin, export=sys.stdout, keep_old_header=False):
        self._new_columns = fieldnames
        self._keep_old_header = keep_old_header
        self._source = open(source) if type(source) == str else source
        self._export = open(export) if type(source) == str else export

        self._inside_iter = False

    def __enter__(self):
        self._reader = csv.DictReader(self._source)
        self._fieldnames = (self._reader.fieldnames if self._keep_old_header else []) + self._new_columns
        self._writer = csv.DictWriter(self._export, fieldnames=self._fieldnames)

        self._writer.writeheader()
        return self

    def __iter__(self):
        self._inside_iter = True
        for row in self._reader:
            self._current_row = row
            yield row
        self._inside_iter = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._source.close()
        self._export.close()

    def writerow(self, data):

        if self._keep_old_header and not self._inside_iter:
            raise Exception("writerow() method not allowed outside of the iterator")

        new_dict = copy.deepcopy(self._current_row)
        if type(data) == list and len(data) == len(self._new_columns):
            sup_dict = {k: v for (k, v) in zip(self._new_columns, data)}

            if self._keep_old_header:
                sup_dict.update(new_dict)

            self._writer.writerow(sup_dict)
        elif type(data) == dict:
            if self._keep_old_header:
                data.update(new_dict)

            self._writer.writerow(data)
        else:
            raise Exception("Not a valid list or dict")

    def log(self, *values):
        print(*values, file=sys.stderr)

