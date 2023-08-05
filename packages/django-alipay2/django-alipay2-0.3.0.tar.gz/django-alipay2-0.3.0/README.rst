==============
django-alipay2
==============

提供django下alipay直接支付接口

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

4. Migrate::

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

6. Create alipay redirect::

    import uuid
    payment = AlipayPayment.objects.create(
        out_no=uuid.uuid4(),
        subject='充值',
        body='1年365元',
        amount_total=0.01,
        # reference_id='1' # 可选
    )
    return redirect('alipay_redirect', pk=payment.pk)

7. [Optional] Run sample::

    python manage.py runserver # visit http://localhost:8000/alipay (if you did step 3)

