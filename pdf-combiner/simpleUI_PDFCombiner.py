#!/usr/bin/env python
import PySimpleGUI as sg
import os
from pdfCombiner import combine_pdfs
import re
#from PIL import Image, ImageTk
#import io

# Get the folder containin:g the images from the user
folder = sg.popup_get_folder('pdf folder to open', default_path='')
if not folder:
    sg.popup_cancel('Cancelling')
    raise SystemExit()

# get list of files in folder
flist0 = os.listdir(folder)

# create sub list of image files (no sub folders, no wrong file types)
fnames = [f for f in flist0 if os.path.isfile(
    os.path.join(folder, f)) and f.lower().endswith(".pdf")]

num_files = len(fnames)                # number of pdf found
if num_files == 0:
    sg.popup('No pdf files in folder')
    raise SystemExit()




col_files = [[sg.Listbox(values=fnames, change_submits=True, size=(60, 10), key='listbox')]
             ]


pdfFilename = sg.InputText()
pageNumber = sg.InputText()
outputFilename = sg.InputText()

inputLayout = [[sg.Text("Enter filename(s) to be combined, file separated with a semicolon ';'")]
                ,[sg.Text("e.g. 1.pdf; 2.pdf")]
                ,[pdfFilename]
                ,[sg.Text("Enter the corresponding page range or 'all', and range separated with a ';'\n\
                          e.g. 1-4; 1-3,5-8 (which means Page 1 to 4 in 1.pdf; page 1 to 3 and 5 to 8 in 2.pdf) ")]
                ,[pageNumber]
                ,[sg.Text("Enter the output filename\n\
                          e.g. combined.pdf")]
                ,[outputFilename]

                ,[sg.Button('Combine', key='-COMBINE-'), sg.Button('Exit', key='-EXIT-')]]

layout = [[sg.Column(col_files)]
          ,inputLayout
          ]

window = sg.Window('pdf Browser', layout)


def contains_letter(input_string):
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(input_string))

def contains_other_symbols(input_string):
    pattern = re.compile(r'[^;,\-]')
    return bool(pattern.search(input_string))

def inputParsing(pdf, page):

    pdf_list = pdf.split(';')
    page_list = page.lower().split(';')

    input_pdf_dict = {}
    
    if len(pdf_list) != len(page_list):
        return [0, "The number of pdf doesn't match the number of page range. Please check again."]
    elif contains_other_symbols(page) == False:
        return [0, "Page number section contains illegal characters. Please check again."]
    elif contains_letter(page) == True:
        for p in page_list:
            if p != "all":
                return [0, "Page number section contains alphabet letter characters. Please check again."]
        for index, (pdf, page) in enumerate(zip(pdf_list, page_list)):
            input_pdf_dict[pdf] = page

    else:
        for index, (pdf, page) in enumerate(zip(pdf_list, page_list)):
            input_pdf_dict[pdf] = page

    if len(input_pdf_dict) == 0:
        return [0, "There is an error when creating the input_pdf_dict. Please check again."]
    
    return [1, input_pdf_dict]
    



while True:
    # read the form
    event, values = window.read()
    #print(event)
    #print(values)
    # perform button and keyboard operations
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    elif event == '-COMBINE-':
        #print(f"pdfFilename: {values[0]}")
        #print(type(values[0]))
        #print(f"pageNumber: {values[1]}")
        #print(f"outputFilename: {values[2]}")

        parsedInput = inputParsing(values[0], values[1])

        if parsedInput[0] == 0:
            sg.popup_ok(parsedInput[1], title='Error')
        else:
            try:
                #print(f"folder: {folder}")
                #print(f"parsedInput: {parsedInput[1]}")
                #print(f"output file: {values[2]}")
                status = combine_pdfs(folder, parsedInput[1], values[2])
                if status == 1:
                    sg.popup_ok(f"pdf saved as {os.path.join(folder, values[2])}.", title='Success')
                else:
                    sg.popup_ok("Status 0. Cannot combine pdf. Please check again.", title='Error')
        
            except :
                sg.popup_ok("Cannot combine pdf. Please check again.", title='Error')
        
    
window.close()
