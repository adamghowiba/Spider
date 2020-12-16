import tkinter as tk
import arch
import fileutil
import configutil


# TODO Work on base version of UI, perferably deisgn first.
class SpiderUI:
    def __init__(self, title):
        self.title = title
        self.width, self.height = 600, 600
        self.master = tk.Tk(screenName=self.title)
        self.master.geometry("950x700")
        self.version = '1.0'

        self.navbar = None
        self.home = None
        self.scan = None
        self.history = None

        # Initialization Spider
        self.spider = arch.Spider("https://www.loopnet.com", 'Deland, FL', False)

        # Button Images
        self.home_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/Home.png'))
        self.scan_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/Scan.png'))
        self.history_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/History.png'))
        
        # Background image
        self.background_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/starbackground.png'))

        # Create frames
        self.create_navbar()
        self.create_home_frame()
        self.create_scan_frame()

        # Configure grid
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=4)

        # Other
        self.create_entries()
        self.create_labels()
        self.scan_buttons()

        # Starts the TKinter GUI
        self.master.mainloop()

    def show_frame(self, name):
        if name == 'home':
            self.home.lift()
            self.scan.lower()
        elif name == 'scan':
            self.scan.lift()
            self.home.lower()
        else:
            raise Exception("Invalid frame given")

    def create_navbar(self):
        self.navbar = tk.Frame(self.master, bg='#202040')
        self.navbar.grid(row=0, column=0, sticky='nsew')

        home_button = tk.Button(self.navbar, command=lambda: self.show_frame('home'), image=self.home_button_image,
                                borderwidth=0, bg='#202040', fg='#202040', activebackground='black')

        scan_button = tk.Button(self.navbar, command=lambda: self.show_frame('scan'), image=self.scan_button_image,
                                borderwidth=0, bg='#202040', fg='#202040')
        self.history = tk.Button(self.navbar, image=self.history_button_image, borderwidth=0, bg='#202040')

        home_button.pack(fill=tk.X)
        scan_button.pack(fill=tk.X)
        self.history.pack(fill=tk.X)

    def create_home_frame(self):
        self.home = tk.Frame(self.master, bg='#ff5151')
        self.home.grid(row=0, column=1, sticky='nsew')

        for x in range(3):
            self.home.columnconfigure(x, weight=1)

        scanned_box = tk.Frame(self.home, bg='white', width=250, height=200)
        scanned_box.grid(row=0, column=0, pady=20)
        scanned_box.grid_propagate(False)
        scanned_box.columnconfigure(0, weight=1)

        scanned_list_label = tk.Label(scanned_box, bg='white', fg='black', font=(None, 18), text='Listings Scanned')
        scanned_list_label.grid(row=0, column=0)

        number_list_label = tk.Label(scanned_box, bg='white', fg='black', font=(None, 18), text='5')
        number_list_label.grid(row=1, column=0, pady=40)

        scanned_box1 = tk.Frame(self.home, bg='white', width=250, height=200)
        scanned_box1.grid(row=0, column=1)
        scanned_box1.grid_propagate(False)
        scanned_box1.columnconfigure(0, weight=1)

        scanned_list_label1 = tk.Label(scanned_box1, bg='white', fg='black', font=(None, 18), text='Records Added')
        scanned_list_label1.grid(row=0, column=0)

        number_list_label = tk.Label(scanned_box1, bg='white', fg='black', font=(None, 18), text='10')
        number_list_label.grid(row=1, column=0, pady=40)

        scanned_box2 = tk.Frame(self.home, bg='white', width=250, height=200)
        scanned_box2.grid(row=0, column=2)
        scanned_box2.grid_propagate(False)
        scanned_box2.columnconfigure(0, weight=1)

        scanned_list_label2 = tk.Label(scanned_box2, bg='white', fg='black', font=(None, 18), text='Cities Scanned')
        scanned_list_label2.grid(row=0, column=0)

        number_list_label = tk.Label(scanned_box2, bg='white', fg='black', font=(None, 18), text='15')
        number_list_label.grid(row=1, column=0, pady=40)

    def create_scan_frame(self):
        canv = tk.Canvas(self.master, width=300, height=300)
        canv.grid(row=0, column=1, sticky='nsew')

        self.scan = tk.Frame(canv, bg='#ff5151', width=100, height=100)
        self.scan.grid(row=0, column=1, sticky='nsew')

        background_label = tk.Label(canv, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        # background_label.lower()
        
        self.scan.lower()

    def create_entries(self, get_text=False):
        website = tk.Entry(self.scan, text="Website", width=20, bg="white")
        location = tk.Entry(self.scan, text="Location", width=20, bg="white")
        
        self.scan.columnconfigure(2, weight=1)
        
        website.grid(row=1, column=1, ipady=3, padx=7, pady=3)
        location.grid(row=1, column=3, ipady=3, pady=3)

    def scan_buttons(self):
        submit_button = tk.Button(self.scan, command=self.start_scan, width=9, height=2, text="Start Search")
        submit_button.columnconfigure(0, weight=0)
        submit_button.rowconfigure(5, weight=1)

        submit_button.grid(row=5, column=1, pady=8)

        stop_button = tk.Button(self.scan, width=5, height=2, text='Stop')
        stop_button.grid(row=6, column=2, pady=0)

    def create_labels(self):
        title = tk.Label(self.scan, text='Spider v1.0', fg='black', bg='#ff5151', font=(None, 20))
        # self.scan.columnconfigure(1, weight=1)
        title.grid(row=0, column=1)

        website_label = tk.Label(self.scan, text='Website', fg='black', bg='#ff5151')
        location_label = tk.Label(self.scan, text='Location', fg='black', bg='#ff5151')

        website_label.grid(row=1, column=0)
        location_label.grid(row=1, column=2)

    def start_scan(self):
        self.spider.run()

    def stop_scan(self):
        self.spider.save_listing()
