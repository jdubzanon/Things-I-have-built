import tkinter as tk
from tkinter import ttk



class Shell(ttk.Frame):
    def add_frame(self, label, row=None, col=None):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(row=row, column=col)
        return frame

    def __init__(self, *args, **kwargs):
        super().__init__()

        #####entry widget/command execution window####
        entry_frame = self.add_frame('Enter Commands Here', row=0)
        self.entry_var = tk.StringVar()
        self.ent_widget = tk.Entry(entry_frame, textvariable=self.entry_var, width=80)
        self.ent_widget.grid()

        #####command history window#####
        command_history_frame = self.add_frame('Command History', row=1)
        self.history_var = tk.StringVar()
        self.command_history_list = []
        self.command_history = ttk.Combobox(command_history_frame, values=self.command_history_list, width=80,
                                            postcommand=lambda: self.command_history.configure(
                                                values=self.command_history_list,
                                                takefocus=1))
        self.command_history.grid()

        ###textbox widget/output window#####
        textbox_frame = self.add_frame('Output Window', row=2)
        self.big_box = tk.Text(textbox_frame, height=30, width=100, background='black', foreground='white',
                               takefocus=0, wrap='none')
        self.big_box.grid()
        ###widget binding###
        self.command_history.bind('<Return>', self.cmd_history_bind_func)
        self.big_box.bind('<FocusIn>', lambda event: self.ent_widget.focus_set())

    def cmd_history_bind_func(self, event):
        self.command_history.focus_set()
        self.entry_var.set(self.command_history_list[self.command_history.current()])
        self.command_history_list.pop(self.command_history.current())
        self.ent_widget.focus_set()
        self.ent_widget.icursor(tk.END)
        self.command_history.set('')
