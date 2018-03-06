from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        # 给出webdriver的路径
        drive_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver\chromedriver.exe'
        # 这是为了忽略浏览器提示“正受到自动化软件的控制”
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(executable_path=drive_path, chrome_options=option)
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #应用邀请他输入一个代办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),"New to-do item did not appear in table"
        )

        self.fail('finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')