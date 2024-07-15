import shutil
from pathlib import Path
import argparse

def get_raw_extension(camera_name):
    if camera_name == 'NIKON_ZF':
        raw_extension = 'NEF'
    elif camera_name == 'EOS_R5':
        raw_extension = 'CR3'
    elif camera_name == 'X-E4':
        raw_extension = 'RAF'
    else:
        print('[WARNING]: Camera model not found, using .DNG RAW extension')
        raw_extension = 'DNG'

    return raw_extension

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('dir', type=str, help='Directory from which we are copying the corresponding RAW files to JPG')
    parser.add_argument('--dry-run', action='store_true', help='Stops creation of new folders and moving')


    args = parser.parse_args()
    args.dir = Path(args.dir)

    if args.dry_run:
        print('== DRY RUN ==')

    for camera_dir in [f for f in args.dir.iterdir() if f.is_dir()]:
        chosen_jpg_dir = camera_dir / 'JPG' / 'Chosen'
        chosen_raw_dir = camera_dir / 'RAW' / 'Chosen'

        raw_extension = get_raw_extension(camera_dir.stem)

        print(f'Directory: {camera_dir.parent.name}')
        print(f'Camera: {camera_dir.stem}')

        # only one or the other can exist, but not both
        # if both folders exist, then we have already run this script

        if chosen_jpg_dir.exists() and chosen_raw_dir.exists():
            print('Both JPG and RAW Chosen folders exist! Skipping...')
            continue

        chosen_extension = None
        chosen_dir = None
        # using the term "dual" like the "conjugate" of the object
        # the "dual" of the directory, if JPG then it is the RAW directory and vice versa
        dual_dir = None
        dual_extension = None

        if chosen_jpg_dir.exists():
            print('Chosen JPG exists!')
            chosen_extension = 'JPG'
            dual_extension = raw_extension
            chosen_dir = chosen_jpg_dir
            dual_dir = chosen_raw_dir
        else:
            print('Chosen JPG does not exist!')

        if chosen_raw_dir.exists():
            print('Chosen RAW exists!')
            chosen_extension = raw_extension
            dual_extension = 'JPG'
            chosen_dir = chosen_raw_dir
            dual_dir = chosen_jpg_dir 
        else:
            print('Chosen RAW does not exist!')

        if chosen_jpg_dir.exists() and not chosen_raw_dir.exists():
            print('Moving chosen RAW files based off chosen JPG list!')

        if not chosen_jpg_dir.exists() and chosen_raw_dir.exists():
            print('Moving chosen JPG files based off chosen RAW list!')

        chosen_files = sorted(list(chosen_dir.glob(f'*.{chosen_extension}')))
        print(f'Moving {len(chosen_files)} {raw_extension} files...')
        confirm = input('Confirm? [y/n]: ')
        if confirm != 'y':
            print('Skipping...')
            print()
            continue

        if not args.dry_run:
            dual_dir.mkdir(parents=True)

        for cf in chosen_files:
            source_dir = dual_dir.parent
            # change filename extension to the dual
            source_filename = f'{cf.stem}.{dual_extension}'

            # moving into the new chosen directory
            source_path = source_dir / source_filename
            dest_path = dual_dir / source_filename

            print(f'Chosen File: {cf}')
            print(f'Moving: {source_path} to {dest_path}')
            if not args.dry_run:
                shutil.move(source_path, dest_path)

            print()

        print()

if __name__=='__main__':
    main()
