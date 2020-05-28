# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:31:50 2020

@author: ots
"""

import datetime
import time
import winsound
from twitter_scraper import get_tweets
    
def main():
    #打ち上げ時刻を設定    
    t_launch = datetime.datetime(2020, 5, 31, 4, 22, 0)
     
    t_start = datetime.datetime.now() #本番用コード
    #t_start = datetime.datetime(2020, 5, 28, 5, 40, 0) #テスト用ダミー
    
    while t_launch-datetime.datetime.now()>datetime.timedelta(minutes=10):
        td = t_launch-datetime.datetime.now()
        print("T-",td)
        time.sleep(1)

    #GO/NOGOチェック
    flg_nogo = False
    for tweet in get_tweets('SpaceflightNow', pages=2):
        if tweet['isRetweet'] == True: #リツイートは見ない
            continue
        
        if tweet['time'] < t_start: #プログラム起動時より古いツイートは見ない
            break
        
        print(tweet['text'])
        print("-----------------------------------\n")
    
        if tweet['text'].startswith('SCRUB.'):
            flg_nogo = True

    if flg_nogo == False:        
        winsound.PlaySound("alarm_clock.wav", winsound.SND_FILENAME|winsound.SND_LOOP|winsound.SND_ASYNC)
        print("打ち上げ10分前")
        print("アラームを止めるためにキー入力してください")
        input()
        winsound.PlaySound("aarm_clock.wav", winsound.SND_FILENAME|winsound.SND_PURGE)
    else:
        print("打ち上げは延期になりました")
       
#メイン関数実行
main()
