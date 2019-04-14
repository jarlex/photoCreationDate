import pywintypes
import win32file
import os
import time
import datetime
import piexif
import math


def get_modification_time(path):
    return os.path.getmtime(path)


def get_creation_time(path):
    return os.path.getctime(path)


def get_creation_photo_time(path):
    try:
        exif_dict = piexif.load(path)
        return time.mktime(
            datetime.datetime.strptime(exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8"),
                                       '%Y:%m:%d %H:%M:%S').timetuple())
    except:
        return math.inf


def older_date(path):
    m_date = get_modification_time(path)
    c_date = get_creation_time(path)
    exif_date = get_creation_photo_time(path)

    return min(m_date, c_date, exif_date)


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


# Change EXIF creation date
def change_photo_taken_time(path, new_time):
    try:
        exif_dict = piexif.load(path)
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime.datetime.fromtimestamp(new_time).strftime(
            '%Y:%m:%d %H:%M:%S').encode("utf-8")
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, path)
    except:
        pass


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
            good_date = older_date(f)
            change_file_creation_time(f, good_date)
            change_photo_taken_time(f, good_date)
            change_file_modification_time(f, good_date)

    else:
        for f in files:
            change_file_creation_time(f, parse_date_to_unix_timestamp(date))
            change_photo_taken_time(f, parse_date_to_unix_timestamp(date))
            change_file_modification_time(f, parse_date_to_unix_timestamp(date))
