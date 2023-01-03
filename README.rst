"""""""""""""""""
Time for Yoga
"""""""""""""""""
...........
Play me a yoga video based on how much time I have available.

The default YouTube channel is `Yoga With Adriene`_, however users 
can specify alterative channel name at command line.

.. _Yoga With Adriene: https://www.youtube.com/@yogawithadriene
...........

.. contents:: Overview
   :depth: 3

===================
Installation
===================
TODO - Use pip to install.

.. code:: bash
   pip install yoga
===================
Usage
===================
----------------------
Run the program
----------------------
The default duration is 30 minutes, and the default channel is `Yoga With Adriene`_. 
So this code will launch a randomly selected video from that channel
where the duration is no longer than 30 minutes, and no shorter than 25 minutes.
.. code:: bash
   python yoga.py
   
You can specify how many minutes you have available using --time or -t. For example, if
you have 10 minutes for a video, the code below will launch a `Yoga With Adriene`_ video
that is between 5 and 10 minutes in duration.
.. code:: bash
    python yoga.py --time 10
    python yoga.py -t 10

Alternatively, you can specify a different YouTube channel using --channel or -c.
.. code:: bash
    python yoga.py --channel 
    python yoga.py -c someotherchannel

Or you can specify both:
.. code:: bash
   python yoga.py -t 10 -c someotherchannel


----------------------
Reuse the functions
----------------------
Each channel on YouTube has a default playlist called 'Uploads', which contains all
all videos uploaded to that channel. If you have the channel name, then you can get the
playlist id of that channel's Uploads playlist, by using the ``get_uploads_playlist_from_channel_name()`` 
function as follows:

.. autofunction:: get_uploads_playlist_from_channel_name()

===================
Contributing
===================
Pull requests are welcome. Please open an issue first to 
discuss the proposed change. Please update tests as appropriate.

TODO - To install with tools to develop and run tests, please run 
the following in your virtual env:
.. code:: bash
   pip install -e [dev]
===================
License
===================
`MIT`_

.. _MIT: https://choosealicense.com/licenses/mit/
