from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Item
# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>',response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
        expected_html = render_to_string('home.html',request=request)
        #f = open('recode.txt', 'w')
        #f.write(response.content.decode())
        #f.write('\n'+expected_html)
        #因为构建了跨站请求使得这里不相等，利用正则表达式去掉CSRF的内容
        import re
        pattern1_str = re.compile(r'value=(.*?)</form>',re.S)
        # result1_str = re.search(pattern1_str, response.content.decode())
        # print('csrf==',result1_str)
        response_content_decode_str_strip = re.sub(pattern1_str,"",response.content.decode())
        pattern2_str = re.compile(r'value=(.*?)</form>', re.S)
        # result2_str = re.search(pattern2_str, expected_html)
        # print('csrf==', result2_str)
        expected_html_str_strip = re.sub(pattern2_str, "", expected_html)
        self.assertEqual(response_content_decode_str_strip, expected_html_str_strip)

    def test_home_page_can_save_a_POST_requests(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')

    def test_home_page_only_save_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(),0)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)
        f=open('recode.txt','w')
        f.write(response.content.decode())
        f.close()
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')