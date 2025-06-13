import json

url = "https://petstore.swagger.io/v2/pet/"

headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

payload = {}

create_payload = json.dumps({
  "id": 0,
  "category": {
    "id": 5,
    "name": "Fantastik"
  },
  "name": "Dragon",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "sold"
})

update_payload = json.dumps({
  "id": 0,
  "category": {
    "id": 6,
    "name": "Nuggets"
  },
  "name": "Dino",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
})
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}