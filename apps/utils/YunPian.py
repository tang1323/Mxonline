import requests
import json
# json是我们最常用的数据常用类型


def send_single_sms(apikey, code, mobile):
    # 发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "【唐明锐】您的验证码是{}。如非本人操作，请忽略本短信".format(code)


    res = requests.post(url, data={
        "apikey": apikey,
        "mobile": mobile,
        "text": text
    })
    # json是我们最常用的数据常用类型
    re_json = json.loads(res.text)
    return re_json


if __name__ == "__main__":
    res = send_single_sms("3b4b90283fa8e7caae18876077f7b08b", "130796", "13232732408")
    import json
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    if code == 0:
        print("发送成功")
    else:
        print("发送失败：{}".format(msg))
    print(res.text)



















