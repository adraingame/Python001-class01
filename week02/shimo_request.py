import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
# headers = {
# 'User-Agent' : ua.random,
# 'Referer' : 'https://shimo.im/profile'
# }

headers = {
    'User-Agent': ua.random,
    'origin': 'https://shimo.im',
    'Referer': 'https://shimo.im/login?from=home',
    'x-requested-with': 'XmlHttpRequest',
    'x-source': 'lizard-desktop'
}


s = requests.Session()

login_url = 'https://shimo.im/lizard-api/auth/password/login'
form_data = {
    'email': 'raingame@163.com',
    'mobile': '+86undefined',

}

response = s.post(login_url, data=form_data, headers=headers)

print(response)
