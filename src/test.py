import re

string = 'alice paiva silva cPf61140145371'
if re.search(r'(?i)cpf', string):
     print(re.split(r'(?i)cpf', string,2))
else:
     print('dont match')