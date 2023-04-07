import json
import jsonpath_ng

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



def extract_values_survey(json_input:json, jsonpath:str):
	'''This function take a json response and uses jsonpath_ng to parse for a response'''

	response_input = json.loads(json_input)
	jsonpath = jsonpath_ng.parse(jsonpath)
	matches = [match.value for match in jsonpath.find(response_input)]

	return(matches)

#á is not working
def replace_pt(word:str):
    word=word.replace(' ','_').replace('á','a').replace('ç','c').replace('ã','a').replace(':','').replace('?','').replace('.','').replace(
        '__','').replace('í','i').replace('ú','u').replace('á','a').replace('/','_').replace('á','a').lower()
    return(word)

def flatten_one_level(l):
    return [item for sublist in l for item in sublist]

'''
class Folder(Base):
    organization = "THP"

    @classmethod
    def describe_class(self):
        return (self.__dict__)

    __tablename__ = "folder"
    id = Column(Integer(15), primary_key=True)
    name = Column(Unicode(65))
    parentId = Column(Integer(15), nullable=True) #what is nullable?
    createdAt = Column(TIMESTAMP(30))
    modifiedAt =  Column(TIMESTAMP(30))
#   surveysURL = Column(Unicode(100))
    foldersUrl =  Column(Unicode(100))

    def __init__(self, id, name, parentId, createdAt, modifiedAt, foldersUrl):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
#       self.surveysUrl = surveysUrl do not use
        self.foldersUrl = foldersUrl #call this to get the site that feed class Survey



class Author(Base):

    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("Book", backref=backref("author"))
    publishers = relationship(
        "Publisher", secondary=author_publisher, back_populates="authors"
    )


    # Instance method
    def describe(self):
        return (self.__dict__)

def folder_factory(id,name,parentId, createdAt, modifiedAt, surveysUrl, foldersUrl):
    #error control?

    return Folder(id,name,parentId, createdAt, modifiedAt, surveysUrl, foldersUrl)
'''

class Survey:

    def __init__(self, id, name, parentId, createdAt, modifiedAt, surveyUrl):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
        self.surveyUrl = surveyUrl


        # Instance method
    def describe(self):
        return (self.__dict__)

    #DO something like this
    #def get_qgroup_names(self):
    #    return ([qg['name'] for qg in self.questionGroups])

def survey_factory(id, name, parentId, createdAt, modifiedAt, surveyUrl):
    #error control?

    return Survey(id, name, parentId, createdAt, modifiedAt, surveyUrl)

class Folder:
    organization = "THP"

    @classmethod
    def describe_class(self):
        return (self.__dict__)

    def __init__(self, id, name, parentId, createdAt, modifiedAt, foldersUrl):
        self.id = id
        self.name = name
        self.parentId = parentId
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
        #self.surveysUrl = surveysUrl do not use
        self.foldersUrl = foldersUrl #call this to get the site that feed class Survey

    # Instance method
    def describe(self):
        return (self.__dict__)

def folder_factory(id,name,parentId, createdAt, modifiedAt, foldersUrl):
    #error control?

    return Folder(id,name,parentId, createdAt, modifiedAt, foldersUrl)


class Form:

    def __init__(self, id, name, questionGroups, version, createdAt, modifiedAt, formInstancesUrl, parentId):
        self.id = id
        self.name = name
        self.questionGroups = questionGroups
        self.version = version
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
        self.formInstancesUrl = formInstancesUrl
        self.parentId = parentId

        # Instance method
    def describe(self):
        return (self.__dict__)

    #Get you a list of the question group names
    def get_qgroup_names(self):
        return ([qg['name'] for qg in self.questionGroups])

def form_factory(id, name, questionGroups, version, createdAt, modifiedAt, formInstancesUrl, parent_id,):
    #error control?

    return Form(id, name, questionGroups, version, createdAt, modifiedAt, formInstancesUrl, parent_id,)

class QuestionGroup:

    def __init__(self, id, name, repeatable, questions, createdAt, modifiedAt, parentId):
        self.id = id
        self.name = name
        self.repeatable = repeatable
        self.questions = questions
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
        self.parentId = parentId

    # Instance method
    def describe(self):
        return (self.__dict__)

    def get_question_names(self):
        return ([question['name'] for question in self.questions])

    def __eq__(self, other):
        return ((self.id) == (other.id))    
     
def qgp_factory(id, name, repeatable, questions, createdAt, modifiedAt, parent_id):
    #error control?

    return QuestionGroup(id, name, repeatable, questions, createdAt, modifiedAt, parent_id)

class Question: 
    def __init__(self, createdAt, id, modifiedAt, name, order, personalData, type, variableName, parentId):
        self.id = id
        self.name = name
        self.type = type
        self.order = order
        self.variableName = variableName
        self.personalData = personalData
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
        self.parentId = parentId

    # Instance method
    def describe(self):
        return (self.__dict__)

def q_factory(createdAt, id, modifiedAt, name, order, personalData, type, variableName, parent_id):
    
    #error control?
    return Question(createdAt, id, modifiedAt, name, order, personalData, type, variableName, parent_id)

class FormInstance:
    def __init__(self, formVersion, deviceIdentifier, modifiedAt, dataPointId, submissionDate, 
    id, responses, identifier, displayName, formId, surveyalTime, submitter, createdAt):

        self.formVersion = formVersion
        self.deviceIdentifier = deviceIdentifier
        self.dataPointId = dataPointId
        self.submissionDate = submissionDate
        self.modifiedAt = modifiedAt
        self.id = id
        self.responses = responses
        self.identifier = identifier
        self.displayName = displayName
        self.formId = formId
        self.surveyalTime = surveyalTime
        self.submitter = submitter
        self.createdAt = createdAt
#       self.parentId = parentId ??

    # Instance method
    def describe(self):
        return (self.__dict__)

class QuestionGroupInstance:

    def __init__(self, id, questions,parentId):
        self.id = id
        self.questions = questions
        self.parentId = parentId

    def __eq__(self, other):
        return ((self.id) == (other.id)) 

    def describe(self):
        return (self.__dict__)
    
def question_group_instance_factory(id, questions,parentId):

    #error control?
    return QuestionGroupInstance(id, questions,parentId)



class InstanceQuestion:

    def __init__(self, id, answer,parentId):
        self.id = id
        self.answer = answer
        self.parentId = parentId

    def __eq__(self, other):
        return ((self.id) == (other.id)) 

    def process(self, processor):
        processor.start_object(self.answer)

    def describe(self):
        return (self.__dict__)


def question_instance_factory(id, questions, parent_id):

    #error control?
    return InstanceQuestion(id, questions, parent_id)
