Lighthouse API client
=====================

This project provides a ready to go implementation of the `Lighthouse
API Client <https://github.com/thiagolcmelo/oglhclient>`_ as a Slack
Bot.

It has also a `Docker
image <https://hub.docker.com/r/thiagolcmelo/oglhslack/>`_ for
launching the slack bot in minutes.

Please refer to `<https://github.com/thiagolcmelo/oglhslack>`_ for a full
documentation.

Authentication
--------------

The **Lighthouse API Client** expects to find the following environment
variables:

-  **(required)** ``OGLH_API_USER`` a valid Lighthouse user
-  **(required)** ``OGLH_API_PASS`` a valid Lighthouse user's password
-  **(required)** ``OGLH_API_URL`` the Lighthouse API url without
   ``/api/v1``

Lighthouse Slack Bot
--------------------

It expects to find the following environment variables:

-  **(required)** ``SLACK_BOT_TOKEN`` which is provided by Slack at the
   moment of `creating a bot <https://api.slack.com/bot-users>`_.
-  **(required)** ``SLACK_BOT_NAME`` is the name given to the Slack bot.
-  **(required)** ``SLACK_BOT_DEFAULT_CHANNEL`` a default Slack channel
   name used for warnings.
-  **(optional)** ``SLACK_BOT_DEFAULT_LOG_CHANNEL`` a Slack channel name
   for logs, if it is not provided, logs will be printed to a file only,
   but logs classified as high priority like warnings and errors will be
   printed to the ``SLACK_BOT_DEFAULT_CHANNEL`` when
   ``SLACK_BOT_DEFAULT_LOG_CHANNEL`` is not set.
-  **(optional)** ``SLACK_BOT_ADMIN_CHANNEL`` is the name for the
   administrator channel, if no name is informed, it is assumed to be
   **oglhadmin**.

The **Lighhouse** Slack bot can be triggered as simple as:

.. code:: python

    from oglhslack import OgLhSlackBot
    slack_bot = OgLhSlackBot()
    slack_bot.listen()

Or, straight from the terminal:

.. code:: bash

    $ python oglhslack.py


Docker image
------------

The Opengear Lighthouse docker image is available at
https://hub.docker.com/r/thiagolcmelo/oglhslack/.

It requires a file containing the environment variables as specified
`here <https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e-env-env-file>`_.

It is supposed to be like:

::

    SLACK_BOT_TOKEN=xoxb-************-************************
    SLACK_BOT_NAME=mybotname
    SLACK_BOT_DEFAULT_CHANNEL=my-default-channel
    SLACK_BOT_DEFAULT_LOG_CHANNEL=my-default-log-channel
    SLACK_BOT_ADMIN_CHANNEL=oglhadmin
    OGLH_API_USER=myOgLhUser
    OGLH_API_PASS=myOgLhPassword
    OGLH_API_URL=https://oglh-octo.opengear.com

For launching the Slack bot just run:

.. code:: bash

    $ sudo docker run --env-file /path/to/my/env.list thiagolcmelo/oglhslack
