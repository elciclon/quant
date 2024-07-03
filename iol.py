from iol_utils.iol_requests import IOLRequest

r = IOLRequest("user_data.json")

data = r.get("MIRG", "bCBA", "2022-01-01", "2022-01-31")
print(data)
