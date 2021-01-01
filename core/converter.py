import png # Main package for preprocessing png files
import os

from typing import IO


class Rgb2Grey(object):

    __ext: str = ".png"

    def __init__(self, **dirs):

        self.colored_dir: str = dirs.get("colored_dir") if dirs.get("colored_dir") else "images/colored"
        self.grey_dir: str = dirs.get("grey_dir") if dirs.get("grey_dir") else "images/grey"

    @staticmethod
    def __rgb2grey(_rgb: tuple) -> int:
        Y:float = (0.299 * _rgb[0]) + (0.587 * _rgb[1]) + (0.114 * _rgb[2])
        return int(Y)

    def __decode_data(self, _file: str) -> tuple:

        f: IO = open(_file, "rb")
        r: png.Reader = png.Reader(file=f)
        rows, cols, data, params = r.read()

        if params.get("greyscale"):
            raise TypeError("File is already black and white")

        # Step for extracting pixles values, 3 if rgb, 4 if rgba
        # Pixels data are organized [r,g,b, r,g,b, r,g,b, ....] if alpha is not set
        # [r,g,b,a, r,g,b,a, r,g,b,a, ....] if alpha is  set
        # This step is important to exactly collect (r,g,b) or (r,g,b,a) of each pixel
        step: int = 4 if params.get("alpha") else 3 

        # png.read() provide pixels data as generator function.
        grey_pixels: list = []

        for px_row in data:
            pixels_row: list = []
            for index in range(0, len(px_row), step):
                t:tuple = (px_row[index], px_row[index+1], px_row[index+2])
                grey:int = self.__rgb2grey(t)
                pixels_row.append(grey)
            grey_pixels.append(pixels_row)
        
        f.close()

        return (rows, cols, grey_pixels)

    def convert_file(self, file_name: str) -> None:

        f_name: str = file_name.replace(self.__ext, "")
        full_file_path: str = os.path.join(self.colored_dir, f_name+self.__ext)

        if not os.path.exists(full_file_path):
            raise FileNotFoundError("File not found, {}".format(full_file_path))

        png_rows, png_cols, pixels = self.__decode_data(full_file_path) # Bluid output pixels

        out_file: str = os.path.join(self.grey_dir, f_name + self.__ext)

        f: IO = open(out_file, "wb")
        w: png.Writer = png.Writer(png_rows, png_cols, greyscale=True)
        w.write(f, pixels)
        f.close()
        return 

    def convert_all(self) -> None:
        
        files: list = next(os.walk(self.colored_dir))[2] # Not the best
        
        for file in files:
            self.convert_file(file)
        
        return
