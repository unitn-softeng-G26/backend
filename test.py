import requests

base_url = 'https://ci4.pesaventofilippo.com/api/v1'


print("--- LOGIN ---")
res = requests.post(f"{base_url}/login", json={
    "username": "filippo.pesavento@studenti.unitn.it",
    "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
})
print(res.status_code, res.json())

token = res.json()['token']

#print("--- LOGOUT ---")
#res = requests.post(f"{base_url}/logout", cookies={"token": token})
#print(res.status_code, res.json())

print("--- CORSI ---")
res = requests.get(f"{base_url}/corsi?docente=4", cookies={"token": token})
print(res.status_code, res.json())


print("--- LIBRETTO ---")
res = requests.get(f"{base_url}/libretto", cookies={"token": token})
print(res.status_code, res.json())

res = requests.post(f"{base_url}/libretto", cookies={"token": token}, json={
    "corsi": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
})
print(res.status_code, res.json())
