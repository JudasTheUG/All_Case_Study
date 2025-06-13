import requests

from data import *
from verification import *



# Create Success
create_response = requests.request("POST", url, headers=headers, data=create_payload)
success_check(create_response)
json_response = create_response.json()
assert json_response.get("id") > 0

# Save pet id to use
pet_id = int(json_response.get("id"))

# Payload corruption for create_payload
payload_dict=json.loads(create_payload)
payload_dict["category"]["id"] = "pet_id"
create_payload = json.dumps(payload_dict)

# Create Fail
create_response = requests.request("POST", url, headers=headers, data=create_payload)
server_error_check(create_response)
json_response = create_response.json()
assert json_response.get("message") == "something bad happened"

# Set saved pet id for update call
payload_dict=json.loads(update_payload)
payload_dict["id"] = pet_id
update_payload = json.dumps(payload_dict)

# Update Success
update_response = requests.request("PUT", url, headers=headers, data=update_payload)
success_check(update_response)
json_response = update_response.json()
assert json_response.get("id") == pet_id

# Payload corruption for update_payload
payload_dict=json.loads(update_payload)
payload_dict["id"] = "*"
update_payload = json.dumps(payload_dict)

# Update Fail
update_response = requests.request("POST", url, headers=headers, data=update_payload)
server_error_check(update_response)
json_response = update_response.json()
assert json_response.get("message") == "something bad happened"

# Get Success
get_response = requests.request("GET", url + str(pet_id) , headers=headers, data=payload)
success_check(get_response)
json_response = get_response.json()
assert json_response.get("id") == pet_id

# DELETE Success
delete_response = requests.request("DELETE", url + str(pet_id) , headers=headers, data=payload)
success_check(delete_response)
json_response = delete_response.json()
assert json_response.get("message") == str(pet_id)

# DELETE Fail
delete_response = requests.request("DELETE", url + str(pet_id) , headers=headers, data=payload)
not_found_check(delete_response)

# Get Fail
get_response = requests.request("GET", url + str(98989865) , headers=headers, data=payload)
not_found_check(get_response)
json_response = get_response.json()
assert json_response.get("message") == "Pet not found"
