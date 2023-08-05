==============
django-alipay2
==============

提供qrcode相关的filter和view，用pillow在本地生成

Quick start
-----------
1. Install::

    pip install django_alipay2


2. Add "alipay" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'alipay',
    ]

3. [Optional] Include the polls URLconf in your project urls.py like this::

    url(r'^alipay/', include('alipay.urls')),

4. Migrate

    python manage.py migrate

5. Add config 'ALIPAY' to settings.py like this::

    ALIPAY = {
        'sandbox': true,  # use sandbox client if true
        'pid': 'real alipay pid',
        'key': 'real alipay key',
        'seller': 'your_seller_email@domain.com',
        'gateway': 'https://mapi.alipay.com/gateway.do?',
        'SERVER_URL': 'http://my.server.com',  # for alipay return and notify
    }

6. [Optional] Run sample:

    use port 8000 to runserver

