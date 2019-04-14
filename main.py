import pywintypes
import win32file
import os
import time
import argparse
import datetime


def get_modification_time(path):
    return os.path.getmtime(path)


def get_creation_time(path):
    return os.path.getctime(path)


def older_date(path):
    m_date = get_modification_time(path)
    c_date = get_creation_time(path)
    if m_date > c_date:
        return c_date
    else:
        return m_date


def parse_date_to_unix_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, '%d-%m-%Y').timetuple())


def change_file_creation_time(path, new_time):
    win_time = pywintypes.Time(new_time)
    new_file = win32file.CreateFile(
        path,
        win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        0
    )

    win32file.SetFileTime(
        new_file,
        win_time
    )

    new_file.close()


def change_file_modification_time(path, new_time):
    os.utime(path, (new_time, new_time))


def change_full_directory_modification_time(path, date):
    files = []
    for r, d, f in os.walk(path):
        for dirs in d:
            change_full_directory_modification_time(dirs, date)

        for file in f:
            files.append(os.path.join(r, file))

    if date == "false":
        for f in files:
            change_file_modification_time(f, older_date(f))
            change_file_creation_time(f, older_date(f))
    else:
        for f in files:
            change_file_creation_time(f, parse_date_to_unix_timestamp(date))
            change_file_modification_time(f, parse_date_to_unix_timestamp(date))


# Main script
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("path", type=str, help="work directory")
parser.add_argument('--date',
                    dest='date',
                    default="false",
                    action='store',
                    nargs='?',
                    type=str,
                    help='date to set, if not present get the last modified date')
args = parser.parse_args()

change_full_directory_modification_time(args.path, args.date)
