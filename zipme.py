import zipfile
import sys
import os

def zip_folder(folder_paths, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    for folder_path in folder_paths:
        parent_folder = os.path.dirname(folder_path)
        # Retrieve the paths of the folder contents.
        contents = os.walk(folder_path)
        try:
            for root, folders, files in contents:
                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    relative_path = absolute_path.replace(parent_folder, '')
                    # print "Adding '%s' to archive." % absolute_path
                    zip_file.write(absolute_path, relative_path)
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(parent_folder, '')
                    # print "Adding '%s' to archive." % absolute_path
                    zip_file.write(absolute_path, relative_path)
            # print "'%s' created successfully." % output_path
        except IOError, message:
            print "1 %s"%message
            sys.exit(1)
        except OSError, message:
            print "2 %s"%message
            sys.exit(1)
        except zipfile.BadZipfile, message:
            print "3 %s"%message
            sys.exit(1)
    zip_file.close()
    # print "'%s' created successfully." % output_path
