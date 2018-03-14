from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
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

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #应用邀请他输入一个代办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        #她按了回车键之后页面更新了
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        ##她开始第二个事项的输入
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        # 她按了回车键之后页面更新了
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')


        self.fail('finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')