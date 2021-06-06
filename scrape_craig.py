###################################################
# run script to see all desired cars on craigslist.
###################################################

import requests #allows us to download html
from bs4 import BeautifulSoup #allows us to scrape html
import re
import pprint
from emailcar import send_email


#Create file containing all desired cars
current_dc = ''
with open('dream_cars.txt', mode = 'r') as my_file:
    file_contents = my_file.read().splitlines()
    for content in file_contents:
        current_dc = current_dc + f' {content}\n'
    inp1 = input(f'The current cars you want are:\n {current_dc}' + '\n Would you like to add more (y/n/reset): ')
    response = inp1.lower()
    if response == 'y':
        with open('dream_cars.txt', mode = 'a') as my_file:
            while True:
                car = input('Enter a car you would like to look for. (If done type \'done\'): ')
                if car == 'done':
                    break
                else:
                    my_file.write(car + '\n')
    elif response == 'reset':
        with open('dream_cars.txt', mode = 'w') as my_file:
            while True:
                car = input('Enter a car you would like to look for. (If done type \'done\'): ')
                if car == 'done':
                    break
                else:
                    my_file.write(car + '\n')

dream_cars = []
with open('dream_cars.txt', mode = 'r') as my_file:
    file_contents = my_file.read().splitlines()
    for content in file_contents:
        dream_cars.append(content.lower())

#scrape data of cars from craigslist
res = requests.get('https://vancouver.craigslist.org/d/cars-trucks-by-owner/search/cto?auto_transmission=1')
soup = BeautifulSoup(res.text, 'html.parser')
carinfo = soup.select('.result-title')

def email_all_cars(cars):
    message = []
    for cardict in cars:
        car = cardict['name']
        link = cardict['link']
        message.append(f'{car} just got posted on craigslist.\n {link} \n')
    send_email(input('Please enter the receiving email: '), message)

def create_custom_CL(carinfo):
    cars = []
    for idx, item in enumerate(carinfo):
        name = item.getText().lower()
        href = item.get('href', None)
        carid = item.get('id')

        for car in dream_cars:
            #check if the craigslist ad is a desired car
            match = re.search(car, name)
            #if the vehicle does not already exist in the list, append
            if match: 
                duplicate = 0
                for x in cars:
                    if carid == x['id']:
                        duplicate += 1
                if not duplicate:
                    cardict = {'name':name,'link':href,'id':carid}
                    cars.append(cardict)
                    
                    
    return email_all_cars(cars)

create_custom_CL(carinfo)



