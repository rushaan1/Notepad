from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox
import tkinter as tk
from tkinter import *
import os
import clipboard
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pyttsx3
app = tk.Tk()
main_menu = tk.Menu()
app.geometry("800x600")
app.title("Untitled-Notepad")

'''
File MENU
'''

file = tk.Menu(main_menu,tearoff = False)
main_menu.add_cascade(label="File", menu=file)

# ALL Functions for the file menu

#NEW FILE

isitsaved = False

#Opening File

text_url = " "


# SAVING THE FILE

def save_file():
    global text_url
    file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                             filetypes=[("All Files", "*.*"),
                                        ("Text Documents", "*.txt")])
    f = open(file, "w")
    f.write(text_editor.get(1.0, END))
    f.close()
    app.title(os.path.basename(file) + " - Notepad")
    print("File Saved")
    global isitsaved
    isitsaved = True

def save__File():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
        if file =="":
            file = None

        else:
            #Save as a new file
            f = open(file, "w")
            f.write(text_editor.get(1.0, END))
            f.close()

            app.title(os.path.basename(file) + " - Notepad")
            print("File Saved")
    else:
        # Save the file
        f = open(file, "w")
        f.write(text_editor.get(1.0, END))
        f.close()
    global isitsaved
    isitsaved = True

def new_file():
    global isitsaved
    if isitsaved == False:
        if messagebox.askyesno(title="Your Changes are not saved", message="You haven't saved this file, are you sure you want to create a new file") == False:
            return
        else:
            app.title("Untitled-Notepad")
            text_editor.delete(1.0, END)
    else:
        app.title("Untitled-Notepad")
        text_editor.delete(1.0, END)



def open_file():
    if text_change == True:
        if messagebox.askyesno(title="Your Changes are not saved", message="You haven't saved this file, are you sure you want to open a new file") == False:
            return
        else:
            global text_url
            text_url = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File",
                                                  filetypes=(("Text file", "*.txt"), ("All files", "*.*")))
            try:
                with open(text_url, "r") as for_read:
                    text_editor.delete(1.0, tk.END)
                    text_editor.insert(1.0, for_read.read())
            except FileNotFoundError:
                return
            except:
                return
            app.title(os.path.basename(text_url))
    else:
        text_url = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File",
                                              filetypes=(("Text file", "*.txt"), ("All files", "*.*")))
        try:
            with open(text_url, "r") as for_read:
                text_editor.delete(1.0, tk.END)
                text_editor.insert(1.0, for_read.read())
        except FileNotFoundError:
            return
        except:
            return
        app.title(os.path.basename(text_url))


def exit_func(event=None):
    global text_url, isitsaved
    if isitsaved == False:
        mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file ?')
        if mbox is True:
            content2 = str(text_editor.get(1.0, tk.END))
            url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',
                                               filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
            url.write(content2)
            url.close()
            app.destroy()
        elif mbox is False:
            app.destroy()
    else:
        app.destroy()


def find_func(event=None):
    def find():
        word = find_input.get()
        print(f"word: {word}")
        text_editor.tag_remove('match', '1.0', tk.END)
        matches = 0
        if word:
            print("made it past 'if word'")
            start_pos = 1.0
            while True:
                print("made it past 'while True'")
                start_pos = text_editor.search(word, start_pos, stopindex=tk.END)
                print(f"start_pos: {start_pos}")
                if not start_pos:
                    print("made it past 'if not start_post'")
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                print(f"end_pos: {end_pos}")
                text_editor.tag_add('match', start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                text_editor.tag_config('match', foreground='red', background='yellow')


    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0, tk.END)
        new_content = content.replace(word, replace_text)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)

    find_dialogue = tk.Toplevel()
    find_dialogue.geometry('450x250+500+200')
    find_dialogue.title('Find')
    find_dialogue.resizable(0, 0)

    ## frame
    find_frame = ttk.LabelFrame(find_dialogue, text='Find & Replace')
    find_frame.pack(pady=20)

    ## labels
    text_find_label = ttk.Label(find_frame, text='Find Word : ')
    text_replace_label = ttk.Label(find_frame, text='Replace Word with : ')

    ## entry
    find_input = ttk.Entry(find_frame, width=50)
    replace_input = ttk.Entry(find_frame, width=50)

    ## button
    find_button = ttk.Button(find_frame, text='Find', command=find)
    replace_button = ttk.Button(find_frame, text='Replace', command=replace)

    ## label grid
    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)

    ## entry grid
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)

    ## button grid
    find_button.grid(row=2, column=0, padx=8, pady=4)
    replace_button.grid(row=2, column=1, padx=8, pady=4)

    find_dialogue.mainloop()


file.add_command(label="New", compound=tk.LEFT, accelerator = "Ctrl+N", command=new_file)
file.add_command(label="Open", compound=tk.LEFT, accelerator = "Ctrl+O",command=open_file)
file.add_command(label="Save File", compound=tk.LEFT, accelerator = "Ctrl+s",command=save__File)
file.add_command(label="Save in New Location", compound=tk.LEFT, accelerator = "Ctrl+Shift+s",command=save_file)
file.add_command(label="Exit", compound=tk.LEFT,command=exit_func)


'''
EDIT MENU
'''

edit = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Find", compound=tk.LEFT, command=find_func)
edit.add_command(label="Copy All", compound=tk.LEFT,command=lambda:clipboard.copy(str(text_editor.get("1.0",END))))
edit.add_command(label="Paste", compound=tk.LEFT,command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label="Cut All", compound=tk.LEFT,command=lambda:text_editor.delete("1.0",END))


'''
VIEW MENU
'''

show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar_label.pack_forget()
        show_toolbar = False
    else :
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar_label.pack(side=tk.TOP, fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar = True

def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else :
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar = True




view = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="View", menu=view)
view.add_checkbutton(label="Tool Bar", onvalue=True, offvalue=0, compound=tk.LEFT, command=hide_toolbar)
view.add_checkbutton(label="Status Bar", onvalue=True, offvalue=0, compound=tk.LEFT,command=hide_statusbar)

'''
COLOR THEME MENU
'''


color_theme = tk.Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Color Themes", menu=color_theme)

def change_to_default():
    text_editor.config(background="white", fg="black")

def change_to_yellow():
    text_editor.config(background="yellow",fg="black")

def change_to_cream():
    text_editor.config(background="#FFFDD0",fg="black")

def change_tosblue():
    text_editor.config(background="#87CEEB",fg="black")

def change_to_orange():
    text_editor.config(background="#ff781f",fg="black")

def change_to_peach():
    text_editor.config(background="#FFE5B4",fg="black")

def change_to_l_pink():
    text_editor.config(background="#FFB6C1",fg="black")

def change_to_h_pink():
    text_editor.config(background="#FF007F",fg="white")

def change_to_green():
    text_editor.config(background="#80c904", fg="white")

def change_to_nb():
    text_editor.config(background="#152238", fg="white")

def change_to_black():
    text_editor.config(background="Black", fg="white")


color_theme.add_radiobutton(label="DEFAULT", compound=tk.LEFT,command=change_to_default)
color_theme.add_radiobutton(label="Dark",compound=tk.LEFT,command=change_to_black)
color_theme.add_radiobutton(label="Yellow", compound=tk.LEFT,command=change_to_yellow)
color_theme.add_radiobutton(label="Cream", compound=tk.LEFT,command=change_to_cream)
color_theme.add_radiobutton(label="Sky Blue", compound=tk.LEFT,command=change_tosblue)
color_theme.add_radiobutton(label="Orange", compound=tk.LEFT,command=change_to_orange)
color_theme.add_radiobutton(label="Peach", compound=tk.LEFT,command=change_to_peach)
color_theme.add_radiobutton(label="Light Pink", compound=tk.LEFT,command=change_to_l_pink)
color_theme.add_radiobutton(label="Hot Pink", compound=tk.LEFT,command=change_to_h_pink)
color_theme.add_radiobutton(label="Green", compound=tk.LEFT,command=change_to_green)
color_theme.add_radiobutton(label="Navy Blue", compound=tk.LEFT,command=change_to_nb)
'''
FONTS MENU
'''
tool_bar_label = ttk.Label(app)
tool_bar_label.pack(side=tk.TOP, fill=tk.X)
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar_label,width = 30, textvariable=font_family, state = 'readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index("Arial"))
font_box.grid(row=0, column=0, padx=5,pady=5)

'''
SIZE MENU
'''

size_variable = tk.IntVar()
font_size = ttk.Combobox(tool_bar_label, width=20, textvariable=size_variable)
font_size["values"] = tuple(range(8,100,2))
font_size.current(5)
font_size.grid(row=0, column=1,padx=5)

'''
ALL BUTTONS
'''

bold_btn = ttk.Button(tool_bar_label, text="BOLD")
bold_btn.grid(row=0,column=2,padx=5)

font_color_button = ttk.Button(tool_bar_label, text="Font Colors")
font_color_button.grid(row=0,column=4,padx=5)

allignleft_btn = ttk.Button(tool_bar_label, text="Allign Left")
allignleft_btn.grid(row=0,column=5,padx=5)

alligncenter_btn = ttk.Button(tool_bar_label, text="Allign Center")
alligncenter_btn.grid(row=0,column=6,padx=5)

allignright_btn = ttk.Button(tool_bar_label, text="Allign Right")
allignright_btn.grid(row=0,column=7,padx=5)

speak_btn = ttk.Button(tool_bar_label, text="Speak")
speak_btn.grid(row=0,column=8,padx=5)

'''
TEXT EDITOR
'''

text_editor = tk.Text(app)
text_editor.config(wrap='word', relief=tk.FLAT, font=font_family.get())


scroll_bar = tk.Scrollbar(app)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

'''
STATUS BAR AND MORE 
'''

status_bar = ttk.Label(app, text="Status Bar")
status_bar.pack(side = tk.BOTTOM)

text_change = False

def change_word(event=None):
    global text_change
    if text_editor.edit_modified():
        text_change = True
        word = len(text_editor.get(1.0,"end-1c").split())
        character = len(text_editor.get(1.0,"end-1c").replace(" ", ""))
        status_bar.config(text = f"Total Characters: {character} \n Total Words: {word}")
    text_editor.edit_modified(False)

text_editor.bind("<<Modified>>", change_word)

speak = False

def speakk():
    engine = pyttsx3.init()
    text = text_editor.get('1.0',END)
    engine.say(text)
    engine.runAndWait()

speak_btn.configure(command=speakk)

'''
FONTS AND FONT SIZEZ 
'''

font_now = "Arial"
font_size_now = 18

#font changing function
def change_font(app):
    global font_now
    font_now = font_family.get()
    text_editor.configure(font=(font_now,font_size_now))
font_box.bind("<<ComboboxSelected>>",change_font)

def change_fontsize(event=None):
    global font_size_now
    font_size_now = size_variable.get()
    text_editor.configure(font=(font_now, font_size_now))
font_size.bind("<<ComboboxSelected>>",change_fontsize)


#bold function

def make_bold():
    text_get = tk.font.Font(font=text_editor["font"])
    if text_get.actual()["weight"] == 'normal':
        text_editor.configure(font=(font_now,font_size_now,"bold"))
    if text_get.actual()["weight"] == 'bold':
        text_editor.configure(font=(font_now,font_size_now,"normal"))
bold_btn.configure(command=make_bold)

def color_chooser():
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

font_color_button.configure(command=color_chooser)

def align_center():
    all_text = text_editor.get(1.0,"end")
    text_editor.tag_config("center", justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT, all_text,"center")

alligncenter_btn.configure(command=align_center)

def align_left():
    all_text = text_editor.get(1.0,"end")
    text_editor.tag_config("left", justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT, all_text,"left")

allignleft_btn.configure(command=align_left)

def align_right():
    all_text = text_editor.get(1.0,"end")
    text_editor.tag_config("right", justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT, all_text,"right")

allignright_btn.configure(command=align_right)

app.config(menu=main_menu)
if __name__ == '__main__':
    file = None
    app.mainloop()
