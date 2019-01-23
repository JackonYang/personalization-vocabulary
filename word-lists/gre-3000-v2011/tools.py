import csv
import json


def csv_to_json(file_basename):
    csv_filename = '%s.csv' % file_basename

    data = {}

    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            # data check
            if len(row) != 2:
                print('error', type(row), row)
            data[row[0]] = row[1]

    json_filename = '%s.json' % file_basename
    with open(json_filename, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=4)


if __name__ == '__main__':
    csv_to_json('gre-3000-v2011')