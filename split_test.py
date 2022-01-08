import os
import shutil

from .entities.StorageNode import StorageNode

from fsplit.filesplit import Filesplit
import tkinter as tk
from tkinter import filedialog

from .entities.Directory import Directory

fs = Filesplit()


def main():
	"""root = tk.Tk()
	root.withdraw()

	file_path = filedialog.askopenfilename()

	print(file_path)"""

	storageRoot = []


	file_path = "music_test.mp3"

	shutil.rmtree("temp_out")
	os.mkdir("temp_out")

	file_size = os.path.getsize(file_path)
	if file_size > 4194304:
		fs.split(file=file_path, split_size=4194304, output_dir="temp_out", callback=split_cb)


def split_cb(f, s):
	print("file: {0}, size: {1}".format(f, s))


if __name__ == "__main__":
	main()
