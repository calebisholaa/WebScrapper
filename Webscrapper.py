import requests
from bs4 import BeautifulSoup
import re
class GraduateProgram:
        def __init__(self, programName="", coordinatorName="", coordinatorPhone="",  coordinatorEmail=""):
                self.programName = programName
                self.coordinatorName = coordinatorName
                self.coordinatorPhone = coordinatorPhone
                self.coordinatorEmail  = coordinatorEmail
                
              
graduateProgramList =[]
URL = "https://www.etsu.edu/gradschool/doctoral-degrees.php"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


#gets all the programs offered
programsResult = soup.find('main')

for program in programsResult.find_all('details'):

        #programName - for example Audiology -Au.D, Biomedical Science -Ph.D
        programName = program.find('summary').get_text().strip()

        #If the program has only one Coordinator
        if program.find(string="Coordinator ") != None:
                
                #Getting Coordinator Info
                coordinatorInfo = program.find(string="Coordinator ").findNext('ul').contents[0].nextSibling.get_text()


                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)

                coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :emailIndex.start()].strip()
                coordinatorEmail = coordinatorInfo[emailIndex.start() + 7:].strip()

                #Getting Program Location/Delivery Method

                gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail)

                if gradProgram not in graduateProgramList:
                        graduateProgramList.append(gradProgram)

        elif program.find(string="Coordinator") != None:

                  #Getting Coordinator Info
                coordinatorInfo = program.find(string="Coordinator").findNext('ul').contents[0].nextSibling.get_text()


                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)

                coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :emailIndex.start()].strip()
                coordinatorEmail = coordinatorInfo[emailIndex.start() + 7:].strip()

                #Getting Program Location/Delivery Method

                gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail)

                if gradProgram not in graduateProgramList:
                        graduateProgramList.append(gradProgram)





for study in graduateProgramList:
        print(study.programName, study.coordinatorName, study.coordinatorPhone, study.coordinatorEmail)
        
        


