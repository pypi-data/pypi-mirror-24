=======
Install
=======

.. code-block:: bash

    pip install amazon_fees

=======
Example
=======

.. code-block:: python

    from python_amazon_fees.parse import AmazonFeesCalculator

    def handler(length, width, height, weight, is_media=False, is_apparel=False, is_pro=False):
      calculator = AmazonFeesCalculator(length, width, height, weight, is_media, is_apparel, is_pro)
      return calculator.fees()

    print(handler(1,1,1,1))


=======

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
  :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YYZQ6ZRZ3EW5C
