# purchase-be

## Perform database migration:
```bash
python manage.py makemigrations
python manage.py migrate
```
## Run Development Server
```bash
python manage.py runserver
```

## Solving runserver widget error for python3 with Django 1.11

```bash
Just open file: venv/lib/python3.7/site-packages/django/contrib/admin/widgets.py and replace the lines

related_url += '?' + '&amp;'.join(
    '%s=%s' % (k, v) for k, v in params.items(),)
with

related_url += '?' + '&amp;'.join('%s=%s' % (k, v) for k, v in params.items())
s
```

## For setting up default 5000 data
```bash
python manage.py shell
```

```bash
from purchase.setup import *
setup_data()
```

