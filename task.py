##############
#### URL Checke ####
#################
## Goes through all amEmbed_JS URLs to make sure they are good ##
## Will expand to checking others too ## 
##############
## Ticket: https://www.notion.so/automedia/QA-Make-a-404-check-service-for-amEmbed-JS-jasp-e803258166374c9bb84e4f3d57e847af 
#############

## Declarations 
import os
from airtable import Airtable
import json
import requests

# Airtable settings 
base_key = os.environ.get("PRIVATE_BASE_KEY")
table_name = os.environ.get("PRIVATE_TABLE_NAME")
api_key = os.environ.get("PRIVATE_API_KEY")
airtable = Airtable(base_key, table_name, api_key) #For production env

#Airtable variables so if name changes will be easy to update here 
viewToCheck = 'Embeds - JS'
statusColumn = 'amService_RunStatus'
statusGood = 'Standby'
statusFail = 'Error - QA' #ie QA failed not actual amEmbed service 

def checkLoop(viewToCheck=viewToCheck, statusColumn=statusColumn, statusGood=statusGood, statusFail=statusFail):
	allRecords = airtable.get_all(view=viewToCheck) #get all data
	for i in allRecords:
			if "Prod_Ready" in i["fields"]: #Only working on prod ready ie checkboxed
				payload = i["fields"]["payload"]
				rec_ofAsked = i["id"]
				r = requests.get(payload)
				if r:
					# print('All good')
					fields = {statusColumn: statusGood}
					airtable.update(rec_ofAsked, fields)
				else:
					# print('URL not good')
					fields = {statusColumn: statusFail}
					airtable.update(rec_ofAsked, fields)

checkLoop()


### Testing Section 
#Bad URLs to test 
# http://httpbin.org/status/404
# https://ourworldindata.org/grapher/external-movement-covid?time=latest&region=Asia
# https://public.flourish.studio/story/212110/embed#slide-0