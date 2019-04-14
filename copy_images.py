import os, sys
import glob
import shutil

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

save_dir = ("images_Gdrive/")

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
drive_folder_id = '1_i7k0O0QFUZelvUVnisMY1jS7VsQ2PdS?lfhs=2'


def main():
    download_Gdrive(save_dir)
    # file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
    # for file1 in file_list:
    #     print('title: %s, id: %s' % (file1['title'], file1['id']))


    # files = listing_file()
    # image_files = listing_file(image_path)
    # for i, file in enumerate(files):
    #     print(image_path)
    #     shutil.copyfile(file, image_path)

def download_Gdrive(save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    max_result = 200
    query =  "'{}' in parents and trashed=false".format(drive_folder_id)

    for file_list in drive.ListFile({'q':query, 'maxResults':max_result}):
        for file in file_list:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                    download_recursively(os.path.join(save_folder, file['title']), file['id'])
            else:
                file.GetContentFile(os.path.join(save_folder, file['title']))



def listing_file(path=None):
    if path != None:
        files = glob.glob(os.path.join(path,"*.png"))
    else:
        files = glob.glob("*.png")
        
    for i, file in enumerate(files):
        fname_for_print = file.split("\\")[-1]
        # print("[",i,"]",fname_for_print)
    
    return files
    # fnum = input("select file No. > ")
    # fnum = int(fnum)
    # if fnum >= 0 and fnum <= len(files):
    #     print(files[fnum])
    #     return files[fnum]
    # elif(fnum == -1):
    #     print(files[fnum])
    #     return files[fnum]
    # else:
    #     print("failed.")

if __name__ == "__main__":
    main()