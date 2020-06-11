try:
	import requests
	import json
except ImportError as e:
	print("Exception Import ")
	print("Args", e.args)
	print("Name", e.name)
	print("Path", e.path)
	exit(-1)


###############################################################################
#This function return '' if value is None
###############################################################################
def convertString(value):
	return ('' if value is None else value)

###############################################################################
#This function return 0 if value is None
###############################################################################
def convertInt(value):
	return int(0 if value is None else value)

###############################################################################
#This function filter data by String value in particular field	
###############################################################################
def filterDictStringValue(varDict, varfield, varComparetation, varValue):
	if(varComparetation=='like'):
		return list( filter(lambda item: convertString(item[varfield]).find(varValue)>=0, varDict))
	elif(varComparetation=='=='):
		return list( filter(lambda item: convertString(item[varfield])==varValue, varDict))
		
###############################################################################
#This function filter data by Int value in particular field
###############################################################################
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

###############################################################################
#This function filter data
###############################################################################
def filterDict(varDict, varfield, varComparetation, varValue):
	if(varValue.isnumeric()==True):
		return filterDictIntValue(varDict, varfield, varComparetation, varValue)
	elif(varValue.isalpha()==True):
		return filterDictStringValue(varDict, varfield, varComparetation, varValue)


###############################################################################
#Class get is working to get data from http://www.balldontlie.io/
###############################################################################
class get():
	###########################################################################
	#Contruct a class with uri
	###########################################################################
	def __init__(self, uri):
		self.uri=uri
	
	###########################################################################
	#This execute a method get rest 
	###########################################################################
	def call(self):	
		if(self.act==1):
			self.response=requests.get(self.uri+'?per_page='+str(self.per_page)+'&page='+str(self.page))
		elif (self.act==2):
			self.response=requests.get(self.uri+'/{}'.format(self.varId))
	
	###########################################################################
	#This method execute get all item
	###########################################################################
	def GetAll(self, max=25, page=0):
		try:
			self.act=1
			assert max>=0 and max<=100
			self.per_page=max
			self.page=page
			self.call()
		except AssertionError:
			print("Number per pages must be between 1 and 100")
	
	###########################################################################
	#This method execute get by Id
	###########################################################################
	def GetById(self, varId):
		self.act=2
		self.varId=varId
		self.call()

###############################################################################
#Instancing a Class get from www.balldontlie.io
###############################################################################
endpoint="https://www.balldontlie.io/api/v1/players"
GetPlayers= get(endpoint)

#Execute GetPlayers for differents parameters
for tuple1 in [(300, 2), (30, 3), (100, 0)]:
	try:
		GetPlayers.GetAll(tuple1[0], tuple1[1])
		if(GetPlayers.response.status_code==200):
			print("All Players max. item={} and page={}".format(tuple1[0], tuple1[1]))
			for value in GetPlayers.response.json()['data']:
				print(json.dumps(value, indent=4))
		print("End of Items")
	except:
		print("Exception handling")
print()

data=GetPlayers.response.json()['data']
#Filter Data which first_name is like 'Mi'
filterData=filterDict(data, 'first_name', 'like', 'Mi')
print()
print('Players whose first name like Mi')
print(json.dumps(filterData))
print()

#Filter Data which first_name is equal to 'Gary'
filterData=filterDict(data, 'first_name', '==', 'Gary')
print()
print('Players whose first name is Gary')
print(json.dumps(filterData))
print()

#Filter Data which height_feet is less than 6
filterData= filterDict(data, 'height_feet', '<', '6')
print()
print('Players whose height in feet is less than 6')
print(json.dumps(filterData))
print()

filterData= filterDict(data, 'height_feet', '>', '5')
print()
print('Players whose height in feet is more than 5')
print(json.dumps(filterData))
print()

filterData= filterDict(data, 'height_feet', '>', '6')
print()
print('Players whose height in feet is more than 6')
print(json.dumps(filterData))
print()

###############################################################################
#Get player by Id
###############################################################################
GetPlayers.GetById(448)
print()
print("Player Id 448", json.dumps(GetPlayers.response.json(), indent=4))
print()
data=GetPlayers.response.json()



###############################################################################
#Modifying a player
###############################################################################
data.update({'first_name':'Gary Jim'})
data.update({'weight_pounds':165})
data.update({'height_feet':5})
data.update({'height_inches':9})
print()
print("Data Changed", json.dumps(data, indent=4))
print()
###############################################################################
#Write a player in a file
###############################################################################
try:
	fp = open('output.json', 'w')
	fp.write(json.dumps(data, indent=4))
	fp.close()
except IOError:
	print('File output.json can not create or write')


#Getting Teams
endpoint="https://www.balldontlie.io/api/v1/teams"
GetTeams= get(endpoint)

#Execute GetTeams for differents parameters
for tuple1 in [(300, 2), (12, 0), (6, 0)]:
	try:
		GetTeams.GetAll(tuple1[0], tuple1[1])
		if(GetTeams.response.status_code==200):
			print("All Teams max. item={} and page={}".format(tuple1[0], tuple1[1]))
			for value in GetTeams.response.json()['data']:
				print(json.dumps(value, indent=4))
			print("End of Items")
	except:
		print("Exception handling")


#Getting Games
endpoint="https://www.balldontlie.io/api/v1/games"
GetGames= get(endpoint)

#Execute GetGames for differents parameters
for tuple1 in [(300, 2), (12, 0), (2, 2)]:
	try:
		GetGames.GetAll(tuple1[0], tuple1[1])
		if(GetGames.response.status_code==200):
			print("All Games max. item={} and page={}".format(tuple1[0], tuple1[1]))
			for value in GetGames.response.json()['data']:
				print(json.dumps(value, indent=4))
			print("End of Items")
	except:
		print("Exception handling")