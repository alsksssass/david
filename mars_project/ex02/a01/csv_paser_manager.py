import csv
import pprint
import operator as op


class Csv_manager:
    def __init__(self):
        self.csv_data = []
        self.csv_header = None

    def set_csv(self, file_path: str, open_type: str = "r", debug: bool = False):
        try:
            if file_path == None:
                raise ValueError("error : file path error")
            with open(file_path, open_type, encoding="utf-8") as data:
                readLine = csv.reader(data)
                self.csv_header = next(readLine)

                if debug:
                    pprint.pprint(self.csv_header)
                for row in readLine:
                    if debug:
                        pprint.pprint(row)
                    self.csv_data.append(row)
        except Exception as e:
            print("error : set_csv")
            raise

    def get_csv_list(self):
        return self.csv_data.copy()

    def get_csv_header(self):
        return self.csv_header.copy()

    # def get_csv_filter(self, filter, index):
    #     return [row for row in self.csv_data if filter(row, index)]

    def get_csv_filter(self, data, index, operator=None):
        data_index = self.csv_header.index(data)
        if data_index == None:
            raise ValueError("error : data colum Not exist!")
        if type(index) == str:
            return [row for row in self.csv_data if index == row[data_index]]
        if operator not in [">", "<", ">=", "<="]:
            raise ValueError("error : invalid operator!")
        op_fun = {
            ">": op.gt,
            "<": op.lt,
            "<=": op.le,
            ">=": op.ge,
        }[operator]
        if type(index) == float:
            return [
                row for row in self.csv_data if op_fun(float(row[data_index]), index)
            ]
