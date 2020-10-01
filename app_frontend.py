# Imports and Set-up
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import ImageTk, Image
import os

import app_backend

intro_text = "[Some instructions here]"
app_title = "[Title of the app here - vX.X]"

#Set parameters
window_width = 500
window_height = 500
max_screen = False
scrollbar = True

#Global parameters
file_imported = False
df_dict = None

def display_title(title, frame):
    label = ttk.Label(frame, text=title, wraplength=546, justify=tk.LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel')
    label.pack(anchor='nw', padx=(30, 30), pady=(0, 5))
    frame.update()
    return label

def display_message(message, frame):
    label = ttk.Label(frame, text=message, wraplength=546, justify=tk.LEFT, font=("Calibri Italic", 11), style='my.TLabel')
    label.pack(anchor='nw', padx=(30, 30), pady=(0, 5))
    frame.update()
    return label


def save_results(results_dict):
    file_types = [('Excel File', '*.xlsx')]
    saving_path = asksaveasfile(mode='wb', filetypes = file_types, defaultextension=".xlsx")

    result = app_backend.save_dataset(saving_path, results_dict)

    if(result):
        display_message("Saved. Bye!")

def import_file(frame):

    global df_dict
    global file_imported

    if(file_imported):
        return
    dataset_path = askopenfilename()

    #If no file was selected, do nothing
    if not dataset_path:
        return

    import_file_message = display_message("[Importig File / Doing some Task / Your custom message]", frame)

    import_succesfull, import_content = app_backend.import_dataset(dataset_path)
    if(import_succesfull):
        display_message("Dataset read successfully", frame)
        df_dict = import_content

        #Change file_imported status so as to disable new imports
        file_imported = True

    else:
        display_message("Error when importing dataset. Try again", frame)
        display_message(import_content, frame)

    import_file_message.pack_forget()

    display_message("Your task starting now", frame)

    main_function_succesfull, main_function_content = app_backend.main_function(df_dict)

    if(main_function_succesfull):
        display_message("Task ready!", frame)
        select_dataset_button = ttk.Button(frame, text="Save results", command= lambda: save_results(main_function_content), style='my.TButton')
        select_dataset_button.pack(anchor='nw', padx=(30, 30), pady=(0, 5))
    else:
        display_message("There was an error!", frame)




def window_setup(master):

    global window_width
    global window_height

    #Add window title
    master.title(app_title)

    #Add window icon
    if hasattr(sys, "_MEIPASS"):
        icon_location = os.path.join(sys._MEIPASS, 'app_icon.ico')
    else:
        icon_location = 'app_icon.ico'
    master.iconbitmap(icon_location)

    #Set window position and max size
    if(max_screen):
        window_width, window_height = master.winfo_screenwidth(), master.winfo_screenheight() # master.state('zoomed')?
    master.geometry("%dx%d+0+0" % (window_width, window_height))

    #Make window reziable
    master.resizable(True, True)


def window_style_setup(root):
    root.style = ttk.Style()
    root.style.configure('my.TButton', font=("Calibri", 11, 'bold'), background='white')
    root.style.configure('my.TLabel', background='white')
    root.style.configure('my.TCheckbutton', background='white')
    root.style.configure('my.TMenubutton', background='white')

def create_first_view_frame(main_frame):

    first_view_frame = tk.Frame(master=main_frame, bg="white")
    first_view_frame.pack(anchor='nw', padx=(0, 0), pady=(0, 0))

    #Add intro text
    intro_text_label = ttk.Label(first_view_frame, text=intro_text, wraplength=746, justify=tk.LEFT, font=("Calibri", 11), style='my.TLabel')
    intro_text_label.pack(anchor='nw', padx=(30, 30), pady=(0, 12))

    #Labels and buttoms to run app
    start_application_label = ttk.Label(first_view_frame, text="Run application: ", wraplength=546, justify=tk.LEFT, font=("Calibri", 12, 'bold'), style='my.TLabel')
    start_application_label.pack(anchor='nw', padx=(30, 30), pady=(0, 10))

    select_dataset_button = ttk.Button(first_view_frame, text="Select Dataset",
    command=lambda : import_file(first_view_frame), style='my.TButton')
    select_dataset_button.pack(anchor='nw', padx=(30, 30), pady=(0, 5))

    return first_view_frame

def add_scrollbar(root, canvas, frame):

    #Configure frame to recognize scrollregion
    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    def onMouseWheel(canvas, event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    #Bind mousewheel to scrollbar
    frame.bind_all("<MouseWheel>", lambda event, canvas=canvas: onMouseWheel(canvas, event))

    #Create scrollbar
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")

if __name__ == '__main__':

    # Create GUI window
    root = tk.Tk()

    window_setup(root)

    window_style_setup(root)

    # Create canvas where app will displayed
    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Create frame inside canvas
    main_frame = tk.Frame(canvas, width=window_width, height=window_height, bg="white")
    main_frame.pack(side="left", fill="both", expand=True)

    #This create_window is related to the scrollbar.
    canvas.create_window(0,0, window=main_frame, anchor="nw")

    #Create Scrollbar
    if(scrollbar):
        add_scrollbar(root, canvas, main_frame)

    #Add IPA logo
    if hasattr(tk.sys, "_MEIPASS"):
        logo_location = os.path.join(sys._MEIPASS, 'ipa_logo.jpg')
    else:
        logo_location = 'ipa_logo.jpg'
    logo = ImageTk.PhotoImage(Image.open(logo_location).resize((147, 71), Image.ANTIALIAS))
    tk.Label(main_frame, image=logo, borderwidth=0).pack(anchor="nw", padx=(30, 30), pady=(30, 0))

    #Add app title
    app_title_label = ttk.Label(main_frame, text=app_title, wraplength=536, justify=tk.LEFT, font=("Calibri", 13, 'bold'), style='my.TLabel')
    app_title_label.pack(anchor='nw', padx=(30, 30), pady=(30, 10))

    #Create first view page
    first_view_frame = create_first_view_frame(main_frame)

    # Constantly looping event listener
    root.mainloop()
