import http.client
import json
import os

api_key = os.getenv("SILICONFLOW_API_KEY")
assert api_key is not None, "SILICONFLOW_API_KEY is not set"

url = "busy-bear.siliconflow.cn"  # Note: Removed 'https://' as http.client needs the host part
endpoint = "/api/v1/playground/comprehensive/all"
headers = {"Authorization": f"Bearer {api_key}"}

siliconflow_channel_type = 45  # reference https://your-oneapi-url/api/ownedby

conn = http.client.HTTPSConnection(url)
conn.request("GET", endpoint, headers=headers)

response = conn.getresponse()
print(response.status)

body = response.read().decode("utf-8")
model_json = json.loads(body)["data"]["models"]

with open("siliconflow_models.json", "w", encoding="utf-8") as f:
    json.dump(model_json, f, ensure_ascii=False, indent=4)

siliconflow_price_json = []
for model in model_json:
    model_name = model["modelName"]
    model_price = float(model["price"])
    model_price_unit = model["priceUnit"]
    print(f"Model Name: {model_name}, Price: {model_price} {model_price_unit}")

    if model_price_unit in ["/ M Tokens", "/ M UTF-8 bytes", "/ M px / Steps"]:
        price_data = {
            "model": model_name,
            "type": "tokens",
            "channel_type": siliconflow_channel_type,
            "input": model_price / 1000 / 0.014,
            "output": model_price / 1000 / 0.014,
        }
    elif model_price_unit in ["/ Video", "/ Image", ""]:
        print(f"special price unit: {model_price_unit}")

        price_data = {
            "model": model_name,
            "type": "times",
            "channel_type": siliconflow_channel_type,
            "input": model_price,
            "output": model_price,
        }
    siliconflow_price_json.append(price_data)
    print("-" * 40)

with open("siliconflow_prices.json", "w", encoding="utf-8") as f:
    json.dump({"data": siliconflow_price_json}, f, ensure_ascii=False, indent=2)
