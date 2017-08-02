from datetime import datetime
import glob
import json
import os
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db, models


def process_file(files_folder, day, f):
    with open(files_folder + day + f) as data_file:
        # parse filename
        basename = os.path.basename(f)
        tokens = basename.split('.')
        time_str = tokens[0]
        time_str_tokens = time_str.split('-')
        time_h = time_str_tokens[0]
        time_m = time_str_tokens[1]
        route = tokens[1]

        day_str = day.strip('/')
        day_str_tokens = day_str.split('-')
        day_y = day_str_tokens[0]
        day_m = day_str_tokens[1]
        day_d = day_str_tokens[2]

        data = json.load(data_file)
        data_src = data['alternatives'] if 'alternatives' in data else [data,]
        total_times = [a['response']['totalRouteTime'] for a in data_src]
        min_total_time = min(total_times)

        t = models.TotalRouteTime(route=route, total_time=int(min_total_time), timestamp=datetime(int(day_y), int(day_m), int(day_d), int(time_h), int(time_m), 0))
        db.session.add(t)
        db.session.commit()


def main(files_folder):
    PROCESSED_FILES_FILE_PATH = '.processed_files'
    days_full = glob.glob(files_folder + '/*/')
    for day_full in days_full:
        # find unprocessed files
        all_files_full = glob.glob(day_full + '*.json')
        all_files = [a[len(day_full):] for a in all_files_full]
        processed_files_file_path = day_full + PROCESSED_FILES_FILE_PATH

        # processed_files = [line.strip() for line in open(processed_files_file_path, 'r')]
        try:
            with open(processed_files_file_path, 'r') as f:
                processed_files = [line.strip() for line in f]
        except OSError as e:
            processed_files = []

        unprocessed_files = [f for f in all_files if f not in processed_files]

        day = day_full[len(files_folder):]
        # process unprocessed files
        for f in unprocessed_files:
            print(files_folder, day, f)
            process_file(files_folder, day, f)

        # write unprocessed files to .processed_files
        with open(processed_files_file_path, 'a') as fh:
            for f in unprocessed_files:
                fh.write("{}\n".format(f))


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python -m insert_data_from_files [files_folder]')
        exit(1)
    files_folder = sys.argv[1]
    main(files_folder)
