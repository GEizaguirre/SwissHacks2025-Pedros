import requests

url = "http://127.0.0.1:5000/tables"  # Adjust if your Flask server runs elsewhere

payload = {
    "deals": ["Amount", "Phase", "Date of the funding round"],
    "companies": ["Industry", "City"]
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Response JSON:")
print(response.json())
