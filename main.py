from tkinter import *
import tkinter
import tkinter as tk
from tkcalendar import Calendar
import os
from datetime import date

#config.txt
projects = []

if not os.path.exists("config.txt"):
    config = open('config.txt', 'w')
    config.close()
with open("config.txt") as f:
    for i in f.read().split("\n"):
        if i != '':
            projects.append(i)
f.close()
if projects == []:
    projects = ['Project']
    project = ""
else:
    project = projects[0]


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

#root
root = Tk()
root.geometry("900x600")
root.title('Journal remastered')


#topbar and its buttons
frame_topbar = Frame(root)
frame_topbar.grid(row=0, column=0)

btn_reset = tkinter.Button(frame_topbar, text="Reset", bg="green")
btn_restart = tkinter.Button(frame_topbar, text="Restart", bg="green")
btn_exit = tkinter.Button(frame_topbar, text="Exit", bg="green")

btn_reset.grid(row=0, column=1)
btn_restart.grid(row=0, column=2)
btn_exit.grid(row=0, column=3)


#main window
main_window = Frame(root)
main_window.grid(row=1, column=0)

main_window_left = Frame(main_window)
main_window_left.grid(row=0, column=0, sticky="n")

main_window_right = Frame(main_window)
main_window_right.grid(row=0, column=1)

def project_change(options):
    options = variable.get()
    print(options)
    global project
    project = options
    global project_label
    project_label.config(text=project)
    event = ""
    journal(event)

def Project_Enter():
    if Project_Entry.get() != '':
        if Project_Entry.get() not in projects:
            if projects == ['Project']:
                projects.remove('Project')
            projects.append(Project_Entry.get())
            global variable
            variable.set(Project_Entry.get())
            options = variable.get()
            project_change(options)
            Project_Entry.delete(0, END)
            with open("config.txt", "w") as f:
                for i in projects:
                    if i == projects[0]:#write first one without linebreak
                        f.write(i)
                    else:
                        f.write("\n%s" % i)
            f.close()
        global Menu
        Menu = OptionMenu(main_window_left, variable, *projects, command=project_change)
        Menu.grid(row=0, column=0)


variable = StringVar(main_window_left)
if project == '':
    variable.set("Project") # default value
else:
    variable.set(project)
Menu = OptionMenu(main_window_left, variable, *projects, command=project_change)
Menu.grid(row=0, column=0)

Project_Entry = Entry(main_window_left)
Project_Entry.grid(row=0, column=1)

Project_Button = tkinter.Button(main_window_left, text="New project", command=Project_Enter)
Project_Button.grid(row=0, column=2)

#label for current text file
date_label=Label(main_window_right)
date_label.grid(row=0, column=0)

#calendar window
calendar_window = Frame(main_window_left)
calendar_window.grid(row=1, column=0, columnspan=3)

#test current project
project_label = Label(calendar_window)
project_label.grid(row=0, column=0)
project_label.config(text=project)

#calendar buttons
calendar = Calendar(calendar_window, locale = "en")
calendar.grid(row=1, column=0)


#text window and scroll bar
#forgot

text_bar = Frame(main_window_right)
text_bar.grid(row=1, column=0)

value_test = ["x", "y"]

planned_list = OptionMenu(text_bar, variable, *value_test)
text_entry = Entry(text_bar)
task2 = OptionMenu(text_bar, variable, *value_test)

planned_text = Label(text_bar, text="a")
planned_text.grid(row=0, column=0)

planned_list.grid(row=1, column=0)
text_entry.grid(row=1, column=1)
task2.grid(row=1, column=2)

scroll_bar = Scrollbar(main_window_right)
text = CustomText(main_window_right, wrap=WORD, yscrollcommand=scroll_bar.set)

scroll_bar.config(command=text.yview)
scroll_bar.config(command=text.yview_moveto('1.0'))

text.grid(row=2, column=0)
scroll_bar.grid(row=2, column=0)

filename = ""

#main script
def journal(event):
    if project == "":
        return
    global filename

#    text.config(state=NORMAL)

    year = str(calendar.selection_get().strftime("%Y"))
    month = str(calendar.selection_get().strftime("%m"))

#    basepath = os.path.dirname(os.path.realpath(__file__))
#    path = os.path.join(basepath, "projects", project, "journal", year, month)
#    filename = os.path.join(path, f"{calendar.selection_get()}.txt")
    path = (f"projects/{project}/journal/{year}/{month}")
    filename = (f"{path}/{calendar.selection_get()}.txt")

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(f"--{calendar.selection_get()}--\n")
        f.close()
    f = open(filename, "r")
    content = f.read()
    f.close()
    date_label.config(text=calendar.selection_get())

    text.delete(1.0, END)
    text.insert(INSERT, content)

#    if filename == os.path.join(path, f"{date.today()}.txt"):
#        text.config(state=NORMAL)
#    else:
#        text.config(state=DISABLED)

calendar.bind('<<CalendarSelected>>', journal)

def save(event):
    save_file = open(filename, "w")
    save_file.write(text.get(1.0, 'end-1c'))
    save_file.close()

event = ""

journal(event)

text.bind("<<TextModified>>", save)

root.mainloop()