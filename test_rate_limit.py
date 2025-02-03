import requests

# URL of the Flask app
# url = "http://localhost:5001/"
url = "https://chowdeck.com/"

# Send multiple requests
for i in range(600000):  # Exceed the limit
    response = requests.get(url)
    response2 = requests.get(url)
    response3 = requests.get(url)
    response4 = requests.get(url)
    response5 = requests.get(url)
    response6 = requests.get(url)
    response7 = requests.get(url)
    response8 = requests.get(url)
    response9 = requests.get(url)
    response10 = requests.get(url)
    
    print(f"Request {i+1}: Status Code = {response.status_code}")
    print(f"Request {i+1}: Status Code = {response2.status_code}")
    print(f"Request {i+1}: Status Code = {response3.status_code}")
    print(f"Request {i+1}: Status Code = {response4.status_code}")
    print(f"Request {i+1}: Status Code = {response5.status_code}")
    print(f"Request {i+1}: Status Code = {response6.status_code}")
    print(f"Request {i+1}: Status Code = {response7.status_code}")
    print(f"Request {i+1}: Status Code = {response8.status_code}")
    print(f"Request {i+1}: Status Code = {response9.status_code}")
    print(f"Request {i+1}: Status Code = {response10.status_code}")
    
    if response.status_code == 429:
        print("Rate limit reached.")
        break
