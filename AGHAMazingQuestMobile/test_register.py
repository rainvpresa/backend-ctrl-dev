import requests

# Make sure your Django server is running on localhost:8000
url = "http://127.0.0.1:8000/api/auth/registration/"

data = {
    "username": "testuser2",
    "email": "test@example.com",
    "password1": "TestPass123",
    "password2": "TestPass123"
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Will raise an error for HTTP 4xx/5xx responses
    print("Success!")
    print(response.json())
except requests.exceptions.HTTPError as errh:
    print("HTTP Error:", errh)
    print(response.text)
except requests.exceptions.ConnectionError as errc:
    print("Connection Error:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("Something went wrong:", err)
