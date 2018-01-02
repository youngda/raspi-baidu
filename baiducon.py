# -*- coding: utf-8 -*-
#auth:youngda
from pyaudio import PyAudio, paInt16
import importlib
import numpy as np
from datetime import datetime
import wave
import time
import urllib,requests, pycurl
import base64
import json
import os
import sys
import RPi.GPIO as GPIO
#importlib.reload(sys) 
save_count = 0
save_buffer = []
t = 0
sum = 0
time_flag = 0
flag_num = 0
filename = '2.wav'
duihua = '1'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT,initial=GPIO.HIGH)
def getHtml(url):
    page = requests.get(url)
    html = page.text
    return html
 
def get_token():
    apiKey = "0ahKpEulEBHlshgWh5nUQKXr"
    secretKey = "228bfd2899906ccf673da75cd94c3f2e"
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+apiKey+"&client_secret="+secretKey
    res = requests.get(auth_url)
    json_data = res.text
    return json.loads(json_data)['access_token']
 
def dump_res(buf):
    global duihua
    a = eval(buf)
    if a['err_msg']=='success.':
        duihua = a['result'][0]
 
def use_cloud(token):
    fp = wave.open(filename, 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    cuid = "10026562" #产品id
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=8000',
        'Content-Length: %d' % f_len
    ]
 
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val
 
# 将data中的数据保存到名为filename的WAV文件中
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes("".join(data))
    wf.close()
 
token = get_token()
try:
    GPIO.output(40, GPIO.HIGH)
    while (True):
        os.system('arecord --format=S16_LE --duration=4 --rate=8k /home/pi/baidu/2.wav')
        use_cloud(token)
        info = duihua
        print info
        while (info == '1' or info == '' or info == '，' or info[1] == '，'):
            os.system('arecord --format=S16_LE --duration=4 --rate=8k /home/pi/baidu/2.wav')
            use_cloud(token)
            info = duihua
            duihua = ""
        if (info.find("前进") >= 0 or info.find("前") >= 0):
            GPIO.output(40, GPIO.LOW)
            duihua = ""
        elif (info.find("后退") >= 0 or info.find("后") >= 0):
            GPIO.output(40, GPIO.HIGH)
            duihua = ""
except:
    print 'Cleaning up'
    GPIO.cleanup()