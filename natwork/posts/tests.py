from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post


class GeneralTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username='pupupu', first_name='pu', last_name='pu', password='pupupu')
        self.user_2 = User.objects.create_user(username='quququ', first_name='qu', last_name='qu', password='quququ')


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

    def test_response_404(self):
        response = self.client.get('/pashalka_marvel/')
        self.assertEqual(response.status_code, 404)

    def test_img_tag(self):
        self.client.force_login(self.user)
        with open('media/posts/social-image.jpg', 'rb') as img:
            post = self.client.post('/new/', {'text': 'text with image', 'image': img})
        response = self.client.get('')
        self.assertContains(response, 'img')
        response = self.client.get(reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertContains(response, 'img')
        response = self.client.get(reverse('posts:post_detail', kwargs={'post_id': self.user.posts.last().id}))
        self.assertContains(response, 'img')

    def test_get_not_img(self):
        self.client.force_login(self.user)
        with open('media/posts/cheats.txt') as img:
            self.client.post('/new/', {'text': 'text with image', 'image': img})
        self.assertEqual(self.user.posts.count(), 0)

    def test_cache_index_page(self):
        self.client.force_login(self.user)
        self.client.get('')
        self.client.post('/new/', {'text': 'testcache'})
        response = self.client.get('')
        self.assertContains(response, 'testcache')

    def test_auth_follow_and_unfollow(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('posts:follow', kwargs={'username': 'pupupu'}), follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('posts:unfollow', kwargs={'username': 'pupupu'}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_visible_post_for_follow_or_not(self):
        Post.objects.create(author=self.user, text='pupupu_text')
        self.client.force_login(self.user)
        self.client.get(reverse('posts:follow', kwargs={'username': 'pupupu'}), follow=True)
        response = self.client.get('/follow/')
        self.assertContains(response, 'pupupu_text')
        self.client.force_login(self.user_2)
        response = self.client.get('/follow/')
        self.assertNotContains(response, 'pupupu_text')

    def test_not_auth_add_comment(self):
        post = Post.objects.create(author=self.user, text='pupupu_text')
        response = self.client.get(reverse('posts:new_comment', kwargs={'post_id': post.id}))
        self.assertEqual(response.status_code, 302)


