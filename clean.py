import os  # Library to delete files from a folder
import shutil  # Library to delete files from a folder


def clean_folder():
    folder = './back-versions'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def delete_files(from_, to_):
    for version in range(from_, to_-1, -1):
        os.remove(f"back-versions/version{version}.png")
        print(f"The file '{version}' has been removed")
