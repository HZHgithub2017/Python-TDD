from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Item,List
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

    #def test_home_page_only_save_items_when_necessary(self):
    #    request = HttpRequest()
    #    home_page(request)
    #    self.assertEqual(Item.objects.count(),0)

    #def test_home_page_displays_all_list_items(self):
    #    Item.objects.create(text='itemey 1')
    #    Item.objects.create(text='itemey 2')

        #        request = HttpRequest()
        #response = home_page(request)
        #f=open('recode.txt','w')
        #f.write(response.content.decode())
        #f.close()
        #self.assertIn('itemey 1', response.content.decode())
        #self.assertIn('itemey 2', response.content.decode())

class NewListTest(TestCase):
    def test_saving_a_POST_requests(self):
        self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_=List()
        list_.save()
        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_=List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1',list=other_list)
        Item.objects.create(text='other itemey 2',list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response,'other itemey 1')
        self.assertNotContains(response,'other itemey 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/%d/add_item' % (correct_list.id,),
                         data={'item_text':'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_can_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%d/add_item' % (correct_list.id,),
                                    data={'item_text':'A new item for an existing list'})
        self.assertRedirects(response,'/lists/%d/' % (correct_list.id,))