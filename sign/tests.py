from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address="shenzhen", start_time="2018-09-05 02:18:22")
        Guest.objects.create(id=1, event_id=1, realname="Alen", phone="1371164885", email="alen@mail.com", sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)
        self.assertEqual(result.address, "beijing")

    def test_guest_models(self):
        result = Guest.objects.get(phone="1371164885")
        self.assertEqual(result.realname, 'Alen')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    '''test index login homepage'''
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    '''test login action'''
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_admin(self):
        '''test add user'''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        '''test username and password are null'''
        test_data = {'username':'', "password":''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        '''test wrong username and password'''
        test_data = {"username": 'abc', "password": '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        '''login successfully'''
        test_data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2018-10-5 12:30:00')
        self.log_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=self.log_user)

    def test_add_event(self):
        '''test add event'''
        event = Event.objects.get(name='xiaomi5')
        self.assertEqual(event.address, 'beijing')

    def test_event_manage_success(self):
        '''test event xiaomi5'''
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'beijing', response.content)

    def test_event_manage_search_success(self):
        response = self.client.post('/search_name/', data={'name': 'xiaomi5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@mail.com', password='admin123456')
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2018-10-5 12:30:00')
        Guest.objects.create(realname='Anker', phone='6505330033', email='Anker@gmail.com', sign=0, event_id=1)
        login_user = {'username': 'admin', "password": 'admin123456'}
        self.client.post('/login_action/', data=login_user)

    def test_add_guest(self):
        guest = Guest.objects.get(realname='Anker')
        self.assertEqual(guest.phone, '6505330033')
        self.assertEqual(guest.email, 'Anker@gmail.com')
        self.assertEqual(guest.event_id, 1)
        self.assertFalse(guest.sign)

    def test_guest_manage_success(self):
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Anker', response.content)
        self.assertIn(b'6505330033', response.content)

    def test_guest_manage_search_success(self):
        response = self.client.post('/search_phone/', data={'phone': '6505330033'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Anker", response.content)
        self.assertIn(b"6505330033", response.content)
