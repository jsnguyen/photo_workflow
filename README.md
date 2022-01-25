# photo\_workflow

Personal scripts for photo workflow. Takes some user input to make photo folders and copy the files.

## Folder Structure

Title Folder:  `YYYYMMDD\_title/`

Camera Folder: `camera/`
t 
Data Folders:  `JPG/` , `RAW/` , `Videos/`

## Files
```pwmakef.py```
Makes the photo folder structure without copying anything.

```pwimport.py```
Automatically import files and sort them into JPG, RAW, and video files.

## Usage
```python3 ./pwmakef.py <search_dir>```

```python3 ./pwimport.py <search_dir>```

## Examples

Needs to be a valid mount point and have `Volumes` as one of the parent folders

```python3 ./pwmakef.py /Volumes/sd_card```

```python3 ./pwmakef.py /Volumes/sd_card```
