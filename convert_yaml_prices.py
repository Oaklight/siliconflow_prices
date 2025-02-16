# https://oneapi.service.oaklight.cn/api/ownedby get json dict from this url result
import json

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


def yaml_to_json(yaml_file_path):
    # 打开并加载YAML文件
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    json_data = {"data": []}

    # 遍历YAML数据中的每个模型
    for model_name, model_info in yaml_data["models"].items():
        # 转换输入价格
        input_price = convert_price(str(model_info["input"]))
        # 转换输出价格
        output_price = convert_price(str(model_info["output"]))

        model_entry = {
            "model": model_name,
            "type": model_info["type"],
            "channel_type": model_info["channel_type"],
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
