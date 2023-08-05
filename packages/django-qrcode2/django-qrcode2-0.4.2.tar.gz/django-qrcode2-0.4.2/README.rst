==============
django-qrcode2
==============

提供qrcode相关的filter和view，用pillow在本地生成

Quick start
===========

- Install

::

    pip install django_qrcode2


- Add "qrcode2" to your INSTALLED_APPS setting:

::

    INSTALLED_APPS = [
        ...
        'qrcode2',
    ]

- [Optional] Include the polls URLconf in your project urls.py

::

    url(r'^qrcode/', include('qrcode2.urls')),

- No migration needed

- Add filter to template

::

    {% load qrcode2 %}

    <!-- if an view with name 'qrcode' is provided, 'src' will be an url, otherwise it's an base64 data blob -->
    <img src="{{ 'some text' | qrcode_src }}">

    <!-- insert an <img> with template inclusion -->
    {% include 'qrcode2/img.html' with text='hello' %}

