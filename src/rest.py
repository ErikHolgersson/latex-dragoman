import json		
import requests
import os
# What to do?
# * Queries an DeepL/andere Übersetzer-API senden
# * Query-JSON mit Sprache und zu übersetzendem Text generieren
# * Übersetzung aus Antwort-JSON extrahieren und ausgeben



def query_deepl(lang, text):
	url	= "https://api-free.deepl.com/v2/translate"
	data=_build_query_json("deepl", lang, text)	

	response = requests.get(url, data)

	translation = _handle_response_json("deepl", response)
	return(translation)


def _build_query_json(api, lang, text):
	if(api=="deepl"):
		key = os.getenv("DEEPL_KEY")
		data = []

		data.append( ("auth_key", key) )
		data.append( ("target_lang", lang) )

		print("Text-Variable-Type: " + str(type(text)))
		if type(text) is str:
			data.append( ("text", text) )
		
		if type(text) is list:
			for entry in text:
				data.append( ("text", entry) )
		
		return(data)


def _handle_response_json(api, response):
	if(api=="deepl"):
			json_response = response.json()
			translation = []
			for entry in json_response["translations"]:
				translation.append(entry["text"])
			return(translation)
			

test_list= ["paranoid", "space caravan", "warpigs", "iron man"]
mytext= _build_query_json("deepl", "DE", test_list)
print(mytext)
my_translation = query_deepl("DE", test_list)
print(my_translation)