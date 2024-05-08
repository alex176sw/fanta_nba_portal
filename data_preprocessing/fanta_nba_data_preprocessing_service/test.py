import requests

# Define the URL of your Flask app
url = 'http://localhost:5000/get_ml_data/inference'  # Replace with your actual URL

# Sample JSON data to send in the POST request
json_data = {
    'key1': 'value1',
    'key2': 'value2'
}

# Send a POST request to the Flask app
response = requests.post(url, json=json_data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response from the Flask app
    print(response.json())
else:
    # Print an error message if the request was not successful
    print('Error:', response.status_code)
