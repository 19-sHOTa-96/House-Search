from bs4 import BeautifulSoup
import requests
from pprint import pprint
import sqlite3
import pandas as pd

connection = sqlite3.connect("HouseData.db")
cursor = connection.cursor()

#Mixed Search
H = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36', 'accepted_language': 'en-US,en;q=0.9,ka-GE;q=0.8,ka;q=0.7'}
URL = "https://binebi.ge/gancxadebebi?page="

class HouseData:

    def __init__(self):
        self.data = []      
        self.data_tupled = []

    def parser(self, city=None, condition=None, transaction=None, pages=2):
        self.city, self.condition, self.transaction, self.pages = city, condition, transaction, pages

        for page in range(self.pages):
            response = requests.get(URL + str(page), H)
            soup = BeautifulSoup(response.text, "html.parser")
            houses = soup.find('div', id="search-item-container").find_all("div", class_="list-item")

            for house in houses:
                locator = "div div div"
                house_info = house.select_one(locator)
                header = house.find("div", class_="item-info").find("a").text.strip()
                house_price = house_info.find("div", class_="item-price m-t-5 m-b-0").text.split()
                house_address = house_info.find("div", class_="address mt-1").text.strip()
                house_specipications = [item.text.split() for item in house.find_all("div", class_="list-item_col")]#.text.split()
                house_description = house_info.find("div", class_="item-description").text.strip()
                                                                                                                                                                                                                                        
                try:
                    dict_data = {}
                    dict_data['header'] = header
                    dict_data['price'] = house_price[0] + ' ' + house_price[1] + ' ' + house_price[2]
                    dict_data['address'] = house_address
                    dict_data['m2'] = house_specipications[0][0] + ' ' + house_specipications[0][1]
                    dict_data['rooms'] = house_specipications[0][2] + ' ' + house_specipications[0][3]
                    dict_data['floor'] = house_specipications[1][0] + ' / ' + house_specipications[1][2] + ' ' + house_specipications[1][3]
                    dict_data['bedroom'] = house_specipications[2][0] + ' ' + house_specipications[2][1]
                    dict_data['description'] = house_description
                    self.data.append(dict_data)
                                            
                except IndexError:
                    dict_data['m2'] = house_specipications[0][0] + ' ' + house_specipications[0][1]
                    dict_data['floor'] = house_specipications[1][0] + ' / ' + house_specipications[1][2] + ' ' + house_specipications[1][3]
                    self.data.append(dict_data)

        # self.data_tupled = []
        for item in self.data:
            try:
                d_1 = (item['header'], item['price'], item['address'], item['m2'], item['rooms'], item['floor'], item['bedroom'], item['description'])
                self.data_tupled.append(tuple(d_1))
            except KeyError:
                continue

    ##DATA BASE FUNCTIONS
    def save_house(self, house):
        
        #Save one house
        self.save_one = False
        cursor.execute("INSERT INTO houses VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", house)
        connection.commit()

        #Save all houses
        self.save_multiply = False
        if self.save_all:
            cursor.executemany("INSERT INTO houses VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", self.data_tupled)
            connection.commit()
       
    def show_saved_houses(self):
        
        cursor.execute("SELECT * FROM houses")
        data = cursor.fetchall()
        return data


    def delete_house(self):

        cursor.execute("DELETE FROM houses WHERE id LIKE :uid", {'uid':id})    




if __name__ == "__main__":
    d_1 = HouseData()
    d_1.parser()
    data = d_1.data
    # pprint(data)
    print(data)


