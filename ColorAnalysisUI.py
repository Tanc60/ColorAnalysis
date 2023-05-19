import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import main
import Helper
from ImageAnalysis import ImageAnalysis


root = tk.Tk()
root.title('Color Analysis')

root.option_add("*font", "Consolas 12")


# font config
Title_Font = ("Consolas", 16)

s = ttk.Style()
s.configure('.', font=('Consolas', 12))


# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# configure labels and entries

# title
title_label = ttk.Label(root, text='ColorAnalysis', font=Title_Font)
title_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

# input
inputDir_label = ttk.Label(root, text='Input Directory:')
inputDir_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
# input entry
inputDir = tk.StringVar()
inputDir_entry = ttk.Entry(root, width=100, textvariable=inputDir)
inputDir_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

# output
outputDir_label = ttk.Label(root, text='Output Directory:')
outputDir_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
# output entry
outputDir = tk.StringVar()
outputDir_entry = ttk.Entry(root, width=100, textvariable=outputDir)
outputDir_entry.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)


def command_button_clicked():

    source = inputDir.get()
    sourceList = Helper.DirStr2List(source)
    filenameList = Helper.DirList2FileNameList(sourceList)

    for dir in sourceList:
        if (os.path.isdir(dir) == False):
            messagebox.showerror(
                title='Error', message='invalid input folder path, try again.')

    target = outputDir.get()
    if (os.path.isdir(target) == False):
        messagebox.showerror(
            title='Error', message='invalid output folder path, try again.')

    ImageAnalysis.ImageFiles2Graph(filenameList, target)


command_button = ttk.Button(root, text="Bar and Pie Graph")
command_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
command_button.configure(command=command_button_clicked)


def histogram_button_clicked():
    source = inputDir.get()
    sourceList = Helper.DirStr2List(source)
    filenameList = Helper.DirList2FileNameList(sourceList)

    for dir in sourceList:
        if (os.path.isdir(dir) == False):
            messagebox.showerror(
                title='Error', message='invalid input folder path, try again.')

    target = outputDir.get()
    if (os.path.isdir(target) == False):
        messagebox.showerror(
            title='Error', message='invalid output folder path, try again.')

    for filename in filenameList:
        basename = os.path.basename(filename)
        targetfilename = os.path.join(target, basename)

        ImageAnalysis.draw_histogram(filename, targetfilename)


command_button = ttk.Button(root, text="Histogram")
command_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)
command_button.configure(command=histogram_button_clicked)

root.mainloop()
