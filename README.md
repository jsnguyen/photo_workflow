# photo\_workflow

Personal scripts for photo workflow. Some scripts take user input to make photo folders and copy the files.

## Folder Structure
Title Folder:  `YYYYMMDD\_title/`

Camera Folder: `camera/`
 
Data Folders:  `JPG/` , `RAW/` , `Videos/`

## Files
```pwmakef.py```
Makes the photo folder structure without copying anything. Requires user input for date, title, and camera name.

```pwimport.py```
Automatically import files and sort them into JPG, RAW, and video files. Needs input to pick the date, set the title, and set camera name if it cannot be determined from the image files.

## Usage
```python3 ./pwmakef.py -[jrv] <search_dir>```

```python3 ./pwimport.py <search_dir>```

## Examples
Needs to be a valid mount point and have `Volumes` as one of the parent folders

Make folder structure without video folder from `sd_card`.

```python3 ./pwmakef.py -v /Volumes/sd_card```

Make folder structure from `sd_card`.

```python3 ./pwimport.py /Volumes/sd_card```
