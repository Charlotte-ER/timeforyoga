Use the Program
===============

The default duration is 30 minutes, and the default channel is `Yoga With Adriene`_. 
So this code will launch a randomly selected video from that channel
where the duration is no longer than 30 minutes, and no shorter than 25 minutes.

.. code-block:: bash

   python yoga.py
   
You can specify how many minutes you have available using --time or -t. For example, if
you have 10 minutes for a video, the code below will launch a `Yoga With Adriene`_ video
that is between 5 and 10 minutes in duration.

.. code-block:: bash

   python yoga.py --time 10
   python yoga.py -t 10

Alternatively, you can specify a different YouTube channel using --channel or -c.

.. code-block:: bash

   python yoga.py --channel someotherchannel
   python yoga.py -c someotherchannel

Or you can specify both:

.. code-block:: bash

   python yoga.py -t 10 -c someotherchannel

.. _Yoga With Adriene: https://www.youtube.com/@yogawithadriene

