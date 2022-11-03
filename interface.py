import psutil
import socket
import ipaddress
import subprocess
import time

from log import logger

from config import ONLINE_CHECK_ADDRESS

# 例外
class getAddressError(Exception):
    pass

# アドレスリスト
address_table = {}

# 引数(interface)に設定されているIPv6グローバルアドレスリストを更新
def updateV6GlobalAddressList(interface):
    global address_table

    # IPアドレスの取得
    configs = psutil.net_if_addrs()[interface]
    
    # 初期値
    globalAddressCount = 0
    newAddressCount = 0

    # IPv6アドレスの抽出
    for config in configs:
        if(config.family == socket.AF_INET6):
            address = config.address
            # グローバルアドレスのみ
            if(ipaddress.IPv6Address(address) in ipaddress.IPv6Network('2000::/3')):
                # 新たに追加されたアドレスのみ
                if(address not in address_table):
                    address_table[address] = time.time()
                    newAddressCount += 1
                globalAddressCount += 1

    # エラー検証
    if(globalAddressCount == 0):
        logger("ERROR: No global address.")
        raise getAddressError()
    if(1 < newAddressCount):
        logger("ERROR: %d new addresses found. number of addresses must be 1." % (newAddressCount))
        raise getAddressError()

# Interfaceに一番最近設定されたグローバルアドレスを取得
def getV6GlobalLatestAddress(interface):
    global address_table

    # 設定されたアドレスを更新
    updateV6GlobalAddressList(interface)

    # 一番最近に追加されたアドレスを取得
    latest = 0
    latestAddress = ''
    for address in address_table:
        updateTime = address_table[address]
        if(updateTime > latest):
            latest = updateTime
            latestAddress = address
    
    return latestAddress

# インターネット接続を確認
# return 0で接続
def checkOnline(src, dest):
    cmd = ["ping", "-c", "1", "-W", "2", "-I", src, dest]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode
