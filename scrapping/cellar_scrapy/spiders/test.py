import time
import re
import numpy as np

def caspio_scrap(appKey, cur_host="www.winedecider.com",cur_protocol="http:", cur_location='/fr/file/ficheA.php', protocol="https:", v_winloc_search="cbResetParam=1&id=1269718&winename=Chateau+Pavie+Macquin+St+Emilion+Grand+Cru+2018"):
    res_appKey = appKey.replace('/&amp;/g', "&").replace('/&lt;/g', "<").replace('/&gt;/g', ">").replace('/&quot;/g', '"').replace('/&#39;/g', "'")
    v_queryString = "AppKey=" + appKey + "&js=true" + "&pathname=" + cur_protocol + "//" + cur_host + cur_location + "&" + v_winloc_search
    v_queryString = "cbqe=" + encode(v_queryString) + "&cbEmbedTimeStamp=" + str(int(time.time()))
    v_cleanAppKey = appKey
    t = re.search('&',appKey)
    if t:
        v_cleanAppKey = appKey[0: t.span[0]]
    return "https://b1.caspio.com/dp/" + v_cleanAppKey + "?" + v_queryString

def utf8_encode(a):
    a = a.replace('/\r\n/g','\n')
    b=""
    for i in range(0,len(a)):
        c=ord(a[i])
        if c<128:
            b += chr(c)
        else:
            if c>127 and 2048 > c:
                b +=chr(c>>6|192)
            else:
                b+=chr(c>>12|224)
                b+=chr(c>>3 & 63 | 128)
            b+=chr(c & 63 |128)
    return b

def encode(a):
    keyStr= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    b=""
    h=0
    a = utf8_encode(a)
    print(a)
    while h<len(a):
        try:
            d = ord(a[h])
        except:
            d='end'
        h+=1
        try:
            c = ord(a[h])
        except:
            c='end'
        h+=1
        try:
            e = ord(a[h])
        except:
            e='end'
        h+=1
        f = d>>2
        if c!='end':
            d = (d&3)<<4|c>>4
        else:
            d=0
            g=n=64
        if e!='end':
            g = (c&15)<<2|e>>6
            n=e&63
        else:
            n=64
        print(h,f, d,g, n)        
        b=b+keyStr[f]+keyStr[d]+keyStr[g]+keyStr[n]
    return b

print(caspio_scrap('04d70000853358c5e45846f2be25', v_winloc_search='cbResetParam=1&id=13102299&winename=Lancelot+Pienne+Champagne+Brut+Blanc+de+Blancs++cuvee+de+la+Table+Ronde+NV+9999'))
#print(encode("AppKey=04d70000853358c5e45846f2be25&js=true&pathname=http://www.winedecider.com/fr/file/ficheA.php&cbResetParam=1&id=1269718&winename=Chateau+Pavie+Macquin+St+Emilion+Grand+Cru+2018"))
