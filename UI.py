import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import main
from StatisticAnalysis import StatisticAnalysis

root = tk.Tk()
root.title('Segmentation and Kmeans')

root.option_add( "*font", "Consolas 12" )



#font config
Title_Font=("Consolas",16)

s = ttk.Style()
s.configure('.', font=('Consolas', 12))


# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# configure labels and entries
title_label=ttk.Label(root, text='Image Analysis',font=Title_Font)
title_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

inputDir_label=ttk.Label(root, text='Input Directory:')
inputDir_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

inputDir = tk.StringVar()
inputDir_entry = ttk.Entry(root,width=100,textvariable=inputDir)
inputDir_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)


outputDir_label=ttk.Label(root, text='Output Directory:')
outputDir_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

outputDir = tk.StringVar()
outputDir_entry = ttk.Entry(root,width=100,textvariable=outputDir)
outputDir_entry.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

#separator
separator = ttk.Separator(root, orient='horizontal')
separator.grid(column=0, row=3, sticky=tk.EW,columnspan=2, padx=5, pady=5)

#label
lab_label=ttk.Label(root, text='Label(s)(example:0 1 2):')
lab_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

lab_Var = tk.StringVar()
lab_Var.set("0 1 2")
lab_entry = ttk.Entry(root,width=100,textvariable=lab_Var)
lab_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

# input directors string to list
# Dir 用","分隔
def DirStr2List(dirStr:str):
    return list(map(str, dirStr.split(',')))
    

# Segmentation button
def seg_button_clicked():
    # output
    target = outputDir.get()
    if(os.path.isdir(target)==False):
        messagebox.showerror(title='Error', message='invalid output folder path, try again.')

    # label
    try:
        labels = [int(n) for n in lab_Var.get().split()]
    except ValueError as error:
        messagebox.showerror(title='Error', message=error)

    #source
    source = inputDir.get()
    sourceList = DirStr2List(source)
    for dir in sourceList:
        if(os.path.isdir(dir)==False):
            messagebox.showerror(title='Error', message='invalid input folder path, try again.')
    #segmentation analysis
    main.SegmentationAnalysis(sourceList,target,labels)


seg_button = ttk.Button(root, text="SegmentationAnalysis")
seg_button.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)
seg_button.configure(command=seg_button_clicked)

# K
K_label=ttk.Label(root, text='K (K>0, k∈integer):')
K_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

K_Var = tk.StringVar()
K_Var.set("15")
K_entry = ttk.Entry(root,width=100,textvariable=K_Var)
K_entry.grid(column=1, row=6, sticky=tk.E, padx=5, pady=5)

# K-List
KList_label=ttk.Label(root, text='KList(example:200 15):')
KList_label.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)

KList_Var = tk.StringVar()
KList_Var.set("200 15")
KList_entry = ttk.Entry(root,width=100,textvariable=KList_Var)
KList_entry.grid(column=1, row=7, sticky=tk.E, padx=5, pady=5)

# Scale
scale_label=ttk.Label(root, text='Scale (0 < Scale < 1):')
scale_label.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)

scale_Var = tk.StringVar()
scale_Var.set("0.6")
scale_entry = ttk.Entry(root,width=100,textvariable=scale_Var)
scale_entry.grid(column=1, row=8, sticky=tk.E, padx=5, pady=5)

#-----------------------Modified Kmeans button------------------------------
def ModifiedKmeans_button_clicked():
    source = inputDir.get()
    if(os.path.isdir(source)==False):
        messagebox.showerror(title='Error', message='invalid input folder path, try again.')

    target = outputDir.get()
    if(os.path.isdir(target)==False):
        messagebox.showerror(title='Error', message='invalid output folder path, try again.')

    try:
        KList = [int(n) for n in KList_Var.get().split()]
        scale=float(scale_Var.get())
    except ValueError as error:
        messagebox.showerror(title='Error', message=error)


    os.chdir(source)
    print(os.getcwd())
    filenames = os.listdir()
    for filename in filenames:
        main.ModifiedKmeans(filename, target, KList, scale)
        

ModifiedKmeans_button = ttk.Button(root, text="ModifiedKmeans")
ModifiedKmeans_button.grid(column=1, row=9, sticky=tk.E, padx=5, pady=5)
ModifiedKmeans_button.configure(command=ModifiedKmeans_button_clicked)


# ----------------------MuitiKmeansAnalysis button------------------------
def MuitiKmeans_button_clicked():

    source = inputDir.get()
    sourceList = DirStr2List(source)
    for dir in sourceList:
        if(os.path.isdir(dir)==False):
            messagebox.showerror(title='Error', message='invalid input folder path, try again.')

    target = outputDir.get()
    if(os.path.isdir(target)==False):
        messagebox.showerror(title='Error', message='invalid output folder path, try again.')

    try:
        K=int(K_Var.get())
    except ValueError as error:
        messagebox.showerror(title='Error', message=error)

    main.MuitiKmeansAnalysis(sourceList,target,K)


# description
scale_label=ttk.Label(root, text='Please enter: Input Directory, Output Directory & K')
scale_label.grid(column=0, row=10,columnspan=2, sticky=tk.W, padx=5, pady=5)

exe_button = ttk.Button(root, text="MuitiKmeansAnalysis")
exe_button.grid(column=1, row=10, sticky=tk.E, padx=5, pady=5)
exe_button.configure(command=MuitiKmeans_button_clicked)

# ------------------------------------颜色占比种类分析---------------------------------------


def BuildColorSourceTable_button_clicked():
    source = SourceDir.get()
    if(os.path.isdir(source)==False):
        messagebox.showerror(title='Error', message='invalid input folder path, try again.')

    target = kmeansResultDir.get()
    if(os.path.isdir(target)==False):
        messagebox.showerror(title='Error', message='invalid output folder path, try again.')
    
    output = outputFileDir.get()

    StatisticAnalysis.ColorSourceAnalysisFromFile(source,target,output)

# UI
title_label2=ttk.Label(root, text='Color -> ObjectType Distribution Analysis',font=Title_Font)
title_label2.grid(column=0, row=11,columnspan = 2, sticky=tk.W, padx=5, pady=5)

#------
Source_label=ttk.Label(root, text='Source Directory:')
Source_label.grid(column=0, row=12, sticky=tk.W, padx=5, pady=5)

SourceDir = tk.StringVar()
Source_entry = ttk.Entry(root,width=100,textvariable=SourceDir)
Source_entry.grid(column=1, row=12, sticky=tk.E, padx=5, pady=5)

#------
kmeansResultDir_label=ttk.Label(root, text='kmeansResult Directory:')
kmeansResultDir_label.grid(column=0, row=13, sticky=tk.W, padx=5, pady=5)

kmeansResultDir = tk.StringVar()
kmeansResultDir_entry = ttk.Entry(root,width=100,textvariable=kmeansResultDir)
kmeansResultDir_entry.grid(column=1, row=13, sticky=tk.E, padx=5, pady=5)

#------
outputFileDir_label=ttk.Label(root, text='outputFile Directory:')
outputFileDir_label.grid(column=0, row=14, sticky=tk.W, padx=5, pady=5)

outputFileDir = tk.StringVar()
outputFileDir_entry = ttk.Entry(root,width=100,textvariable=outputFileDir)
outputFileDir_entry.grid(column=1, row=14, sticky=tk.E, padx=5, pady=5)
outputFileDir.set(os.getcwd()+r"\ObjectTypeDistributionByColor.json")

#------
exe_button = ttk.Button(root, text="BuildColorSourceTable")
exe_button.grid(column=1, row=15, sticky=tk.E, padx=5, pady=5)
exe_button.configure(command=BuildColorSourceTable_button_clicked)



root.mainloop()