from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        # 给出webdriver的路径
        drive_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver\chromedriver.exe'
        # 这是为了忽略浏览器提示“正受到自动化软件的控制”
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(executable_path=drive_path, chrome_options=option)
        self.browser.implicitly_wait(30)
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('finish the test!')
if __name__ == '__main__':
    unittest.main(warnings='ignore')