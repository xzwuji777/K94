#dictionary has name and age
age = {
    'Kelly': 18, 
    'Sara' : 20,
 'Mirrah' : 25
 }

x = age.values()
x = age.get('Kelly')
print(x)
y = age.values()
print(y)
age['Sara'] = 30
print(y)
del age['Mirrah']
print(age)


