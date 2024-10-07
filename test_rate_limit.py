import requests

# URL of the Flask app
url = "http://localhost:5001/"

# Send multiple requests
for i in range(60):  # Exceed the limit
    response = requests.get(url)
    print(f"Request {i+1}: Status Code = {response.status_code}")
    
    if response.status_code == 429:
        print("Rate limit reached.")
        break
