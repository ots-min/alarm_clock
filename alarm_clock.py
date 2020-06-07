# -*- coding: utf-8 -*-
"""
Created on Thu May 28 14:31:50 2020

@author: ots
"""

import datetime
import time
import configparser
import winsound
from twitter_scraper import get_tweets

def main(): 
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini",encoding="utf-8")
    
    #打ち上げ時刻を設定    
    t_launch = datetime.datetime.strptime(config_ini["LAUNCH"]["Launch_Time"],"%Y-%m-%d %H:%M:%S")
     
    t_start = datetime.datetime.now()
    while t_launch-datetime.datetime.now()>datetime.timedelta(minutes=10):
        td = t_launch-datetime.datetime.now()
        print("T-",td)
        time.sleep(1)

    #GO/NOGOチェック
    flg_nogo = False
    for tweet in get_tweets(config_ini["TWITTER"]["Target_Twitter_User"], pages=2):
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
