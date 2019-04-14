from Mierdecillas.photoCreationDate import lib as photo_creation_date
import argparse

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

print(photo_creation_date.get_creation_photo_time(args.path))
print(photo_creation_date.get_creation_time(args.path))
print(photo_creation_date.get_modification_time(args.path))

print(photo_creation_date.older_date(args.path))
