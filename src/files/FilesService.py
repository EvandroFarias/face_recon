import os

class FileManipulation():
    def __init__(self, original_path):
        self.original_path = original_path    

    def check_file(self, file):
        path = f'{self.original_path}\\{file}'
        return os.path.isfile(path)    

    def delete_file(self, file):
        path = f'{self.original_path}\\{file}'
        if self.check_file(file):
            os.remove(path)


    def create_file(self, file):
        path = f'{self.original_path}\\{file}'
        if not os.path.isfile(path):
            open(path, 'x').close()

    def write_file(self, file, text):
        path = f'{self.original_path}\\{file}'
        with open(path, "w") as f:
            f.write(text)

    
    def delete_nfiles(self, *args):
        for file in args:
            if self.check_file(file):
                self.delete_file(file)

        
