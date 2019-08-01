import os 
import csv
import pandas as pd 
dictionary = {}

field  = "address,categories,city,country,latitude,longitude,name,postalCode,province,reviews.date,reviews.dateAdded,reviews.doRecommend,reviews.id,reviews.rating,reviews.text,reviews.title,reviews.userCity,reviews.username,reviews.userProvince"
file_path = "hotel-reviews/7282_1.csv"

locationlist = pd.read_csv(file_path)
is_hotel = locationlist["categories"]== "Hotels"
hotel_list = locationlist[is_hotel]
csvfile = hotel_list.to_csv(r"hotels_noindex.csv",index=None, header=True)

print (hotel_list.head())


'''with open (file_path, newline="") as csvfile:
    Reader = csv.DictReader(csvfile)
    for (i , row) in enumerate(Reader):
        print (i,row)
        dictionary[i] = row 
    temp = dictionary[1]
    print(temp)
needed_data = dictionary ['' ] '''    