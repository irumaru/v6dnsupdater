import datetime

from config import LOG_PATH

def logger(message):
    # 時刻の追加
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    message = "[%s]: %s" % (now, message)

    # ファイルに出力
    with open(LOG_PATH, 'a') as p:
        print(message, file=p)