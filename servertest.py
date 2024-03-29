import requests
import json
import pandas as pd
from ibm_watson import ToneAnalyzerV3
import os 

def call_server_analyzer():
    
    newURL = URLserver_tone + hotelname #+'/'
    res = requests.post(newURL)
    if res.status_code == 200:
        print(res.content)
        res_dict = json.loads(res.text)
        print(res_dict)
    return res

def analyzer(watson_key,watson_url,hotel_name):
    maxlen = 390
    hotel_data = hotel_list[hotel_list["name"]== hotel_name]
    hotel_review = hotel_data["reviews.text"]
    if len(hotel_review) > maxlen:
        hotel_review = hotel_review[0:maxlen]
        print("------"+hotel_name+">400 ------ ")
    # 2.create json/ string
    json_input = hotel_review.to_json()  # .dumps(hotel_review)
    tone_analyzer = ToneAnalyzerV3(
                version='2017-09-21',
                iam_apikey=watson_key,
                url=watson_url)

    watson_responce = tone_analyzer.tone(
                    {'text':json_input} , 
                    content_language='en', sentences=False, 
                    content_type="application/json").get_result()
    return json.dumps(watson_responce)

def create_single_json(hotelname):
    # creats one json file containing all data about a single hotel given its name
    fields = "address,categories,city,country,latitude,longitude,name,postalCode,province".split(',')
    review_fields = ["date","dateAdded","doRecommend", "id" , "rating","text","title","userCity","username","userProvince"]
    
    new_hotel_data = {}
    reviews = {}
    reviews_formatted={}
    
    hotel_data = hotel_list[hotel_list["name"]== hotelname]

    # seperating all reviews from the rest of the data
    for field in review_fields:
        reviews[field] = hotel_data["reviews." + field]

    # filling everything that's not part of the reviews 
    # 1 static data
    print("")
    for field in fields:
        temp_array = list(hotel_data[field].unique()) #[0]
        new_hotel_data[field] = temp_array#temp_dict    
    # 2 filling watson tone data 
    json_path = os.path.join("hotel-tones",hotelname.replace("/", "=") + ".json")
    if not os.path.exists(json_path):
        string = "json doesn't exist" + hotelname 
        print(string)
        new_hotel_data["tone"] = string
    else:
        with open(json_path) as json_file:
            data = json.load(json_file)
        new_hotel_data["tone"] = data
    # filling reviews
    reviews = pd.DataFrame.from_dict(reviews)
    reviews = reviews.replace({pd.np.nan:"empty"})
    for i,row in reviews.iterrows():
        temp_review = {}
        # for each review copy fields into json form (dictionary)
        for j in range(len(review_fields)):
            temp_review[review_fields[j]] = row[review_fields[j]]
            if  temp_review[review_fields[j]] is None:
                temp_review[review_fields[j]] ="empty"
            
        #add review to the list of reviews 
        reviews_formatted[i] = temp_review    
    new_hotel_data["reviews"] = reviews_formatted
    
    filename =  os.path.join("hotel-database",hotelname.replace("/", "=") + ".json")
    with open(filename, 'w') as f:
        json.dump(new_hotel_data, f)
    return new_hotel_data    



def get_watson_responces():
    for hotelname in namelist:
        print(hotelname)
        if not os.path.exists(os.path.join("hotel-tones",hotelname.replace("/", "=") + ".json") ):
            responce = analyzer(watson_key,watson_url,hotelname)
            filename =  os.path.join("hotel-tones",hotelname.replace("/", "=") + ".json")
            with open(filename, 'w') as f:
                json.dump(responce, f)

def create_dataset():
    for name in namelist:
        print(name)
        json_path = os.path.join("hotel-dataset",name.replace("/", "=") + ".json")
        if not os.path.exists(json_path):
            result = create_single_json(name) 

hotelname= "Hawthorn Suites By Wyndham Livermore Wine Country"
URLserver_tone = "http://127.0.0.1:5000/tone_analyzer/"   #<hotel_name>"
URLserver_index = "http://127.0.0.1:5000/Hotel_Indexer/"  #<indexby>"   

watson_url = "https://gateway-lon.watsonplatform.net/tone-analyzer/api"

watson_key = "key goes here"
file_path  = "hotels_noindex.csv"
hotel_list = pd.read_csv(file_path)
namelist = hotel_list.name.unique()

create_dataset()
   
# responce = analyzer(watson_key,watson_url,hotelname)
# responce = call_server_analyzer()
# print(responce)
