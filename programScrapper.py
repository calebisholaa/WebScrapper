import os
import time


print('Loading...')
time.sleep(2)
print()
print()
print("=========================================================================")
print()
print()

time.sleep(2)
print("Scrapping for coordinators...")
print()
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

print()
print()
print("=========================================================================")
print()
print()

time.sleep(2)

print("Scrapping program requirements...")
print()

os.system("python Webscrapper-Doctoral-Requirements.py")
print("Doctoral Programs Done!")

os.system("python Webscrapper-Masters-Requirements.py")
print("Masters Programs Done!")

os.system("python Webscrapper-Certificate-Requirements.py")
print("Certificate Programs Done!")

os.system("python Webscrapper-Online-degrees-Requirements.py")

os.system("python Webscrapper-Non-Degree-Requirements.py")
print("Non degree Programs Done!")


time.sleep(2)


print()
print()
print("=========================================================================")
print()
print()

time.sleep(2)

print("Scrapping program Deadlines...")
print()


os.system("python Webscrapper-Doctoral-Deadlines.py")
print("Doctoral Programs Done!")

os.system("python Webscrapper-Masters-Deadlines.py")
print("Masters Programs Done!")

os.system("python Webscrapper-Certificate-Deadlines.py")
print("Certificate Programs Done!")

os.system("python Webscrapper-Online-degrees-Deadlines.py")

os.system("python Webscrapper-Non-Degree-Deadlines.py")
print("Non degree Programs Done!")

print()
print()
print("=========================================================================")
print()
print()


print("Scrapping complete")

