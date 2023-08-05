# django-static-md5url

This is extension for versioning static files in Django projects, if ```PRODUCTION = True```.

For example this css file:
```
<link rel="stylesheet" href="{% md5url 'base/css/styles.min.css' %}">
```
will be replace with:
```
<link rel="stylesheet" href="/static/base/css/styles.min.css?v=a6e2ba64">
```

where **a6e2ba64** is first 8 characters of md5 file sum.

# Installation

Install using pip
```
pip install django-static-md5url
```

Add ``` django_static_md5url ``` to INSTALLED_APPS.

# Configuration

Load ```{% load md5url %}``` template tag in your Django template.
