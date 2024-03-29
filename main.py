from Mierdecillas.photoCreationDate import lib as photo_creation_date
import argparse

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

photo_creation_date.change_full_directory_modification_time(args.path, args.date)
