from flask import Flask , jsonify
from flask_restful import reqparse, abort, Api, Resource
import pandas as pd
from ibm_watson import ToneAnalyzerV3
from elasticsearch import Elasticsearch 
import os ,json


app = Flask(__name__)
api = Api(app)
es=Elasticsearch([{'host':'localhost','port':9200}])

file_path  = "hotels_noindex.csv"
watson_url = "https://gateway-lon.watsonplatform.net/tone-analyzer/api"
watson_key = "key goes here"

class Hotel_Tone_Analyzer(Resource):
    def post(self,hotel_name):
        print("---Hotel analyser---")
        
        # 1.extract hotel data
        print("name:" + hotel_name)
        hotel_data = hotel_list[hotel_list["name"]== hotel_name]
        hotel_review = hotel_data["reviews.text"]
        print(hotel_review.head())
        # 2.create json/ string 
        watson_input = hotel_review.to_json()
        
        # 3.send it to watson
        tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey=watson_key,
            url=watson_url)
        try : 
            #watson 
            print("requesting tone analysis")
            watson_responce = tone_analyzer.tone(
                    {'text':watson_input} , 
                    content_language='en', sentences=False, 
                    content_type="application/json").get_result()
            print("watson responded" )

            return (watson_responce) ,200
        except: 
            return {"message":"failed to connect"} ,500   
        # recieve watson result , send it back 

class  Hotel_Indexer(Resource):
    def post(self,json_data):
        # uses elastic search
        load_dataset()
        try:
            print(res['result'])
            return 200
        return {'message':'not yet emplemented'},501
        
    '''def get(self,docid):
        res = es.get(index="hotel-list",doc_type="hotel",id=docid)
        return {'message':'not yet emplemented'},501
    def delete(self):
        return {'message':'not yet emplemented'},501'''
        


URLs_tone_analayzer= "/tone_analyzer/<hotel_name>"
URLs_hotel_indexer= "/Hotel_Indexer/"

api.add_resource(Hotel_Tone_Analyzer,URLs_tone_analayzer)
api.add_resource(Hotel_Indexer,URLs_hotel_indexer)

def create_index(es_object, index_name='recipes'):
    created = False
    # index settings
    fields = "address,categories,city,country,latitude,longitude,name,postalCode,province".split(',')
    review_fields = ["date","dateAdded","doRecommend", "id" , "rating","text","title","userCity","username","userProvince"]
    
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "members": {
                "dynamic": "strict",
                "properties": {
                    "address": {"type": "nested"},
                    "categories": {"type": "nested"},
                    "city": {"type": "nested"},
                    "country": {"type": "nested"},
                    "latitude": {"type": "nested"},
                    "longitude": {"type": "nested"},
                    "name": {"type": "nested"},
                    "postalCode": {"type": "nested"},
                    "province":{"type":"nested"},
                    "reviews":{
                        "type":'nested',
                        "date":{"type":"text"},
                        "dateAdded":{"type":"text"},
                        "doRecommend":{"type":"text"},
                        "id":{"type":"text"},
                        "rating":{"type":"text"},
                        "text":{"type":"text"},
                        "title":{"type":"text"},
                        "userCity":{"type":"text"},
                        "username":{"type":"text"},
                        "userProvince":{"type":"text"}

                    }
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def load_dataset():
    i=0
    for json_name in os.listdir('hotel-database'):
        path = os.path.join('hotel-database',json_name)
        with open(path) as json_file:
            data = json.load(json_file)
        res = es.index(index='hotel-list',doc_type='hotel',id=i,body=data) 
        i = i+1 
        print(res)       


if __name__ == '__main__':
    hotel_list = pd.read_csv(file_path)
    
    app.run(debug=True)   # change before final upload 