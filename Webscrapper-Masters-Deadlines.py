import requests
from bs4 import BeautifulSoup, NavigableString
import re 
import csv 



URL = "https://www.etsu.edu/gradschool/masters-degrees.php"


page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

programsResult = soup.find('main')
csv_file = open('Masters_deadlines.csv', mode='w')
writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')		
for program in programsResult.find_all('details'):

    try:
        programName = program.find('summary').get_text().strip()


        requirements = program.text
        deadlineTableLabels = program.find(string="Deadlines (11: 59 p.m. ET)").findNext('thead').get_text().replace(' ', '').split('\n')
        deadlineTableDates = program.find(string="Deadlines (11: 59 p.m. ET)").findNext('tbody').get_text().replace(' ', '').split('\n')

        deadlineTableLabels = [x for x in deadlineTableLabels if x != '']
        deadlineTableDates = [x for x in deadlineTableDates if x != '']

        size = len(deadlineTableLabels)
        deadlineTableDates = [deadlineTableDates[i * size:(i + 1) * size] for i in range((len(deadlineTableDates) + size - 1) // size )]

        writer.writerow([programName])
        writer.writerow(deadlineTableLabels)
        writer.writerows(deadlineTableDates)
        writer.writerow([" "])
    except:
        		# Something went wrong if ther other rows are blank besides the name
	    writer.writerow([programName])
		

		
  
   
   
    