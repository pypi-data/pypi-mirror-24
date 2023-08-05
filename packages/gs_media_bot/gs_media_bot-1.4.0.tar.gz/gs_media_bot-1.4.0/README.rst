gs_media_bot
==============
Bot for posting media to GNU Social.

Installation
------------

``pip install gs_media_bot``

or

``python3 setup.py install``

You can also install ``gs-media-bot`` package from AUR.

Basic usage
-----------

Set the configuration parameters in the default location (``$XDG_CONFIG_HOME/gs_media_bot/config.json``) or supply it to the script with ``-c``.

Configuration example:

::

    {
        "credentials": {
            "server_url": "https://gnusocial.server",
            "username": "username",
            "password": "password",
        },
        "patterns": {
            "~/My_Cool_Photos/my_photo.jpg": "Yet another photo!",
            "~/Directory/With/subdirs/**": "random pic"
        }
    }
