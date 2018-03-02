
from selenium import webdriver
#给出webdriver的路径
drive_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver\chromedriver.exe'
#这是为了忽略浏览器提示“正受到自动化软件的控制”
option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(executable_path=drive_path, chrome_options=option)
browser.get('http://localhost:8000')
assert 'Django' in browser.title