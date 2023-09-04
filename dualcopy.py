import shutil
from pathlib import Path

def main():
    directory = Path('/Users/jsn/landing/archived_pictures/2023/2023-09-03_Bridges')

    for camera_dir in [f for f in directory.iterdir() if f.is_dir()]:
        chosen_dir = camera_dir / 'JPG' / 'Chosen'
        print(chosen_dir)

    chosen_jpgs = list(chosen_dir.glob('*.JPG')) + list(chosen_dir.glob('*.jpg'))
    for cj in chosen_jpgs:
        raw_name = '{}.RAF'.format(cj.stem)
        print(cj.name, raw_name)


if __name__=='__main__':
    main()