#dictionary having name and age
age = {
    'Kelly': 18, 
    'Sara' : 20,
 'Mirrah' : 25
 }

x = age.values()
z = age.get('Kelly')
print(x)
y = age.values()
print(y)
#how to tukar value age:
age['Sara'] = 30
print(z)
del age['Mirrah']
print(age)

#if u try to change a key yg nonexistent, python will add it instead label as error
age ['aliyazaf'] = 18
print(age)