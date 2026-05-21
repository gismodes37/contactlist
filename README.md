# Contact List - Agenda Virtual

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![django-crispy-forms](https://img.shields.io/badge/django--crispy--forms-2.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![django-imagekit](https://img.shields.io/badge/django--imagekit-4.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-9.5-3776AB?style=for-the-badge&logo=python&logoColor=white)

> **Nota:** La idea base de este proyecto no es mía. Fue tomada de un repositorio encontrado en GitHub y decidí mejorarlo con dockerización, correcciones de bugs, variables de entorno, tests y mejoras en la UI/UX.

Proyecto Django creado originalmente en el taller en Vivo "Crea una agenda virtual con Django". CRUD completo de contactos con interfaz responsiva.

## Funcionalidades

- Listar contactos con paginación, búsqueda por nombre y ordenamiento por columnas
- Ver detalle individual de cada contacto
- Crear, editar y eliminar contactos con mensajes flash de confirmación
- Subida y previsualización de avatar por contacto
- Validaciones: email único, fecha de nacimiento no futura, formato de teléfono
- Exportar contactos a CSV
- Interfaz responsiva con Bootstrap 5
- Formularios con django-crispy-forms
- Panel admin mejorado con filtros y búsqueda
- 20 tests automatizados

## Requisitos

- Python 3.11+
- Docker (opcional)

## Instalación y ejecución local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Ejecución con Docker

```bash
# Construir y levantar
docker compose up -d

# La app estará disponible en http://localhost:2051
```

Para crear un superusuario automáticamente, usa las variables de entorno en el archivo `.env` (ver `.env.example`).

## Tests

```bash
python manage.py test
```

## Formas de implementar

### Local (desarrollo)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Docker (desarrollo/QA)

```bash
cp .env.example .env
docker compose up -d
# http://localhost:2051
```

### Producción (VPS / cloud)

Opción A — Docker en servidor:

```bash
# Cambiar DJANGO_DEBUG=False en .env
# Usar proxy reverso (Nginx/Caddy) apuntando a localhost:2051
docker compose up -d --build
```

Opción B — Sin Docker:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn contactlist.wsgi:application --bind 0.0.0.0:2051 --workers 4
# Detrás de Nginx/Caddy para SSL y archivos estáticos/media
```

## Posibles mejoras

### Implementadas ✓
- [x] **Paginación preservando búsqueda** — Los enlaces de página mantienen el término `?q=`
- [x] **Avatar en lista y formulario** — Thumbnail en tabla, preview al editar
- [x] **Exportar a CSV** — Botón "Exportar" descarga todos los contactos en CSV
- [x] **Ordenar columnas** — Click en encabezados de tabla para ordenar (nombre, email, cumpleaños, fecha)
- [x] **Mensajes flash** — Feedback visual al crear, editar y eliminar contactos
- [x] **Vista de detalle** — Página individual con toda la información del contacto
- [x] **Validaciones** — Email único, fecha no futura, formato de teléfono
- [x] **Admin mejorado** — `list_display`, `search_fields`, `list_filter`, `date_hierarchy`
- [x] **20 tests automatizados** — Modelo, formularios, vistas, paginación, CSV, mensajes

### Pendientes
- [ ] **Base de datos** — Migrar de SQLite a PostgreSQL para escalar en producción
- [ ] **Autenticación** — Sistema de login/registro para que cada usuario tenga sus propios contactos
- [ ] **API REST** — Exponer endpoints con Django REST Framework para consumo desde apps móviles
- [ ] **Importar desde CSV/vCard** — Subir archivo para crear contactos en lote
- [ ] **Grupos y etiquetas** — Modelo `Category` con ManyToMany para organizar contactos
- [ ] **Búsqueda avanzada** — Filtrar por email, teléfono, rango de fechas
- [ ] **Notificaciones** — Recordatorio de cumpleaños por email
- [ ] **PWA** — Service worker para funcionar offline como app instalable
- [ ] **CI/CD** — GitHub Actions para correr tests y deploy automático
- [ ] **Traducciones** — Soporte multi-idioma con `django-modeltranslation`

![image](https://user-images.githubusercontent.com/95874195/234608808-aee37477-c7c1-4983-92fe-a9463bd4f1c6.png)

Mira la grabación del taller aquí: https://youtu.be/EQ-kqDmfUoM
