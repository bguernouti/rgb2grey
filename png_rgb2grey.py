import sys
from core.converter import Rgb2Grey

app = Rgb2Grey()

class FileNameNotProvidedError(Exception):
    pass

def default():
    app.convert_all
    
def convert_file(filename):
    app.convert_file(file_name=filename)


if __name__ == "__main__":

    args = sys.argv

    if "-f" in args:
        try :
            fname = args[args.index("-f")+1]
            app.convert_file(fname)
        except :
            raise FileNameNotProvidedError("No file name provided, Usage -f [filename]")
    else :
        # We ignore any other argument, and convert all images
        app.convert_all()        
