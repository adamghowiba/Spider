import tkinter as tk
import arch
from tkinter import messagebox


# TODO Work on base version of UI, perferably deisgn first.
class SpiderUI:
    def __init__(self, title):
        self.title = title
        self.width, self.height = 600, 600
        self.master = tk.Tk(screenName=self.title)
        self.master.geometry("500x500")
        self.frame = self.create_frame()
        self.version = '1.0'

        # self.frame.grid_rowconfigure(1, weight=6)
        # self.frame.grid_columnconfigure(0, weight=1)

        self.search_city_entry(False)
        self.create_title()
        self.submit_button()

        # Starts the TKinter GUI
        self.master.mainloop()

    def create_frame(self):
        frame = tk.Frame(self.master, bg='#222831')
        frame.place(relwidth=1.0, relheight=1.0)

        return frame

    def search_city_entry(self, get_text=False):
        click = tk.Entry(self.frame, text="CLick Me", width=20, bg="#ffd369")
        location = tk.Entry(self.frame, text="Test", width=20, bg="white")
        max = tk.Entry(self.frame, text="Test", width=20, bg="white")

        max.grid(row=3, column=0, ipady=3)
        location.grid(row=2, column=0, ipady=3)
        click.grid(row=1, column=0, ipady=3)

        if get_text:
            return str(click.get())

    def submit_button(self):
        submit_button = tk.Button(self.frame, width=5, height=1, text="Search")
        submit_button.grid_columnconfigure(0, weight=0)
        submit_button.grid(row=1, column=1, padx=4)

    def start_scan(self):
        spider = arch.Spider("https://www.loopnet.com", self.search_city_entry(True))
        spider.lookup_location_action()
        spider.store_current_listings()
        spider.scan_listings()
    
    def create_title(self):
        title = tk.Label(self.frame, text='Spider v1.0', fg='white', bg='#222831', font=(None, 20))

        title.grid(row=0, column=8)
