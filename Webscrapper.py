import requests
from bs4 import BeautifulSoup

URL = "https://www.etsu.edu/gradschool/doctoral-degrees.php"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')



programsResult = soup.find('main')

for program in programsResult.find_all('details'):

        programName = program.find('summary').get_text().strip()
        print(programName)


