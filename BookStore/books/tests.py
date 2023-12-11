from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Book

class BookTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='adesh',
            email='adeshwadghule@gmail.com',
            password='Adesh@123',
        )

        self.book = Book.objects.create(
            title='django for beginners',
            author='WS Vincent',
            description='anything',
            price='30',
            image_url='https://forexample.jpg',
            follow_author='https://twitter.com/wsv3000?lang=en',
            book_available='True',
        )

    def test_string_representation(self):
        book = Book(title='new book')
        self.assertEqual(str(book), book.title)

    def test_book_model_fields_content(self):
        self.assertEqual(f'{self.book.title}', 'django for beginners')
        self.assertEqual(f'{self.book.author}', 'WS Vincent')
        self.assertEqual(f'{self.book.description}', 'anything')
        self.assertEqual(f'{self.book.price}', '30')
        self.assertEqual(f'{self.book.image_url}', 'https://forexample.jpg')
        self.assertEqual(f'{self.book.follow_author}', 'https://twitter.com/wsv3000?lang=en')
        self.assertEqual(f'{self.book.book_available}', 'True')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(username='adesh', email='adeshwadghule@gmail.com', password='Adesh@123')
        request = self.client.get(reverse('list'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_book_list_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('list'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_book_detail_view_for_logged_in_user(self):
        self.client.login(username='adesh', email='adeshwadghule@gmail.com', password='Adesh@123')
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, 'WS Vincent')
        self.assertContains(request, '30')

    def test_book_detail_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, 'WS Vincent')
        self.assertContains(request, '30')

    def test_checkout_view_for_logged_in_user(self):
        self.client.login(username='adesh', email='adeshwadghule@gmail.com', password='Adesh@123')
        request = self.client.get(reverse('checkout', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_checkout_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('checkout', args='1'))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, '/accounts/login/?next=/1/checkout/')

    def test_book_when_available(self):
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Buy Now')
        self.assertNotContains(request, 'Out of Stock !')

    def test_book_when_out_of_stock(self):
        book = Book.objects.create(
            title='new book',
            author='adesh',
            description='anything',
            price='30',
            image_url='https://forexample.jpg',
            follow_author='https://twitter.com/wsv3000?lang=en',
            book_available='False',
        )
        request = self.client.get(reverse('detail', args='2'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Out of Stock !')
        self.assertNotContains(request, 'Buy Now')
