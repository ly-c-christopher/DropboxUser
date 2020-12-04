from os import scandir
from DropboxAccess import DropboxAccess
from config import config
import datetime

SET_PATH_LIST = set()
SERVER_ITEM_NAMES = set()


def main():
    f = open("dropbox_log_file.txt", "a")
    f.write('[%s] Run time \n' % datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"))
    params = config('dropbox')
    f.write('[%s] scanning local files. \n' % datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"))
    get_local_files(params['server_path'])
    dba = DropboxAccess(access_token=params['user_key'], current_root='All_NuOrder_Images')
    dba.get_dropbox_folders_in_all(f)
    for folder_name in dba.get_dropbox_folders():
        print('folder_name: %s' % folder_name)
        dba.get_dropbox_files_in_folders(folder_name, f)
    print('dba.all_dropbox_items: %s' % len(dba.all_dropbox_items))
    print('SERVER_ITEM_NAMES %s ' % len(SERVER_ITEM_NAMES))
    f.write('[%s] total items in dropbox: %s \n' % (datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"),
                                                    len(dba.get_dropbox_items())))
    f.write('[%s] total items in local disk: %s \n' % (datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"),
                                                       len(SERVER_ITEM_NAMES)))
    difference_set = SERVER_ITEM_NAMES.difference(dba.get_dropbox_items())

    if len(difference_set) > 0:
        today = datetime.datetime.today()
        today_string = '%s-%s-%s' % (today.month, today.day, today.year)
        dba.create_folder(str(today_string), f)
        new_upload_set = set()  # images with the file path in local network
        print('getting missing file directories')
        for diff in difference_set:
            for pathItem in SET_PATH_LIST:
                if diff.lower() == pathItem[0].lower():
                    new_upload_set.add(pathItem)
                    break
        dba.upload_items(new_upload_set, today_string, f)
    else:
        f.write('[%s] No items found to upload.')
    f.write('============================================================================================\n')
    f.close()


def get_local_files(path):
    dir_entries = scandir(path)
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            if ".png" in entry.name and 'bom' not in entry.name and 'cad' not in entry.name and 'CAD' not in entry.name \
                    and 'BOM' not in entry.name:
                if entry.name[len(entry.name) - 8: len(entry.name) - 7] == '_' and (entry.name.find(" ") == -1) and \
                        (entry.name.count("_") == 1):
                    if len(entry.name[0: len(entry.name) - 8]) <= 8:
                        SET_PATH_LIST.add((entry.name.lower(), path + "\\" + entry.name))
                        SERVER_ITEM_NAMES.add(entry.name.lower())
                        # print("LOCAL FILE: " + entry.name.lower())
        else:
            get_local_files(path + "\\" + entry.name)


if __name__ == '__main__':
    main()
