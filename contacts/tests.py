from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from contacts.forms import ContactForm
from contacts.models import Contact


class ContactModelTest(TestCase):
    def test_create_contact(self):
        contact = Contact.objects.create(
            name='Juan Pérez',
            email='juan@example.com',
            phone='123456789',
        )
        self.assertEqual(str(contact), 'Juan Pérez')
        self.assertEqual(contact.email, 'juan@example.com')


class ContactFormTest(TestCase):
    def setUp(self):
        Contact.objects.create(name='Alice', email='alice@test.com')

    def test_email_unique_validation(self):
        form = ContactForm(data={'name': 'Bob', 'email': 'alice@test.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_future_birth_validation(self):
        future = date.today() + timedelta(days=1)
        form = ContactForm(data={
            'name': 'Bob', 'email': 'bob@test.com',
            'birth': future,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth', form.errors)

    def test_valid_birth_date(self):
        past = date.today() - timedelta(days=365 * 30)
        form = ContactForm(data={
            'name': 'Bob', 'email': 'bob@test.com',
            'birth': past,
        })
        self.assertTrue(form.is_valid())

    def test_phone_with_letters_invalid(self):
        form = ContactForm(data={
            'name': 'Bob', 'email': 'bob@test.com',
            'phone': '123-abc-456',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_phone_with_spaces_and_plus_valid(self):
        form = ContactForm(data={
            'name': 'Bob', 'email': 'bob@test.com',
            'phone': '+54 11 1234-567',
        })
        self.assertTrue(form.is_valid())


class ContactViewsTest(TestCase):
    def setUp(self):
        Contact.objects.create(name='Alice', email='alice@test.com')
        Contact.objects.create(name='Bob', email='bob@test.com')
        Contact.objects.create(name='Carlos', email='carlos@test.com')

    def test_list_view(self):
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')

    def test_list_search(self):
        response = self.client.get(reverse('contact_list'), {'q': 'Alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertNotContains(response, 'Bob')

    def test_list_search_case_insensitive(self):
        response = self.client.get(reverse('contact_list'), {'q': 'alice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')

    def test_create_view(self):
        response = self.client.get(reverse('contact_new'))
        self.assertEqual(response.status_code, 200)

    def test_create_contact_post(self):
        data = {'name': 'Daniel', 'email': 'daniel@test.com', 'phone': '999888777'}
        response = self.client.post(reverse('contact_new'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(name='Daniel').exists())

    def test_create_duplicate_email_rejected(self):
        data = {'name': 'Daniel', 'email': 'alice@test.com'}
        response = self.client.post(reverse('contact_new'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertIn('Ya existe un contacto', form.errors['email'][0])

    def test_detail_view(self):
        contact = Contact.objects.first()
        response = self.client.get(reverse('contact_detail', args=[contact.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, contact.name)

    def test_edit_view(self):
        contact = Contact.objects.first()
        response = self.client.get(reverse('contact_edit', args=[contact.pk]))
        self.assertEqual(response.status_code, 200)

    def test_edit_update(self):
        contact = Contact.objects.first()
        response = self.client.post(
            reverse('contact_edit', args=[contact.pk]),
            {'name': 'Alice Updated', 'email': 'alice@test.com'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Alice Updated')

    def test_delete_view(self):
        contact = Contact.objects.first()
        response = self.client.post(reverse('contact_delete', args=[contact.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(pk=contact.pk).exists())

    def test_pagination(self):
        for i in range(10):
            Contact.objects.create(name=f'Persona {i}', email=f'persona{i}@test.com')
        response = self.client.get(reverse('contact_list'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Persona 4')

    def test_ordering_by_name(self):
        response = self.client.get(reverse('contact_list'), {'sort': 'name'})
        self.assertEqual(response.status_code, 200)
        first_name = response.context['object_list'][0].name
        self.assertEqual(first_name, 'Alice')

    def test_export_csv(self):
        response = self.client.get(reverse('contact_list'), {'export': 'csv'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Alice', content)
        self.assertIn('Bob', content)

    def test_messages_on_create(self):
        data = {'name': 'Eva', 'email': 'eva@test.com'}
        response = self.client.post(reverse('contact_new'), data, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Contacto creado exitosamente.')
