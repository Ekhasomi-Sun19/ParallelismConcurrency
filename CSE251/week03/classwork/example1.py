import requests

response = requests.get('http://localhost:8790/')
data = response.json()
#print(f'{data=}')
films = data['films']
print(f'{films=}')
film6 = f'{films}6'
print(f'{film6=}')