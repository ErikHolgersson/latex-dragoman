import json		
import requests
import os
# What to do?
# * Queries an DeepL/andere Übersetzer-API senden
# * Query-JSON mit Sprache und zu übersetzendem Text generieren
# * Übersetzung aus Antwort-JSON extrahieren und ausgeben



def queryDeepL(lang, text):
	url	= "https://api-free.deepl.com/v2/translate"
	data=__buildQueryJson("deepl", lang, text)	

	response = requests.get(url, data)

	translation = __handleResponseJson("deepl", response)
	return(translation)


def __buildQueryJson(api, lang, text):
	if(api=="deepl"):
		key = os.getenv("DEEPL_KEY")
		data = {	"auth_key": key,
					"target_lang": lang,
					"text": text }
		return(data)	


def __handleResponseJson(api, response):
	if(api=="deepl"):
			jsonResponse = response.json()
			translation = jsonResponse["translations"][0]["text"]
			return(translation)
			

myTranslation = queryDeepL("EN", "Gesundheit ist ein Zustand des vollkommenen körperlichen, geistigen und sozialen Wohlbefindens"
					+" - und nicht die bloße Abwesenheit von Krankheit.")
