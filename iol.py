from iol_utils.iol_requests import IOLRequest

r = IOLRequest("user_data.json")

data = r.get("MIRG", "bCBA", "2024-07-01", "2024-07-03", True)
print(data)
