import json
import jsonpath_ng
import classes
from classes import qgp_factory,survey_factory,form_factory, extract_values_survey, q_factory, replace_pt, flatten_one_level, question_group_instance_factory, question_instance_factory
from pprint import pprint
import copy
from response_SurveyDataPoints import dictio_forms_in_survey,dictio_qgs_in_forms,dictio_questions_in_a_form
from datetime import date 
#from maybe import generate_dictionaries_qgs

'''API CALL RESPONSE''' #This is one form instance answers (surveys are made up by form). 
api_url = 'https://api-auth0.akvo.org/flow/orgs/thehungerproject/form_instances?survey_id=400070001&form_id=385010001'

data = r'''{
	"formInstances": [
		{
			"formVersion": 1.0,
			"deviceIdentifier": "akvo-jonah",
			"dataPointId": "439350001",
			"submissionDate": "2022-10-04T08:21:08Z",
			"modifiedAt": "2022-10-04T09:36:04.187Z",
			"id": "405190001",
			"responses": {
				"388540002": [
					{
						"404010076": [
							{
								"text": "Microfinanças & meios de vida"
							}
						],
						"404010081": 12.0,
						"404010084": [
							{
								"text": "Contabilidade"
							}
						],
						"398220065": 12.0
					}
				],
				"388540003": [
					{
						"382720001": {
							"filename": "https://akvoflow-211.s3.amazonaws.com/images/41a0e1e5-08af-4c77-89ae-cbe9a6fcacb1.jpg",
							"location": null
						},
						"382720002": "12",
						"382720003": [
							{
								"text": "Médio"
							}
						]
					}
				],
				"388540001": [
					{
						"386430059": "2022-10-04T08:19:37.673Z",
						"386430060": "t",
						"386430061": [
							{
								"text": "Malindile"
							}
						],
						"386430062": [
							{
								"text": "Treinamento de Treinadoress (ToT)"
							}
						],
						"386430063": [
							{
								"text": "Comunidade"
							}
						],
						"386430064": {
							"lat": -1.3582283333333334,
							"long": 36.92758333333334,
							"elev": 1428.8,
							"code": null
						}
					}
				]
			},
			"identifier": "qbat-drrt-r1be",
			"displayName": "Malindile",
			"formId": "385010001",
			"surveyalTime": 99,
			"submitter": "akvo-jonah",
			"createdAt": "2022-10-04T09:35:59.556Z"
		}
	],
	"nextPageUrl": "https://api-auth0.akvo.org/flow/orgs/thehungerproject/form_instances?survey_id=400070001&form_id=385010001&cursor=CjASKmoOZX5ha3ZvZmxvdy0yMTFyGAsSDlN1cnZleUluc3RhbmNlGPHqmsEBDBgAIAA"
}'''

data =  json.loads(data)	

#	instance.__eq__()

#Create a dictionary of question groups
d_form_instances = {}

for form_instance in data["formInstances"]:
	parent_id = form_instance['id']
	for id,questions in form_instance['responses'].items():
		d_form_instances[id]=question_group_instance_factory(id,questions,parent_id)


#Create a dictionary of questions, WITH THE ANSWERS UGLY
d_question_instaces = {}

for instance in d_form_instances.values():
	parent_id = instance.id
	for gq in instance.questions:
		for id,question in gq.items():
			d_question_instaces[id] =question_instance_factory(id,question,parent_id)

pprint(d_question_instaces['382720003'].describe())


class dvf_factory:

    def __init__(self):
        self._creators = {}

    def register_format(self, format, creator):
        self._creators[format] = creator

    def get_processor(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)

        return creator()

factory = dvf_factory()

class ListProcess():
	def __init__(self):
		self._current_object  = None

	def start_object(self, object_name):
		self._current_object = object_name

	def to_single_str_values(self):
		response = list(self.__dict__.values())[0][0].values()
		return (list(response)[0]) #THIS NEEDS TO BE IMPROVED

class DictionaryProcess():
	def __init__(self):
		self._current_object  = None

	def start_object(self, object_name):
		self._current_object = object_name

	def to_single_str_values(self):
		response = list(self.__dict__.values())
		return(response[0])

class StringProcess():
	def __init__(self):
		self._current_object  = None

	def start_object(self, object_name):
		self._current_object = object_name

	def to_single_str_values(self):
		response = 	response = list(self.__dict__.values())
		return(response[0])

class FloatProcess():
	def __init__(self):
		self._current_object  = None

	def start_object(self, object_name):
		self._current_object = object_name

	def to_single_str_values(self):
		response = 	response = list(self.__dict__.values())
		return(response[0])

class NoneProcess():
	def __init__(self):
		self._current_object  = None

	def start_object(self, object_name):
		self._current_object = object_name

	def to_single_str_values(self):
		response = 	response = list(self.__dict__.values())
		return(response[0]) # !!! Needs more control over what it means where?

class IntegerProcess():
	def __init__(self):
		self._current_object  = None

	def start_object(self, object_name):
		self._current_object = object_name

	def to_single_str_values(self):
		response = 	response = list(self.__dict__.values())
		return(response[0])

factory.register_format('LIST', ListProcess)
factory.register_format('DICTIONARY',DictionaryProcess)
factory.register_format('STRING',StringProcess)
factory.register_format('FLOAT',FloatProcess)
factory.register_format('NONE',NoneProcess)
factory.register_format('INTEGER',IntegerProcess)

class DataTypeProcessor:
    def process(self, serializable, format):
        processor = factory.get_processor(format)
        serializable.process(processor)
        return processor.to_single_str_values()

process = DataTypeProcessor()

def manage_response_structure(response_input):

	if isinstance(response_input, list):
		return("LIST")
	elif isinstance(response_input, str):
		return ("STRING")
	elif isinstance(response_input, dict):
		return ("DICTIONARY")
	elif isinstance(response_input, date):
		return ("DATE")
	elif isinstance(response_input, float):
		return ("FLOAT")
	elif isinstance(response_input, None):
		return ("NONE")
	elif isinstance(response_input, int):
		return ("INTEGER")
	else:
		raise ValueError(response_input,'date type:',type(response_input))

#Create a dictionary of questions, WITH THE ANSWERS BEAUTIFUL

for key in d_question_instaces.keys():
	clean_answer = process.process(d_question_instaces[key], manage_response_structure(d_question_instaces[key].answer))
	setattr(d_question_instaces[key], 'answer', clean_answer)

#print('Processed output:', Straits_Processed)
pprint("-----------------------------------")
pprint([x.describe() for x in d_question_instaces.values()])



'''
name = 't_question_group'

from collections import namedtuple
t_question_group = namedtuple(name, 'question_id answer')


pt1 = Point(1.0, 5.0)
pt2 = Point(2.5, 1.5)


l_q_answers = [[t_question_group(question,answer) for question, answer in question_group.questions[0].items()] for question_group in d_form_instances.values()]
l_q_answers = flatten_one_level(l_q_answers)

#[t_q_g.answer for ]

pprint(d_form_instances)
pprint("------------------")
pprint([gq.answer for gq in l_q_answers])

'''




