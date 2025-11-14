## Architecture Overview
### Project Structure
```text
filemac_web/
├── filemac_web/          # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── filemac_app/          # Main application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── utils.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── converters/
│   └── results/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── media/               # Uploaded files
```
