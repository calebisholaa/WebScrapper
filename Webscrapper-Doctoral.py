import requests
from bs4 import BeautifulSoup, NavigableString
import re
import csv
class GraduateProgram:
        def __init__(self, programName="", coordinatorName="", coordinatorPhone="",  coordinatorEmail="", deliveryMethod=""):
                self.programName = programName
                self.coordinatorName = coordinatorName
                self.coordinatorPhone = coordinatorPhone
                self.coordinatorEmail  = coordinatorEmail
                self.deliveryMethod = deliveryMethod


def between(cur, end):
	string = []
	while cur and cur != end:
		if isinstance(cur, NavigableString):
			text = cur.strip()
			if len(text) and text != "Coordinators" and text != "Phone:" and text != "Email:":
				string.append(text)
		cur = cur.next_element
	
	return string
              
graduateProgramList =[]

URL = "https://www.etsu.edu/gradschool/doctoral-degrees.php"
#URL = "https://www.etsu.edu/gradschool/masters-degrees.php"
#URL = "https://www.etsu.edu/gradschool/certificate-programs.php"


page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
#soup = BeautifulSoup(page.content, 'html5lib')
#soup = BeautifulSoup(page.content, 'lxml')


#gets all the programs offered
programsResult = soup.find('main')

for program in programsResult.find_all('details'):

        #programName - for example Audiology -Au.D, Biomedical Science -Ph.D
        programName = program.find('summary').get_text().strip()

        #If the program has only one Coordinator - this logic handles the Coordinator written with Space at the end
        if program.find(string="Coordinator ") != None:
                
                
                #Getting Coordinator Info
                #coordinatorInfo = program.find(string="Coordinator ").findNext('ul').contents[0].nextSibling.get_text()
                coordinatorInfo = program.find(string="Coordinator ").findNext('ul').contents[0].nextSibling.get_text()

                #testing for masters
                #print(coordinatorInfo)

                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)

                coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :emailIndex.start()].strip()
                coordinatorEmail = coordinatorInfo[emailIndex.start() + 7:].strip()

                #Getting Program Location/Delivery Method
                deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()
               
                gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)
                

                if gradProgram not in graduateProgramList:
                        graduateProgramList.append(gradProgram)


        #If the program has only one Coordinator - this logic handles the Coordinator written with no Space at the end
        elif program.find(string="Coordinator") != None:

                #Getting Coordinator Info
                coordinatorInfo = program.find(string="Coordinator").findNext('ul').contents[0].nextSibling.get_text()

                
                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)

                coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :emailIndex.start()].strip()
                coordinatorEmail = coordinatorInfo[emailIndex.start() + 7:].strip()

                #Getting Program Location/Delivery Method
                deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()

                gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)

                if gradProgram not in graduateProgramList:
                        graduateProgramList.append(gradProgram)   

        #If program has more than one coordinator this logic handles the Coordinator written with no Space at the end
        elif program.find(string="Coordinators") != None:

                coordinatorInfoList =between((program.find(string="Coordinators")),(program.find(string="Location/Delivery Method")))
                while(True):
                        if '-' in coordinatorInfoList[0]:
                                coordName = coordinatorInfoList[0].split('-')

                                programNameAndCon = programName
                                programNameAndCon += " ; "
                                programNameAndCon += coordinatorInfoList[1]

                        
                                  #Getting Program Location/Delivery Method
                                deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()
                                del coordinatorInfoList[1]



                                gradProgram = GraduateProgram(programNameAndCon, coordinatorInfoList[0], coordinatorInfoList[1], coordinatorInfoList[2],deliveryMethod)

                        else:
                                gradProgram = GraduateProgram(programNameAndCon, coordinatorInfoList[0], coordinatorInfoList[1], coordinatorInfoList[2],deliveryMethod)


                        if gradProgram not in graduateProgramList:
                                graduateProgramList.append(gradProgram)

                        del coordinatorInfoList[0]
                        del coordinatorInfoList[0]
                        del coordinatorInfoList[0]

                        if len(coordinatorInfoList) == 0:
                                break

                



      
with open('Programs_Coordinators_Doctoral.csv', mode='w') as csv_file:
	writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	
	writer.writerow(["Program Name - Type ; Concentration", "Coordinator's Name", "Coordinator's Phone Number", "Coordinator's Email"])
	
	for study in graduateProgramList:
		writer.writerow([study.programName,study.coordinatorName, study.coordinatorPhone, study.coordinatorEmail, study.deliveryMethod])       
        


