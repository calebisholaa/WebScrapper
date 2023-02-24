import requests 
from bs4 import BeautifulSoup, NavigableString
import re 
import csv

class ProgramRequirements:
		def __init__(self, programName="",  transcript="", recommendation="", gpa="", testScores="", personalState="", additionalReq=""):
				self.programName = programName		
				self.transcript = transcript
				self.recommendation = recommendation
				self.gpa = gpa
				self.testScores = testScores
				self.personalState = personalState
				self.additionalReq = additionalReq
				
		


graduateProgramList =[]
str;personalStatement=""


URL = "https://www.etsu.edu/gradschool/certificate-programs.php"


page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

programsResult = soup.find('main')

for program in programsResult.find_all('details'):

	programName = program.find('summary').get_text().strip()
	
		 #print(program.text)

	requirements = program.text
	before,sep, after = requirements.partition("Recommendations")
	if len(after) > 0:
		requirements = after

	#Get transcripts 
	transcript = program.text
	before,sep, after = transcript.partition("Transcripts")
	if len(after) > 0:
		transcript = after
    
	before,sep, after = transcript.partition("Recommendations")
	if len(before) >0:
		transcript = before
		transcript.strip()
	#print(strValue)

	#Get Recommendation
	recommendation = program.text
	before,sep, after = recommendation.partition("Recommendations")
	if len(after) > 0:
		recommendation = after

	before,sep, after = recommendation.partition("GPA")
	if len(before) > 0:
		recommendation = before
		recommendation.strip()

		
	#Get GPA
	gpa = program.text
	before,sep, after = gpa.partition("GPA")
	if len(after) > 0:
		gpa = after
	
	
	before,sep, after = gpa.partition("Test Scores")
	if len(before) > 0:
		gpa = before
		gpa.strip()


	#Test Scores
	testScores = program.text
	before,sep, after = testScores.partition("Test Scores")
	if len(before) > 0:
		testScores = after

	
	requirements_tokens = requirements.split()
	bool;flag = False
	for words in requirements_tokens:
		if words == "Personal" or words == "Statement":
				flag = True
				before,sep, after = testScores.partition("Personal Statement")
				if len(before) > 0:
					testScores = before
					testScores.strip()	
		else:
			before,sep, after = testScores.partition("Additional Requirements")
			if len(before) > 0:
				testScores = before
				testScores.strip()

	#Get Personal Statement
	if flag == True:
		personalState = program.text
		before,sep,after = 	personalState.partition("Personal Statement")
		if len(after) > 0:
			personalState = after

		before,sep, after = personalState.partition("Additional Requirements")
		if len(before) > 0:
			personalState = before
			personalState.strip()
			personalStatement = personalState

			
	#Get Additional Requirements
	additionalReq = program.text
	before,sep, after = additionalReq.partition("Additional Requirements")
	if len(after) > 0:
		additionalReq = after


	
	programRequirement = ProgramRequirements(programName, transcript, recommendation, gpa, testScores, personalStatement , additionalReq )
	if programRequirement not in graduateProgramList:
		graduateProgramList.append(programRequirement)




      
with open('Programs_Requirements_Certificate.csv', mode='w') as csv_file:
	writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	
	writer.writerow(["Program Name - Type ; Concentration", "Transcript", "Recommendation", "GPA", "Test Scores", "Personal Statement","Additional Requirements"])
	
	for study in graduateProgramList:
		writer.writerow([study.programName,study.transcript,study.recommendation, study.gpa, study.testScores, study.personalState, study.additionalReq])       



with open('All_Programs_Requirement.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	
        writer.writerow(["ProgramType", "Program Name ;  Concentration", "Transcript", "Recommendation", "GPA", "Test Scores", "Personal Statement","Additional Requirements"])
	
        for study in graduateProgramList:
	        writer.writerow(["Certificate" ,study.programName,study.transcript,study.recommendation, study.gpa, study.testScores, study.personalState, study.additionalReq])