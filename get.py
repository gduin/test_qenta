import requests
import json

#This function return '' if value is None
def convertString(value):
	return ('' if value is None else value)

#This function return 0 if value is None
def convertInt(value):
	return int(0 if value is None else value)

#This function filter data by String value in particular field	
def filterDictStringValue(varDict, varfield, varComparetation, varValue):
	if(varComparetation=='like'):
		return list( filter(lambda item: convertString(item[varfield]).find(varValue)>=0, varDict))
	elif(varComparetation=='=='):
		return list( filter(lambda item: convertString(item[varfield])==varValue, varDict))
		
#This function filter data by Int value in particular field		
def filterDictIntValue(varDict, varfield, varComparetation, varValue):
	varValue=int(varValue)
	if(varComparetation=='<'):
		return list( filter(lambda item: convertInt(item[varfield]) > 0 and convertInt(item[varfield]) < varValue, varDict))
	elif (varComparetation=='<='):
		return list( filter(lambda item: convertInt(item[varfield]) > 0 and convertInt(item[varfield]) <= varValue, varDict))
	elif (varComparetation=='>'):
		return list( filter(lambda item: convertInt(item[varfield]) > varValue, varDict))
	elif (varComparetation=='>='):
		return list( filter(lambda item: convertInt(item[varfield]) >= varValue, varDict))
	else:
		return list( filter(lambda item: convertInt(item[varfield]) == varValue, varDict))

#This function filter data
def filterDict(varDict, varfield, varComparetation, varValue):
	if(varValue.isnumeric()==True):
		return filterDictIntValue(varDict, varfield, varComparetation, varValue)
	elif(varValue.isalpha()==True):
		return filterDictStringValue(varDict, varfield, varComparetation, varValue)

#Class get is working to get data from http://www.balldontlie.io/

class get():
	
	def __init__(self, uri):
		self.uri=uri
		
	def call(self):	
		if(self.act==1):
			self.response=requests.get(self.uri+"?per_pages="+str(self.per_pages))
		elif (self.act==2):
			self.response=requests.get(self.uri+"/{}".format(self.varId))
	
	def GetAll(self, max=25):
		try:
			self.act=1
			assert max>=0 and max<=100
			self.per_pages=max
			self.call()
		except AssertionError:
			print("Number per pages must be between 1 and 100")
		
	def GetById(self, varId):
		self.act=2
		self.varId=varId
		self.call()


endpoint="https://www.balldontlie.io/api/v1/players"
GetPlayers= get(endpoint)

GetPlayers.GetAll(100)

print(GetPlayers.response)
if(GetPlayers.response.status_code=='200'):
	print("All Players")
	for value in GetPlayers.response.json()['data']:
		print(value)
	 
data=GetPlayers.response.json()['data']
#Filter Data which first_name is like 'Mi'
filterData=filterDict(data, 'first_name', 'like', 'Mi')
print('Players whose first name like Mi')
print(filterData)
print()

#Filter Data which first_name is equal to 'Gary'
filterData=filterDict(data, 'first_name', '==', 'Gary')
print('Players whose first name is Gary')
print(filterData)
print()


filterData= filterDict(data, 'height_feet', '<', '6')
print('Players whose height in feet is less than 6')
print(filterData)
print()

filterData= filterDict(data, 'height_feet', '>', '5')
#list( filter(lambda item: convertInt(item['height_feet'])>5, data))
print('Players whose height in feet is more than 5')
print(filterData)
print()

filterData= filterDict(data, 'height_feet', '>', '6')
#list( filter(lambda item: convertInt(item['height_feet'])>6, data))
print('Players whose height in feet is more than 6')
print(filterData)
print()

GetPlayers.GetById(448)
print("Data del Id 448", GetPlayers.response.json())
data=GetPlayers.response.json()
for key, value in GetPlayers.response.json().items():
	 print(key, value)

data.update({'first_name':'Gary Jim'})
data.update({'weight_pounds':165})
data.update({'height_feet':5})
data.update({'height_inches':9})

print("Data Changed", data)
try:
	fp = open('output.json', 'w')
	fp.write(json.dumps(data, indent=4))
	fp.close()
except IOError:
	print('File output.json can not create or write')


