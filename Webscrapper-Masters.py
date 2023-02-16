from distutils.filelist import findall
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
			if len(text) and text != "Coordinators" and text != "Phone:" and text != "Email:" and text != "Inquiries:" and text != "Forms:":
				string.append(text)
		cur = cur.next_element
	
	return string

def betweenFinds(cur, end):
	string = []
	while cur and cur != end:
		if isinstance(cur, NavigableString):
			text = cur.strip()
			if len(text) and text != "Coordinators" and text != "Phone:" and text != "Email:":
				string.append(text)
		cur = cur.next_element
	
	return string
def betweenNoEmails(cur, end):
    string = []
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text) and text != "Coordinators" and text != "Phone:" and text != "Inquiries:" and text != "Forms:" and text != "Email:":
                string.append(text)
        cur = cur.next_element
    return string

def countEmails(list):
        int;numberEmailsFound=0
        for item in list:
                emailsFound = re.findall(r'[\w\.-]+@[\w\.-]+', item)
                numberEmailsFound += len(emailsFound)
        return numberEmailsFound

def notOneEmail(list):
        bool;flag = False
        if list[4] == re.match(r'[\w\.-]+@[\w\.-]+',list[4]):
                flag = True

        return flag

def countInquires(list):
        int;count = 0
        for item in list:
            inquiresFound = re.findall(r'Inquiries:', item)
            count += len(inquiresFound)
        return count
              
def publicHealth(prgName):
    bool;flag = False
    
    if prgName == "Public Health - M.P.H.":
         flag = True  
         
        
    return flag

graduateProgramList =[]

URL = "https://www.etsu.edu/gradschool/masters-degrees.php"
#URL = "https://www.etsu.edu/gradschool/certificate-programs.php"
#URL ="https://www.etsu.edu/gradschool/online-degrees.php"
#URL ="https://www.etsu.edu/gradschool/non-degree.php"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

programsResult = soup.find('main')
int;m=0
for program in programsResult.find_all('details'):

        #programName - for example Audiology -Au.D, Biomedical Science -Ph.D
        programName = program.find('summary').get_text().strip()

        
     
        #If the program has only one Coordinator - this logic handles the Coordinator written with Space at the end
        if program.find(string="Coordinator ") != None:
            
              #Getting Coordinator Info
                coordinatorInfo = program.find(string="Coordinator ").findNext('ul').get_text()
                
     
                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)
                inquiriesIndex = re.search(r'Inquiries:', coordinatorInfo)
                formsIndex = re.search(r'Forms:', coordinatorInfo)
             
             #This logic handles a special case where the coordinator does not have a email, but forms and inqiries 
                if emailIndex == None:
                    coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                    coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :inquiriesIndex.start()].strip()
                    coordinatorInquiries = coordinatorInfo[inquiriesIndex.start() + 11 :formsIndex.start()].strip()
                    coordinatorForm = coordinatorInfo[formsIndex.start() + 7:].strip()
                    coordinatorEmail = "Inquiries: " + coordinatorInquiries +  " Form: " + coordinatorForm
                    

                else:
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
                coordinatorInfo = program.find(string="Coordinator").findNext('ul').get_text()
                
     
                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)
                inquiriesIndex = re.search(r'Inquiries:', coordinatorInfo)
                formsIndex = re.search(r'Forms:', coordinatorInfo)
             
             #This logic handles a special case where the coordinator does not have a email, but forms and inqiries 
                if emailIndex == None:
                    coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                    coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :inquiriesIndex.start()].strip()
                    coordinatorInquiries = coordinatorInfo[inquiriesIndex.start() + 11 :formsIndex.start()].strip()
                    coordinatorForm = coordinatorInfo[formsIndex.start() + 7:].strip()
                    coordinatorEmail = "Inquiries: " + coordinatorInquiries +  " Form: " + coordinatorForm
                    

                else:
                    coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                    coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :emailIndex.start()].strip()
                    coordinatorEmail = coordinatorInfo[emailIndex.start() + 7:].strip() 


                #Getting Program Location/Delivery Method
                deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()

                gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)
                

                if gradProgram not in graduateProgramList:
                        graduateProgramList.append(gradProgram)

         #If program has more than one coordinator this logic handles the Coordinator written with no Space at the end
        #If program has more than one coordinator this logic handles the Coordinator written with no Space at the end
       
        elif program.find(string="Coordinators ") != None:
                coordinatorInfoList =between((program.find(string="Coordinators ")),(program.find(string="Location/Delivery Method")))
                coordinatorInfoListdup = betweenFinds((program.find(string="Coordinators ")),(program.find(string="Location/Delivery Method")))
                numInquiries = countInquires(coordinatorInfoListdup)
                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)
                inquiriesIndex = re.search(r'Inquiries:', coordinatorInfo)    
                fromsIndex = re.search(r'Forms:', coordinatorInfo)
                 
                int;countEmailIndex =0
                countEmailIndex = len(re.findall('Email',coordinatorInfo))
                

                '''
                coordinatorWithNoEmail = betweenNoEmails((program.find(string="Coordinators")),program.find(string="Location/Delivery Method"))
                phoneIndexdup = re.search(r'Phone:', coordinatorWithNoEmail)
                inquiriesIndexdup = re.search(r'Inquiries:', coordinatorWithNoEmail)
                formsIndexdup = re.search(r'Forms:', coordinatorWithNoEmail)
               '''

                while(True):
                        if countEmails(coordinatorInfoList) >= 3:
                               
                                if '-' in  coordinatorInfoList[0]:
                                    if(numInquiries > 0):
                                        coordName =  coordinatorInfoList[0].split('-')

                                        programNameAndCon = programName
                                        programNameAndCon += " ; "
                                        programNameAndCon +=  coordinatorInfoList[1]

                                        del coordinatorInfoList[1]

                                        coordinatorName =  coordinatorInfoList[0]
                                        coordinatorPhone = coordinatorInfoList[1]
                                        
                                        coordinatorInquiries = coordinatorInfoList[2]
                                        coordinatorForm =   coordinatorInfoList[3]
                                        
                                        coordinatorEmail = "Inquiries: " + coordinatorInquiries +  " Form: " + coordinatorForm
                                        deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()
                                        gradProgram = GraduateProgram(programNameAndCon, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)
                                        
                                        if gradProgram not in graduateProgramList:
                                                 graduateProgramList.append(gradProgram)
                                      
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                       
                                       
                                        

                                        if len(coordinatorInfoList) == 0:
                                                break

                                        numInquiries-1
                                    else:
                                        coordName =  coordinatorInfoList[0].split('-')

                                        programNameAndCon = programName
                                        programNameAndCon += " ; "
                                        programNameAndCon +=  coordinatorInfoList[1]

                                        del coordinatorInfoList[1]

                                        coordinatorName =  coordinatorInfoList[0]
                                        coordinatorPhone = coordinatorInfoList[1]
                                        
                                        coordinatorEmail = coordinatorInfoList[2]

                                        deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()

                                        gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)

                                        if gradProgram not in graduateProgramList:
                                                graduateProgramList.append(gradProgram)
                                       
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]

                                        if len(coordinatorInfoList) == 0:
                                                break
                                        

                                else: 
                                        coordinatorName = coordinatorInfo[0 : phoneIndex.start()].strip()
                                        coordinatorPhone = coordinatorInfo[phoneIndex.start() + 7 :emailIndex.start()].strip()

                                        if emailIndex != None:                                     
                                           coordinatorEmail = coordinatorInfo[emailIndex.start() + 7:].strip() 

                                        #Getting Program Location/Delivery Method
                                           deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()

                                           gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)
                

                                
                                        if gradProgram not in graduateProgramList:
                                                graduateProgramList.append(gradProgram)
                                        
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]

                                        if len(coordinatorInfoList) == 0:
                                                break
                                

                        else:
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
        elif program.find(string="Coordinators") != None:
            if publicHealth(programName):
                coordinatorInfoList =between((program.find(string="Coordinators")),(program.find(string="SOPHAS Application Specialist")))
                coordinatorInfoListdup = betweenFinds((program.find(string="Coordinators")),(program.find(string="SOPHAS Application Specialist")))
                numInquiries = countInquires(coordinatorInfoListdup)
                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)
                inquiriesIndex = re.search(r'Inquiries:', coordinatorInfo)    
                fromsIndex = re.search(r'Forms:', coordinatorInfo)
                 
                int;countEmailIndex =0
                countEmailIndex = len(re.findall('Email',coordinatorInfo))





            else:

                coordinatorInfoList =between((program.find(string="Coordinators")),(program.find(string="Location/Delivery Method")))
                coordinatorInfoListdup = betweenFinds((program.find(string="Coordinators")),(program.find(string="Location/Delivery Method")))
                numInquiries = countInquires(coordinatorInfoListdup)
                phoneIndex = re.search(r'Phone:', coordinatorInfo)
                emailIndex = re.search(r'Email:', coordinatorInfo)
                inquiriesIndex = re.search(r'Inquiries:', coordinatorInfo)    
                fromsIndex = re.search(r'Forms:', coordinatorInfo)
                 
                int;countEmailIndex =0
                countEmailIndex = len(re.findall('Email',coordinatorInfo))
               

                '''
                coordinatorWithNoEmail = betweenNoEmails((program.find(string="Coordinators")),program.find(string="Location/Delivery Method"))
                phoneIndexdup = re.search(r'Phone:', coordinatorWithNoEmail)
                inquiriesIndexdup = re.search(r'Inquiries:', coordinatorWithNoEmail)
                formsIndexdup = re.search(r'Forms:', coordinatorWithNoEmail)
               '''

            while(True):
                        if countEmails(coordinatorInfoList) >= 3:
                               
                                if '-' in  coordinatorInfoList[0]:
                                    if(numInquiries > 0):
                                        coordName =  coordinatorInfoList[0].split('-')

                                        programNameAndCon = programName
                                        programNameAndCon += " ; "
                                        programNameAndCon +=  coordinatorInfoList[1]

                                        del coordinatorInfoList[1]

                                        coordinatorName =  coordinatorInfoList[0]
                                        coordinatorPhone = coordinatorInfoList[1]
                                        
                                        coordinatorInquiries = coordinatorInfoList[2]
                                        coordinatorForm =   coordinatorInfoList[3]
                                        
                                        coordinatorEmail = "Inquiries: " + coordinatorInquiries +  " Form: " + coordinatorForm
                                        deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()
                                        gradProgram = GraduateProgram(programNameAndCon, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)
                                        numInquiries-1

                                        if gradProgram not in graduateProgramList:
                                                 graduateProgramList.append(gradProgram)
                                      
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                       
                                       
                                        

                                        if len(coordinatorInfoList) == 0:
                                                break

                                        
                                    else:
                                        coordName =  coordinatorInfoList[0].split('-')

                                        programNameAndCon = programName
                                        programNameAndCon += " ; "
                                        programNameAndCon +=  coordinatorInfoList[1]

                                        del coordinatorInfoList[1]

                                        coordinatorName =  coordinatorInfoList[0]
                                        coordinatorPhone = coordinatorInfoList[1]
                                        
                                        coordinatorEmail = coordinatorInfoList[2]

                                        deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()

                                        gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)

                                        if gradProgram not in graduateProgramList:
                                                graduateProgramList.append(gradProgram)
                                       
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]
                                        del coordinatorInfoList[0]

                                        if len(coordinatorInfoList) == 0:
                                                break
                                        

                                else: 
                                     if(numInquiries > 0):
                                            coordinatorName = coordinatorInfoList[0]
                                            coordinatorPhone = coordinatorInfoList[1]
                                            coordinatorInquiries = coordinatorInfoList[2]
                                            coordinatorForm =   coordinatorInfoList[3]

                                            coordinatorEmail = "Inquiries: " + coordinatorInquiries +  " Form: " + coordinatorForm

                                        #Getting Program Location/Delivery Method
                                            deliveryMethod = program.find(string="Location/Delivery Method").findNext('ul').contents[0].nextSibling.get_text()

                                            gradProgram = GraduateProgram(programName, coordinatorName, coordinatorPhone, coordinatorEmail,deliveryMethod)
                                            numInquiries - 1

                                
                                            if gradProgram not in graduateProgramList:
                                                    graduateProgramList.append(gradProgram)
                                            
                                            del coordinatorInfoList[0]
                                            del coordinatorInfoList[0]
                                            del coordinatorInfoList[0]
                                            del coordinatorInfoList[0]

                                            if len(coordinatorInfoList) == 0:
                                                    break
                                

                        else:
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
                                        gradProgram = GraduateProgram(programName, coordinatorInfoList[0], coordinatorInfoList[1], coordinatorInfoList[2],deliveryMethod)

                                        
                                if gradProgram not in graduateProgramList:
                                        graduateProgramList.append(gradProgram)

                                del coordinatorInfoList[0]
                                del coordinatorInfoList[0]
                                del coordinatorInfoList[0]

                                if len(coordinatorInfoList) == 0:
                                        break
       

              


      
      
with open('Programs_Coordinators_Masters.csv', mode='w') as csv_file:
	writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	
	writer.writerow(["Program Name - Type ; Concentration", "Coordinator's Name", "Coordinator's Phone Number", "Coordinator's Email"])
	
	for study in graduateProgramList:
		writer.writerow([study.programName,study.coordinatorName, study.coordinatorPhone, study.coordinatorEmail, study.deliveryMethod])