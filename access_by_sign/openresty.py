#coding=utf-8
import time
import requests

# 生成签名的字符串
def getSignature(params, secret):

    # basestring=a=1&b=hello&c=world&key=1&time=1566877802288
    ivlist = []
    # 拼凑字符串
    for i,v in params.items():
        tmpstr=str(i)+"="+str(v)
        ivlist.append(tmpstr)
    ivlist.append(secret)
    basestr = "&".join(sorted(ivlist))
    print("basestr = %s" % basestr)

    # 由于MD5模块在python3中被移除
    # 在python3中使用hashlib模块进行md5操作
    import hashlib
    # 创建md5对象
    m = hashlib.md5()

    # 此处必须encode，若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
    # 因为python3里默认的str是unicode
    # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
    b = basestr.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()

    return str_md5


if __name__ == "__main__":
    # 拼凑访问url
    params = {"a":22,"b":"hello","c":"wrold","key":1}
    time = int(round(time.time() * 1000))
    params["time"] = time

    sinstr = getSignature(params, "zzz")
    print(sinstr)

    params["sign"] = sinstr
    url = "http://stg.paat.com/sign?a=22&b=hello&c=world&key=1&time={time}&sign={sign}".format(time = time, sign = sinstr)
    print("url = %s" % url)
    print('=====================================')
    # 模拟正确的请求
    res = requests.get("http://stg.paat.com/fd98e31b3feafd554feed75131888ee5.pdf", params = params, timeout=10)
    res.encoding="utf-8"
    print(res.content)
