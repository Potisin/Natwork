from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.test import TestCase, Client
from django.urls import reverse


class GeneralTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username='pupupu', first_name='pu', last_name='pu', password='pupupu')

    def test_create_profile(self):
        response = self.client.get('/profile/pupupu/')
        self.assertEqual(response.status_code, 200)

    def test_auth_create_post(self):
        self.client.force_login(self.user)
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_after_create_post(self):
        response = self.client.get('/new/', follow=True)
        self.assertEqual(response.resolver_match.func.__name__, LoginView.as_view().__name__)
        self.assertTemplateUsed(response, template_name='users/login.html')

    def test_check_new_post(self):
        self.client.force_login(self.user)
        response = self.client.post('/new/', {'text': 'testtest'}, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('')
        self.assertEqual((response.context['page_obj'])[-1].text, 'testtest')
        response = self.client.get(reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual((response.context['page_obj'])[-1].text, 'testtest')
        response = self.client.get(reverse('posts:post_detail', kwargs={'post_id': self.user.posts.last().id}))
        self.assertEqual(response.context['post'].text, 'testtest')

    def test_edit_post_and_check(self):
        self.client.force_login(self.user)
        self.client.post('/new/', {'text': 'testtest'}, follow=True)
        update_url = reverse('posts:edit_post', kwargs={'post_id': self.user.posts.last().id})
        self.client.post(update_url, {'text': 'updated'}, follow=True)
        response = self.client.get('')
        self.assertEqual((response.context['page_obj'])[-1].text, 'updated')
        response = self.client.get(reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual((response.context['page_obj'])[-1].text, 'updated')
        response = self.client.get(reverse('posts:post_detail', kwargs={'post_id': self.user.posts.last().id}))
        self.assertEqual(response.context['post'].text, 'updated')
