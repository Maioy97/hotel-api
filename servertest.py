import requests
import json
import pandas as pd
from ibm_watson import ToneAnalyzerV3



def call_server_analyzer():
    
    newURL = URLserver_tone + hotelname #+'/'
    res = requests.post(newURL)
    if res.status_code == 200:
        print(res.content)
        res_dict = json.loads(res.text)
        print(res_dict)
    return res


def analyzer(watson_key,watson_url,hotel_name):
    hotel_data = hotel_list[hotel_list["name"]== hotel_name]
    hotel_review = hotel_data["reviews.text"]
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

hotelname= "Hawthorn Suites By Wyndham Livermore Wine Country"
URLserver_tone = "http://127.0.0.1:5000/tone_analyzer/"   #<hotel_name>"
URLserver_index = "http://127.0.0.1:5000/Hotel_Indexer/"  #<indexby>"   

watson_url = "https://gateway-lon.watsonplatform.net/tone-analyzer/api"
watson_key = "key goes here"
file_path  = "hotels_noindex.csv"
hotel_list = pd.read_csv(file_path)

#responce = analyzer(watson_key,watson_url,hotelname)
responce = call_server_analyzer()
print(responce)