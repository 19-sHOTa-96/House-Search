import tkinter as tk
from tkinter import *
from tkinter import ttk
from main import HouseData
from geopy.geocoders import Nominatim
from IPython.display import HTML
import folium
from time import sleep
import webbrowser
import os
import tkintermapview
import sqlite3
from pprint import pprint


class HouseSearchApp(HouseData):
    
    def __init__(self):
        super().__init__()
        self.progress_index = 0
        self.res_flag = False

    # Search 
    def search_window(self, window):    

        window.title("House Main Gui")
        window.resizable(False, False)

        print(self.res_flag)

        window.geometry("200x220")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        ttk.Label(window, text = "City:").grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(window, text = 'Condition:').grid(row = 2, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(window, text = 'Transaction type: ').grid(row = 4, column = 0, padx = 5, sticky = 'sw')

        city = StringVar()
        condition = StringVar()
        transaction = StringVar()

        self.city = ttk.Combobox(window, width = 24, font = ('Arial', 10), textvariable=city, values=('Tbilisi', 'Rustavi', 'Kutaisi'))
        self.condition = ttk.Combobox(window, width = 24, font = ('Arial', 10), textvariable=condition, values=('New', 'Old'))
        self.transaction = ttk.Combobox(window, width = 24, font = ('Arial', 10), textvariable=condition, values=('Rent', 'Buy'))

        self.city.grid(row = 1, column = 0, padx = 5)
        self.condition.grid(row = 3, column = 0, padx = 5)
        self.transaction.grid(row = 5, column = 0, padx = 5)

        print(self.city.get(), self.condition.get(), self.transaction.get())

        self.city.set("Tbilisi")
        self.condition.set("New")
        self.transaction.set("Buy")

        self.search_button = ttk.Button(window, text="Search", command=self.result_window).grid(row = 6, columnspan = 2, pady = 10)
        self.progress_search = ttk.Progressbar(window, orient=HORIZONTAL, length=180, mode='determinate').grid(row = 7, columnspan = 2, pady = 3)

    # Result
    def result_window(self):
          
        print(self.res_flag)

        res_win = Toplevel(window)
        res_win.title('Current Results')
        res_win.geometry("1420x590")
        res_win.resizable(False, False)

        s = ttk.Style() 
        s.theme_use('clam')
        s.configure('Treeview', rowheight=40)

        columns = ('header', 'price', 'address', 'm2', 'rooms', 'floor', 'bedroom')
        self.tree = ttk.Treeview(res_win, columns=columns, show='headings')

        # self.tree.heading('id', text='id')
        self.tree.heading('header', text='header')
        self.tree.heading('price', text='price')
        self.tree.heading('address', text='address')
        self.tree.heading('m2', text='m2')
        self.tree.heading('rooms', text='rooms')
        self.tree.heading('floor', text='floor')
        self.tree.heading('bedroom', text='bedroom')

        houses = []
        self.parser()
        for item in self.data_tupled:
            houses.append(item)

        index = 0    
        for house in houses:
            self.tree.insert('', tk.END, values=house)
            self.progress_index += 1
            # self.search_progress()
            print(self.progress_index)

        self.tree.grid(row=0, column=1, sticky='ns')
        scrollbar = ttk.Scrollbar(res_win, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=4, sticky='ns')
        
        ttk.Button(res_win, text="Show On Map", command=self.get_location).grid(row = 5, columnspan = 2, pady = 10)
        ttk.Button(res_win, text="Add To Favorites", command=self.save).grid(row = 7, columnspan = 2, pady = 10)
        ttk.Button(res_win, text="Show Saved Houses").grid(row = 8, columnspan = 2, pady = 10)

        self.res_flag = True  

    def get_location(self):

        selected_house = self.tree.focus()
        values = self.tree.item(selected_house, 'values')
        print(values)
        address = values[2]

        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(address)

        root = Toplevel(window)
        root.title("Map") 
        root.geometry("900x700")

        label = LabelFrame(root)
        label.pack(pady=30)

        house_map = tkintermapview.TkinterMapView(label, width = 800, height = 600, corner_radius = 0)
        house_map.set_position(location.latitude, location.longitude, marker = True)
        house_map.set_zoom(20)
        house_map.set_marker(location.latitude, location.longitude, text=address)
        house_map.pack()


    def search_progress(self):
        self.progress_search.step()


    def save(self):
        
        selected_house = self.tree.focus()
        values = self.tree.item(selected_house, 'values')
        self.save_house(values)
        


    def show(self):
        pass


    def delete(self):
        pass



window = Tk()

app = HouseSearchApp()
app.search_window(window)

window.mainloop()