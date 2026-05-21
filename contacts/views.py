import csv
from typing import Any
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import QuerySet

from contacts.forms import ContactForm
from contacts.models import Contact


class ContactListView(generic.ListView):
    model = Contact
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        q = self.request.GET.get('q')
        sort = self.request.GET.get('sort', '-created')
        allowed_sorts = {
            'name': 'name', '-name': '-name',
            'email': 'email', '-email': '-email',
            'phone': 'phone', '-phone': '-phone',
            'created': 'created', '-created': '-created',
            'birth': 'birth', '-birth': '-birth',
        }

        if sort not in allowed_sorts:
            sort = '-created'

        qs = Contact.objects.all().order_by(sort)
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['current_sort'] = self.request.GET.get('sort', '-created')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('export') == 'csv':
            return self.export_csv()
        return super().render_to_response(context, **response_kwargs)

    def export_csv(self):
        qs = Contact.objects.all().order_by('-created')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contactos.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Email', 'Teléfono', 'Teléfono 2', 'Cumpleaños', 'Registrado'])
        for c in qs:
            writer.writerow([c.name, c.email, c.phone or '', c.phone2 or '', c.birth or '', c.created])
        return response


class ContactDetailView(generic.DetailView):
    model = Contact


class ContactCreateView(generic.CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        messages.success(self.request, 'Contacto creado exitosamente.')
        return super().form_valid(form)


class ContactUpdateView(generic.UpdateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        messages.success(self.request, 'Contacto actualizado exitosamente.')
        return super().form_valid(form)


class ContactDeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        messages.success(self.request, 'Contacto eliminado exitosamente.')
        return super().form_valid(form)
