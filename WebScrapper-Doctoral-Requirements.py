import requests 
from bs4 import BeautifulSoup, NavigableString
import re 
import csv




URL = "https://www.etsu.edu/gradschool/doctoral-degrees.php"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

programsResult = soup.find('main')

for program in programsResult.find_all('details'):

	 programName = program.find('summary').get_text().strip()
	 if programName == "Audiology - Au.D.":
		 #print(program.text)
		 strValue = program.text 
		 before, sep, after = strValue.partition("Requirements")

		 if len(after) >0:
			 strValue = after

		 print(strValue)