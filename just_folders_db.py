import json
import jsonpath_ng
from datetime import datetime

import sqlalchemy as sqlalc
from sqlalchemy import Column, INTEGER, Integer,ForeignKey, Table, VARCHAR, TIMESTAMP, MetaData, create_engine, inspect, cast, select, SmallInteger
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pprint import pprint

url = 'mysql://dccampbellf:Dojo2020!@127.0.0.1/dbclay_akvo'
engine = create_engine(url, echo=True)
connection = engine.connect()

CC_local_base = declarative_base(bind=engine)

'''
pprint(CC_local_base)
pprint("---------------")
akvo_table = sqlalc.Table('person_tbl',sqlalc.MetaData(), autoload=True, autoload_with=engine)
pprint(akvo_table)
pprint("---------------")
pprint("QUERY")
query = sqlalc.select([akvo_table]) 
pprint(query)
pprint("---------------")
pprint("execute query")
ResultProxy = connection.execute(query)
pprint(ResultProxy)
pprint("---------------")
pprint("Results")
pprint(ResultProxy.fetchall())
'''

#Methods for cleaning and controlling
def clean_time_akvo_feed(datetime_str):
    try:
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return(datetime_object)
    except:
        raise ValueError(datetime_str)

#This can be ignored, Pablo, I am trying to map the relationship between the data and created a dummy Survey Table which is significantly simpler than the real one
class Survey_IDDS(CC_local_base):
    __tablename__ = "Survey_IDDS"
    id = Column(Integer, primary_key=True)
    
    def __init__(self, id):
        self.id = id

#Ignore
def survey_idds_factory(id):
    #error control?

    return Survey_IDDS(id)

'''This is a good example of the work ahead -- this actually maps and has fed the database based off an object'''
class Folder(CC_local_base):
    __tablename__ = "folder_alt"
    id = Column(Integer, primary_key=True) #got rid of the (10) got says integer takes no values
    name = Column(VARCHAR, default='place-holder') #collation='utf8mb4_unicode_ci',nullable = False) 
    parentId = Column(Integer, nullable=False) #got rid of the (10) got says integer takes no values, ForeignKey('Survey_IDDS.id', ondelete='CASCADE') 
    createdAt = Column(TIMESTAMP(30), nullable=False)
    modifiedAt =  Column(TIMESTAMP(30), nullable = False)
#   surveysURL = Column(Unicode(100))
    foldersUrl =  Column(VARCHAR(100)),
     #(parentId) REFERENCES survey(id)

    def __init__(self, id, name, parentId, createdAt, modifiedAt, foldersUrl):
        self.id = id
        self.name = name # !!! #ADD BACK IN
        self.parentId = parentId
        self.createdAt = createdAt  
        self.modifiedAt = modifiedAt
#       self.surveysUrl = surveysUrl #DO NOT USE
        self.foldersUrl = foldersUrl #call this to get the site that feed class Survey

    def describe(self):
        return (self.__dict__)

def folder_factory(id,parentId, createdAt, modifiedAt,  foldersUrl):
    #error control?

    return Folder(id=id,parentId=parentId, name='place-holder', createdAt=clean_time_akvo_feed(createdAt), modifiedAt=clean_time_akvo_feed(modifiedAt),  foldersUrl=foldersUrl)

CC_local_base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()

#put back name
'''API CALL'''
url= 'https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders'
data = r'''
{
	"folders": [
		{
			"id": "352980002",
			"name": "Mozambique",
			"parentId": "0",
			"createdAt": "2022-04-21T08:17:49.746Z",
			"modifiedAt": "2022-06-14T07:56:47.516Z",
			"surveysUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/surveys?folder_id=352980002",
			"foldersUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders?parent_id=352980002"
		},
		{
			"id": "132140086",
			"name": "WASH Surveys",
			"parentId": "0",
			"createdAt": "2020-09-14T15:18:02.378Z",
			"modifiedAt": "2020-09-14T15:18:15.869Z",
			"surveysUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/surveys?folder_id=132140086",
			"foldersUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders?parent_id=132140086"
		},
		{
			"id": "112030011",
			"name": "Test Survey",
			"parentId": "0",
			"createdAt": "2020-09-09T20:32:40.700Z",
			"modifiedAt": "2020-09-09T20:33:19.714Z",
			"surveysUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/surveys?folder_id=112030011",
			"foldersUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders?parent_id=112030011"
		},
		{
			"id": "134010004",
			"name": "Her Choice Monitoring Forms",
			"parentId": "0",
			"createdAt": "2020-09-10T14:34:57.268Z",
			"modifiedAt": "2020-09-10T14:38:23.847Z",
			"surveysUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/surveys?folder_id=134010004",
			"foldersUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders?parent_id=134010004"
		},
		{
			"id": "189110140",
			"name": "Training Registration  2021",
			"parentId": "0",
			"createdAt": "2021-04-05T08:01:56.674Z",
			"modifiedAt": "2021-04-05T08:02:28.898Z",
			"surveysUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/surveys?folder_id=189110140",
			"foldersUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders?parent_id=189110140"
		},
		{
			"id": "102010001",
			"name": "Evaluations",
			"parentId": "0",
			"createdAt": "2020-09-09T19:18:56.016Z",
			"modifiedAt": "2020-09-09T19:22:09.346Z",
			"surveysUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/surveys?folder_id=102010001",
			"foldersUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/folders?parent_id=102010001"
		}
	]
}'''
data = json.loads(data)

jsonpath_expression = jsonpath_ng.parse("$..*")
data  = [match.value for match in jsonpath_expression.find(data)]#[0]?

#the second list is a bunch of code for their website that is of on use to use for this exercise
data = data[0]

#get and transform the names of the folders to name the Folder() class instances
names_of_folders = [result['name'] for result in data]
names_of_folders = [name.replace(' ','_').lower() for name in names_of_folders]

#generate the folder class instances.
folders_l = [folder_factory(id=result['id'], parentId=result['parentId'], createdAt=result['createdAt'], modifiedAt=result['modifiedAt'], foldersUrl=result['foldersUrl']) for result in data] 
folders_d = {}

#add back result['name']

#create a dictionary that links each Folder() class instantiation to the names of the folders in a dictionary
for name,instanciation in zip(names_of_folders,folders_l): 
    folders_d[name] = instanciation

folders = list(folders_d.values())

#Ignore this line, this is tied to the dummy survey class above, for relationship mapping purposes
survey_with_just_ids = [survey_idds_factory(c.id) for c in folders_d.values()]


s.add_all(folders)
s.commit()




