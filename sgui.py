import tkinter as tk


root = tk.Tk()
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)




f = tk.Frame(root)
f.grid(row=1, column=2, sticky=tk.SE)

g = tk.Button(f, text="Export", width=5, height=3)
g.pack()


root.mainloop()