import requests

base_url = 'http://localhost:4481'
# base_url = 'https://ci4.pesaventofilippo.com/api/v1'


print("--- LOGIN ---")
res = requests.post(f"{base_url}/login", json={
    "username": "",
    "password": ""
})
print(res.status_code, res.content)
print(res.headers)
print(res.cookies)

token = res.json()['token']

#print("--- LOGOUT ---")
#res = requests.post(f"{base_url}/logout", cookies={"token": token})
#print(res.status_code, res.json())

print("--- CORSI ---")
res = requests.get(f"{base_url}/corsi?docente=4", cookies={"token": token})
print(res.headers)
print(res.status_code, res.json())


print("--- LIBRETTO ---")
res = requests.get(f"{base_url}/libretto", cookies={"token": token})
print(res.status_code, res.json())

res = requests.post(f"{base_url}/libretto", cookies={"token": token}, json={
    "corsi": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
})
print(res.status_code, res.json())
