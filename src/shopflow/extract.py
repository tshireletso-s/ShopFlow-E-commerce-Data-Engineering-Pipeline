import csv


def data_extraction(csv_file: str):
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            dict_reader = csv.DictReader(file)
            new_dictionary = []
            for row in dict_reader:
                new_dictionary.append(row)
            if new_dictionary == []:
                return "This csv file is empty"
            return new_dictionary
    except FileNotFoundError:
        return "This csv file does not exist"


