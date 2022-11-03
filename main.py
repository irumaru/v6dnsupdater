import cloudflare
import interface
from log import logger

import time

from config import CLOUDFLARE_RECORD_ID, CLOUDFLARE_RECORD_NAME, CLOUDFLARE_ZONE_ID, INTERFACE, LOOP_INTERVAL, ONLINE_CHECK_ADDRESS

# グローバル変数
ifAddress = ''
dnsAddress = ''

def main():
    global ifAddress, dnsAddress
    logger('Main start.')

    # DNSアドレスの取得
    record = cloudflare.getCloudflareDnsRecord(CLOUDFLARE_ZONE_ID, CLOUDFLARE_RECORD_ID)
    dnsAddress = record['content']

    # ループ
    while(True):
        # Interfaceに最近設定されたアドレスを取得
        ifAddress = interface.getV6GlobalLatestAddress(INTERFACE)

        # アドレスの変更がある
        if(ifAddress != dnsAddress):
            updateAddress()
        
        # 遅延
        time.sleep(LOOP_INTERVAL)

# DNSアドレスを更新
def updateAddress():
    global ifAddress, dnsAddress

    logger("Attempt to update dns. : %s -> %s" % (dnsAddress, ifAddress))

    # オンラインになるまで繰り返し
    while(True):
        # オンラインか確認
        if(interface.checkOnline(ifAddress, ONLINE_CHECK_ADDRESS) == 0):
            # オンライン
            logger("Check online. src=%s dest=%s : Online." % (ifAddress, ONLINE_CHECK_ADDRESS))
            break
        # オフライン
        logger("Check online. : Offline.")

        # 遅延
        time.sleep(LOOP_INTERVAL)
    
    # dnsAddressの更新
    dnsAddress = ifAddress

    # DNSの更新
    cloudflare.updateCloudflareDnsRecord(CLOUDFLARE_ZONE_ID, CLOUDFLARE_RECORD_ID, "AAAA", CLOUDFLARE_RECORD_NAME, dnsAddress)
    logger("Successful DNS update.")

# mainを実行
main()