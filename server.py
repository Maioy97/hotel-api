from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pandas as pd
from ibm_watson import ToneAnalyzerV3

app = Flask(__name__)
api = Api(app)
file_path  = "hotels_noindex.csv"
watson_url = "https://gateway-lon.watsonplatform.net/tone-analyzer/api"
watson_key = "key goes here"

class Hotel_Tone_Analyzer(Resource):
    def post(self,hotel_name):
        print("---Hotel analyser---")
        tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey=watson_key,
            url=watson_url)
        # 1.extract hotel data
        print("name:" + hotel_name)
        hotel_data = hotel_list[hotel_list["name"]== hotel_name]
        hotel_review = hotel_data["reviews.text"]
        # 2.create json/ string 
        watson_input =hotel_review.to_json()
        #print("\n"+hotel_review.head())
        # 3.send it to watson
        
        try : 
            #watson 
            print("try")
            watson_responce = tone_analyzer.tone(
                {'text':watson_input} , content_language='en', content_type="application/json").get_result()
            print("watson passed" + watson_responce)
            # dict_responce = json.dumps(watson_responce,indent = 2 )
            # print(dict_responce)
            return watson_responce ,200
        except: 
            return {"message":"failed to connect"} ,500   
        # recieve watson result , send it back 



class  Hotel_Indexer(Resource):
    def post(self):
        # runs automatically 
        # uses elastic search 
        return {'message':'not yet emplemented'},501

URLs_tone_analayzer= "/tone_analyzer/<hotel_name>"
URLs_hotel_indexer= "/Hotel_Indexer/<indexby>"

api.add_resource(Hotel_Tone_Analyzer,URLs_tone_analayzer)
api.add_resource(Hotel_Indexer,URLs_hotel_indexer)

if __name__ == '__main__':
    hotel_list = pd.read_csv(file_path)
    app.run(debug=True)   # change before final upload 