import dropbox
import datetime


class DropboxAccess:
    def __init__(self, access_token, current_root):
        self.all_dropbox_items = set()
        self.folders = set()
        self.access_token = access_token
        self.current_root = current_root

    def get_dropbox_items(self):
        return self.all_dropbox_items

    def get_dropbox_folders(self):
        return self.folders

    def create_folder(self, folder_name, f):
        try:
            f.write('[%s] trying to create folder. \n' % datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"))
            dbx = dropbox.Dropbox(self.access_token)
            new_folder_path = '/%s/%s' % (self.current_root, folder_name)
            print('new_folder_path: ', new_folder_path)
            dbx.files_create_folder_v2(new_folder_path)
            print("new folder created: ", new_folder_path)
            f.write('[%s] folder created sucessfully.\n' % datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"))
        except dropbox.exceptions.ApiError:
            f.write('[%s] folder could not be created.\n ' % datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"))
            print('could not create folder named: %s' % folder_name)

    def get_dropbox_files_in_folders(self, folder_name, f):
        f.write('[%s] checking all files within folder: %s. \n' %
                (datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S")), folder_name)
        dbx = dropbox.Dropbox(self.access_token)
        response = dbx.files_list_folder('/%s/%s/' % (self.current_root, folder_name))
        cursor = response.cursor
        length = len(response.entries)
        count = 0
        for i in range(length):
            count += 1
            self.all_dropbox_items.add(response.entries[i].name.lower())
            # print(response.entries[i].name)
        while response.has_more:
            response = dbx.files_list_folder_continue(cursor)
            cursor = response.cursor
            length = len(response.entries)
            for i in range(length):
                count += 1
                self.all_dropbox_items.add(response.entries[i].name.lower())
                # print(response.entries[i].name)
        print('%s has %s in the folder' % (folder_name, count))

    def get_dropbox_folders_in_all(self, f):
        f.write('[%s] checking all folders within root.\n' % datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"))
        dbx = dropbox.Dropbox(self.access_token)
        response = dbx.files_list_folder('/%s/' % self.current_root)
        cursor = response.cursor
        length = len(response.entries)
        for i in range(length):
            self.folders.add(response.entries[i].name)
            print('initial: %s ' % response.entries[i].name)
        while response.has_more:
            response = dbx.files_list_folder_continue(cursor)
            cursor = response.cursor
            length = len(response.entries)
            for i in range(length):
                self.folders.add(response.entries[i].name)
                print('while: %s ' % response.entries[i].name)

    def upload_file(self, file_from, file_to, f_write):
        try:
            # upload a file to Dropbox using API v2
            dbx = dropbox.Dropbox(self.access_token)
            with open(file_from, 'rb') as f:
                dbx.files_upload(f.read(), file_to)
            return True
        except:
            print("UPLOAD BROKE FOR : " + file_from)
            f_write.write('[%s] Failed to upload %s. \n' % (datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"),
                                                            file_from))
            return False

    def upload_items(self, set_list, folder_name, f):
        f.write('[%s] uploading %s items to dropbox. \n' % (datetime.datetime.now().strftime("%m/%d/%y-%H:%M:%S"),
                                                            len(set_list)))
        for item in set_list:
            file_from = item[1]
            file_name = '/%s/%s/%s' % (self.current_root, folder_name, item[0])
            print('file_from: %s, file_name: %s' % (file_from, file_name))
            self.upload_file(file_from, file_name, f)
            # print(item[0] + " ::: " + item[1])
