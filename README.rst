=============
Time for Yoga
=============

Play me a yoga video based on how much time I have available.

The default YouTube channel is `Yoga With Adriene`_, however users 
can specify alterative channel name at command line.

.. _Yoga With Adriene: https://www.youtube.com/@yogawithadriene

============
Installation
============

To use timeforyoga, first install it using pip:

.. code-block:: console

   (.venv) $ pip install timeforyoga

===============
Use the Program
===============

The default duration is 30 minutes, and the default channel is `Yoga With Adriene`_. 
So this code will launch a randomly selected video from that channel
where the duration is no longer than 30 minutes, and no shorter than 25 minutes.

.. code-block:: bash

   timeforyoga
   
You can specify how many minutes you have available using --time or -t. For example, if
you have 10 minutes for a video, the code below will launch a `Yoga With Adriene`_ video
that is between 5 and 10 minutes in duration.

.. code-block:: bash

   timeforyoga --time 10
   timeforyoga -t 10

Alternatively, you can specify a different YouTube channel using --channel or -c:

.. code-block:: bash

   timeforyoga --channel someotherchannel
   timeforyoga -c someotherchannel

Or you can specify both:

.. code-block:: bash

   timeforyoga --time 10 --channel someotherchannel
   timeforyoga -t 10 -c someotherchannel

===============
Use the Package
===============

.. autofunction:: get_uploads_playlist_from_channel_name
   :module: timeforyoga

.. autofunction:: timeforyoga.get_videos_in_playlist
   :module: timeforyoga.timeforyoga

.. autofunction:: get_videos_within_5_mins_of_max_duration
   :module: timeforyoga.timeforyoga

.. autofunction:: reformat_playtime_to_minutes

============
Contributing
============
Pull requests are welcome. Please open an issue first to 
discuss the proposed change. Please update tests as appropriate.

To install with tools to develop and run tests, please run 
the following in your virtual env:

.. code-block:: bash

   pip install -e .[dev]

=======
License
=======
`MIT`_

.. _MIT: https://choosealicense.com/licenses/mit/
