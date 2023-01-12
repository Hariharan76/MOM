from fastapi import FastAPI
import pymongo
from summarizer import Summarizer
import pydantic
import os
import json
myclient = pymongo.MongoClient("mongodb:")
app = FastAPI()
mydb = myclient["Unifiedring"]
mycol = mydb["urr_meeting_closecaptions"]
model = Summarizer()
@app.get("/read_root")
def read_root(uuid: str): 
    try:              
        i = mycol.find_one({"uuid" :uuid})
        if i:                                               
            if i.get("MOM") is not None:                
                mom= i.get("MOM")
                mom1={"MOM":mom}
                return mom1
            else:
                b=""
                se=set()
                for item in i.get("transcripts"):                           
                    a=item.get("text") 
                    se.add("speakerName")                
                    b+=a    
                print(list(se))
                get_summary=b               
                result = model(get_summary, min_length=20)
                summary = "".join(result) 
                mycol.update_one({"uuid":uuid},{"$set": {"MOM":summary}},False,True)
                return{"MOM":summary}  
        else:
            return{"statusCode" : 422 , "message": f"No available meeting  {uuid}" }
    except:
          
        return  {"statusCode" : 500 , "message": "Internal server error" }

#q:A #mongodb://mongodb-st4:27017,mongodb-st5:27017,mongodb-st6:27017/Unifiedring?w=0&readPreference=nearest&replicaSet=vectreplica01&auto_reconnect=true
#stage:mongodb://mongo-test1:27017,mongo-test2:27017,mongo-test3:27017/Unifiedring?w=0&readPreference=nearest&replicaSet=replconfig01&auto_reconnect=true


                      


   




