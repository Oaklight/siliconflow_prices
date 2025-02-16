import json

import requests
import yaml


def convert_price(price_str):
    # 初始化价格和缩放因子
    price = 0
    scale_factor = 1

    # 检查价格字符串中是否包含 "usd"
    if "usd" in price_str:
        scale_factor = 0.002
        price = float(
            price_str.replace("usd", "")
            .replace("/", "")
            .replace("M", "")
            .replace("K", "")
            .strip()
        )
        # 如果价格字符串中包含 "M"，将价格除以1000000
        if "M" in price_str:
            price = price / 1000000
        # 如果价格字符串中包含 "K"，将价格除以1000
        elif "K" in price_str:
            price = price / 1000
    # 检查价格字符串中是否包含 "rmb"
    elif "rmb" in price_str:
        scale_factor = 0.014
        price = float(
            price_str.replace("rmb", "")
            .replace("/", "")
            .replace("M", "")
            .replace("K", "")
            .strip()
        )
        # 如果价格字符串中包含 "M"，将价格除以1000000
        if "M" in price_str:
            price = price / 1000000
        # 如果价格字符串中包含 "K"，将价格除以1000
        elif "K" in price_str:
            price = price / 1000
    else:
        price = float(price_str)
    # 返回根据缩放因子调整后的价格
    return price / scale_factor


def get_channel_id_mapping():
    try:
        # 发送请求获取数据
        response = requests.get("https://oneapi.service.oaklight.cn/api/ownedby")
        response.raise_for_status()
        data = response.json()
        mapping = {}
        for key, value in data["data"].items():
            mapping[value["name"]] = int(key)
        return mapping
    except requests.RequestException as e:
        print(f"请求出错: {e}")
    except (KeyError, ValueError) as e:
        print(f"解析数据出错: {e}")
    return {}


def yaml_to_json(yaml_file_path):
    # 打开并加载YAML文件
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    # 获取渠道类型映射
    channel_id_mapping = get_channel_id_mapping()

    json_data = {"data": []}

    # 遍历YAML数据中的每个渠道
    for channel_type, models in yaml_data["models"].items():
        new_channel_type = channel_id_mapping.get(channel_type)
        if new_channel_type is None:
            print(f"未找到 {channel_type} 对应的渠道 ID，将保留原始值。")
            new_channel_type = channel_type

        # 遍历每个渠道下的模型
        for model_name, model_info in models.items():
            # 转换输入价格
            input_price = convert_price(str(model_info["input"]))
            # 转换输出价格
            output_price = convert_price(str(model_info["output"]))

            # 获取类型，如果未指定则默认为 "tokens"
            model_type = model_info.get("type", "tokens")

            model_entry = {
                "model": model_name,
                "type": model_type,
                "channel_type": new_channel_type,
                "input": input_price,
                "output": output_price,
            }
            json_data["data"].append(model_entry)

    return json_data


# 指定YAML文件的路径
yaml_file_path = "manual_prices.yaml"
# 调用函数将YAML转换为JSON
result = yaml_to_json(yaml_file_path)
# 打印转换后的JSON数据，格式化输出
print(json.dumps(result, indent=2))
