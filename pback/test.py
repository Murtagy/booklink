import requests

localhost = 'http://127.0.0.1:8000/'
r = requests.post(localhost+'visit', json={
    'version': 1,
    'phone': '375',
    'client_id': 'cc',
    'services': []
}
)

r = requests.get(localhost+'visits')

r = requests.put(localhost+'visit/5', json={
    'version': 1,
    'phone': '375',
    'client_id': 'cc',
    'services': []
})

r = requests.get(localhost+'availability/5')