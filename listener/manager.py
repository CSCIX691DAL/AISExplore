import os
import shutil


def str_to_path(f_name):
    f_name = f_name[:10]
    f_name = f_name.replace('-', '/')
    return f_name


if __name__ == '__main__':
    files = os.listdir('.')
    csv = [file for file in files if 'csv' in file]
    csv = sorted(csv)
    csv.pop(-1)
    for csv_file in csv:
        path = str_to_path(csv_file) + '/'
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.move(csv_file, path)
        print("Moved {} to {}".format(csv_file, path))
