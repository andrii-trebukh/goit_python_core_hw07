#!/bin/python3

import re
from sys import argv
from pathlib import Path
import shutil 

TRANS = {
    1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
    1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
    1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
    1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
    1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH',
    1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
    1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i',
    1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
}

FILETYPES = {
    "images": ('JPEG', 'PNG', 'JPG', 'SVG'),
    "video": ('AVI', 'MP4', 'MOV', 'MKV'),
    "documents": ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    "audio": ('MP3', 'OGG', 'WAV', 'AMR'),
    "archives": ('ZIP', 'GZ', 'TAR'),
    "unknown": ()
}

sorted_files = {
        "images": [],
        "video": [],
        "documents": [],
        "audio": [],
        "archives": [],
        "unknown": []
    }
    
known_exts = set()
unknown_exts = set()

def usage():
    print(f"Run this script as:\n{argv[0]} DIR_PATH")
    exit(1)


# def make_prep(folder, rarfile): # remove me before handing!!!!
#     shutil.rmtree(folder, True)
#     shutil.unpack_archive(rarfile)


def make_dirs(path):
    for dir_name in FILETYPES.keys():
        p = Path(f"{path}/{dir_name}")
        if not p.exists():
            p.mkdir()


def normalize(name):
    name = name.translate(TRANS)
    name = re.sub(r"[^a-zA-Z0-9_]{1}","_",name)    
    return name


def def_file_type(file_ext):
    file_ext = file_ext.upper()[1:]
    for cat, exts in FILETYPES.items():
        if file_ext in exts:
            return cat
    return "unknown"


def sort_files(rootpath, path = ""): # need to keep rootpath for further recursive call. path - relative path to rootpath, starts with empty.
    p = Path(f"{rootpath}/{path}")
    for unsorted_item in p.iterdir():
        if unsorted_item.is_dir():
           if unsorted_item.relative_to(rootpath).as_posix() in FILETYPES.keys(): # skip targeted dirs
               continue
           sort_files(rootpath, unsorted_item.relative_to(rootpath)) # recursive function call. need to keep rootpath to move files to targeted dirs e.g. rootpath/audio
           unsorted_item.rmdir() # it should be empty afterall
           continue
        
        file_ext = unsorted_item.suffix # preparing some vars for file processing
        file_new_base_name = normalize(unsorted_item.stem)
        file_type = def_file_type(file_ext)

        file_new_path = Path(f"{rootpath}/{file_type}/{file_new_base_name}{file_ext}")
        file_num=0
        while file_new_path.exists(): # if file name already exist, trying to find appropriate one
            file_num += 1
            file_new_path = Path(f"{rootpath}/{file_type}/{file_new_base_name}_{file_num}{file_ext}")
        
        unsorted_item.rename(file_new_path) # moving file to targeted dir

        sorted_files[file_type].append(file_new_path.name) # collecting some useful data
        file_ext = file_ext.upper()[1:]
        if file_type == "unknown":
            unknown_exts.add(file_ext)
        else:
            known_exts.add(file_ext)


def unpack(dir, file_list):
    for file in file_list:
        file_path = Path(f"{dir}/{file}")
        try:
            shutil.unpack_archive(file_path, file_path.with_suffix(""))
            file_path.unlink()
        except shutil.ReadError:
            print(f"Archive '{file_path}' is corrupted. Leaving unchanged.")


def main():
    
    # make_prep("folder", "folder.tar.gz") # remove me before handing!!!!
    
    if len(argv) != 2:
        usage()

    path = argv[1]

    p = Path(path)
    if not p.is_dir():
        usage()

    make_dirs(path) # creating targeted dirs

    sort_files(path) # it's all fun here!

    unpack(f"{path}/archives", sorted_files["archives"])

    print("Found next files by types:") # let's print results!
    for type, files in sorted_files.items():
        print(f"\n{type}:")
        for file in files:
            print(f"  {file}")

    print(f"\nFound next known file extensions: {known_exts}")
    print(f"\nFound next unknown file extensions: {unknown_exts}")
    
    
if __name__ == "__main__":
    main()
