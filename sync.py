import os
import shutil
import time
import sys
from datetime import datetime


def get_dir_size(dir_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    return total_size


def date_time():
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y, %H:%M:%S")
    return dt


def log_print_delete():
    f = open(log_file_path + "/" + "logs.txt", "a+")

    f.write("{} {} {} {} {}\n".format(date_time(),
            " - Deleting : ", file, "from", bk_folder))
    f.seek(0)
    print(f.readlines()[-1])
    f.close()


def log_print_copy():
    f = open(log_file_path + "/" + "logs.txt", "a+")

    f.write("{} {} {} {} {}\n".format(date_time(),
            " - Copying : ", file, "to", bk_folder))
    f.seek(0)
    print(f.readlines()[-1])
    f.close()


def log_print_update():
    f = open(log_file_path + "/" + "logs.txt", "a+")

    f.write("{} {} {} {} {}\n".format(date_time(),
            " - Updating : ", file, "at", bk_folder))
    f.seek(0)
    print(f.readlines()[-1])
    f.close()


try:
    while True:

        src_folder = sys.argv[1]
        bk_folder = sys.argv[2]
        log_file_path = sys.argv[3]

        source_content = os.listdir(src_folder)
        backup_content = os.listdir(bk_folder)
        # for copying from source to backup
        difference = list(set(source_content) - set(backup_content))
        # for deleting from backup what was deleted from source
        difference2 = list(set(backup_content) - set(source_content))
        if len(difference) == 0:
            print("NO missing files found in ",
                  bk_folder, '\n')
        else:
            print("You have ", len(difference), " missing file(s)  in ",
                  bk_folder, " ", difference, '\n')
        if len(difference2) != 0:
            print("You have ", len(difference2), "file(s) no longer needed in ",
                  bk_folder, '\n')
        for file in difference:

            src = src_folder + "/" + file
            dst = bk_folder + "/" + file

            if os.path.isfile(src):
                shutil.copy2(src,
                             dst)
                log_print_copy()

            else:
                shutil.copytree(src,
                                dst)
                log_print_copy()

        for file in difference2:
            dst = bk_folder + "/" + file
            if os.path.isfile(dst):
                os.remove(dst)

                log_print_delete()

            else:
                shutil.rmtree(bk_folder + "/" + file)

                log_print_delete()

        for file in source_content:
            src = src_folder + "/" + file
            dst = bk_folder + "/" + file
            if os.path.isfile(dst):
                if os.path.getsize(src) > os.path.getsize(dst) or os.stat(src).st_mtime > os.stat(dst).st_mtime:
                    os.remove(dst)
                    shutil.copy2(src,
                                 dst)

                    log_print_update()
            else:
                if get_dir_size(src) > get_dir_size(dst) or os.stat(src).st_mtime > os.stat(dst).st_mtime:
                    shutil.rmtree(dst)
                    shutil.copytree(src,
                                    dst)

                    log_print_update()

        time.sleep(int(sys.argv[4]))
except KeyboardInterrupt:
    print("\n Script terminated by user")
