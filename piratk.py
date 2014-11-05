import tkinter as tk
import tkinter.ttk as ttk


class FullscreenApp2(object):

    def __init__(self, master):
        self._master = master
        master.attributes('-zoomed', True)

        style = ttk.Style()
        style.configure("TButton",
                        foreground="green",
                        background='#000022',
                        relief="flat")
        style.map("TButton",
                  background=[('pressed', '#000055'),
                              ('active', '#000033')])
        style.configure("TFrame", background="#000022")
        style.configure("TTreeView",
                        fieldbackground="#000022",
                        background="#000022")

        self.frame = ttk.Frame(master)

        ttk.Button(self.frame, text="<").pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Treeview(self.frame).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Button(self.frame, text=">").pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.frame.pack(fill=tk.BOTH, expand=True)
        self.is_fullscreen = False
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self._master.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.is_fullscreen = False
        self._master.attributes("-fullscreen", False)
        return "break"


root = tk.Tk()
app = FullscreenApp2(root)
root.mainloop()
