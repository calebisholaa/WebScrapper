import os
import time


print('Loading...')
time.sleep(2)
print("Scrapping for coordinators...")
os.system('python Webscrapper-Doctoral.py')
print("Doctoral Programs Done!")
os.system('python Webscrapper-Masters.py')
print("Masters Programs Done!")
os.system('python Webscrapper-Certificate.py')
print("Certificate Programs Done!")
os.system('python Webscrapper-Online-degrees.py')
print("Online degrees Programs Done!")
os.system('python Webscrapper-Non-Degree.py')
print("Non degree Programs Done!")
time.sleep(2)
print("Scrapping complete")

