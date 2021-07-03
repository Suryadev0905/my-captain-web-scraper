# Project 2 : Web Scraping using BeautifulSoup4 and requests

import requests 
from bs4 import BeautifulSoup
import pandas
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--page_no", help="Enter the number of apges to parse", type=int)
args = parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_no = args.page_no
scraped_info_list = []

for page_num in range(page_no):
    req = requests.get(oyo_url + str(page_num))
    content = req.content

    soup = BeautifulSoup(content, "html.parser")

    all_hotels = soup.find_all("div", {"class": "hotelCardListing"})
    

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("h3", {"class": "listingHotelDescription_hotelName"}).text
        hotel_dict["address"] = hotel.find("span", {"itemprop": "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class": "listingPrice_finalPrice"}).text
        try:
            hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating_ratingSummary"}).text
        except AttributeError:
            pass 

        parent_amenities_element = hotel.find("div", {"class": "amenityWrapper"})    

        amenities_list = []
        for amenity in parent_amenities_element.find_all("div", {"class": "amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())

        hotel_dict["amenities"] = ', '.join(amenities_list[:-1])

        scraped_info_list.append(hotel_dict)

        # print(hotel_name, hotel_address, hotel_price, hotel_rating, amenities_list)

dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")