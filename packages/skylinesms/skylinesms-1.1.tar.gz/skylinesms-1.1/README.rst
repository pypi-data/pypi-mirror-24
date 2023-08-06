Python module for sending sms with Skylinesms
----------------------------------------

Installation
~~~~~~~~~~~~

.. code:: bash

    pip install skylinesms

Usage example
~~~~~~~~~~~~~

.. code:: python

    import time
    from skylinesms import SkylineSms

    number = '256700123456'
    message = 'Hello from Skyline!'

    client = SkylineSms(your_api_key)

    print("Sending '%s' to %s" % (message, number))
    response = client.send_message(number, message)
    message_id = response['reference']

    response = client.check_status(message_id)
    while response['delivery'] != 'Delivered':
        print(response['status'])
        time.sleep(1)
        response = client.check_status(message_id)
    print(response['status'])

.. note::

    You will need a Skyline sms account for getting your api key and secret. Visit www.skylinesms.com to get started.

Using as command line script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    ./skylinesms.py
    usage: skylinesms.py <application key> send <number> <message> <from_number>
           skylinesms.py <application key> status <message_id>
           skylinesms.py <application key> balance