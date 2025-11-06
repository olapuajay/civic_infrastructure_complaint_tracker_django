# Civic Infrastructure Complaint and Status Tracker

This Django project allows citizens to file civic complaints (potholes, broken streetlights, water leaks, waste) and track their resolution status. Admins can manage complaints via Django admin.

Quick start (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install requirements

```powershell
pip install -r requirements.txt
```

3. Apply migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (the project expects username `admin`, password `admin` — create with manage.py shell if you want non-interactive):

Interactive (recommended):

```powershell
python manage.py createsuperuser
```

Or create the admin user programmatically (unsafe for production):

```powershell
python - <<'PY'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin','admin@example.com','admin')
print('done')
PY
```

5. Run the development server

```powershell
python manage.py runserver
```

6. Visit http://127.0.0.1:8000/

Notes:

- Uploaded images are stored in `media/complaints/`.
- Admin panel: http://127.0.0.1:8000/admin/

Next steps:

- Add tests and more validation
- Add pagination for list views
- Add email notifications on status updates
