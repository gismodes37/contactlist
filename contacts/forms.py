from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'phone2', 'birth', 'avatar')
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'avatar': forms.FileInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = Contact.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un contacto con este correo electrónico.')
        return email

    def clean_birth(self):
        birth = self.cleaned_data.get('birth')
        if birth and birth > timezone.now().date():
            raise ValidationError('La fecha de nacimiento no puede ser futura.')
        return birth

    def _clean_phone(self, value):
        if not value:
            return value
        cleaned = value.replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', '')
        if not cleaned.isdigit():
            raise ValidationError('El teléfono solo puede contener números, espacios, guiones, paréntesis y +.')
        return value

    def clean_phone(self):
        return self._clean_phone(self.cleaned_data.get('phone'))

    def clean_phone2(self):
        return self._clean_phone(self.cleaned_data.get('phone2'))
