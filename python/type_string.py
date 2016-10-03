from time import sleep
import sys

s = 'Hello \n Welcome to this program'


for i in s:
    sys.stdout.write(i)
    sleep(0.05)
