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
		data = {	"auth_key": key,
					"target_lang": lang,
					"text": text }
		return(data)	


def _handle_response_json(api, response):
	if(api=="deepl"):
			json_response = response.json()
			translation = json_response["translations"][0]["text"]
			return(translation)
			

#my_translation = query_deepl("EN", "Gesundheit ist ein Zustand des vollkommenen körperlichen, geistigen und sozialen Wohlbefindens"
#					+" - und nicht die bloße Abwesenheit von Krankheit.")
#print(my_translation)