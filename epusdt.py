import hashlib
import json

import requests

from config import EPUSDT_API_URL, EPUSDT_API_KEY


def epusdt_submit(order_data):
    print("order_data", json.dumps(order_data))
    print("当前选择USDT支付页")
    create_data = {
        "order_id": order_data['out_trade_no'],
        "amount": order_data['money'],
        "notify_url": order_data['notify_url'],
        "redirect_url": order_data['return_url'],
    }
    items = create_data.items()
    items = sorted(items)
    wait_sign_str = ''
    for i in items:
        wait_sign_str += str(i[0]) + '=' + str(i[1]) + '&'
    wait_for_sign_str = wait_sign_str[:-1] + EPUSDT_API_KEY
    sign = hashlib.md5(wait_for_sign_str.encode('utf-8')).hexdigest()
    create_data.update(signature=sign)
    try:
        request_api_url = EPUSDT_API_URL + '/api/v1/order/create-transaction'
        print(request_api_url)
        print(json.dumps(create_data))
        req = requests.post(request_api_url, json=create_data, headers={'User-Agent': "vgrpc/python"})
        print("req.text", req.text)
        resp = req.json()
        return resp
    except Exception as e:
        print('submit | API请求失败')
        print(e)
        return 'API请求失败'


def check_status(out_trade_no):
    print("开始查询EPUSDT订单号支付情况:{}".format(out_trade_no))
    try:
        req = requests.get(EPUSDT_API_URL + '/pay/check-status/{}'.format(out_trade_no),
                           timeout=5)
        resp = req.json()
        print(resp)
        if resp['status_code'] == 200:
            # trade_no = str(rst_dict['trade_no'])
            # msg = str(rst_dict['msg'])
            pay_status = resp['data']['status']
            if pay_status == 2:
                print('支付成功')
                return '支付成功'
            else:
                print('支付失败')
                return '支付失败'
        else:
            print('查询失败，订单号不存在')
            return '查询失败，订单号不存在'
    except Exception as e:
        print('check_status | 请求失败')
        print(e)
        return 'API请求失败'
