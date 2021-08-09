=====================================
⚠️⚠️DEPRECATED - NO LONGER MAINTAINED⚠️⚠️
=====================================
This repository is no longer maintained by the SoundCloud team due to capacity constraints. We're instead focusing our efforts on improving the API & the developer platform. Please note, at the time of updating this, the repo is already not in sync with the latest API changes. 

We recommend the community to fork this repo in order to maintain the SDK. We'd be more than happy to make a reference on our developer that the developers can use different SDKs build by the community. In case you need to reach out to us, please head over to https://github.com/soundcloud/api/issues  

=================
soundcloud-python
=================

.. image:: https://travis-ci.org/soundcloud/soundcloud-python.svg
    :target: https://travis-ci.org/soundcloud/soundcloud-python

A friendly wrapper around the `Soundcloud API`_.

.. _Soundcloud API: http://developers.soundcloud.com/

Installation
------------

To install soundcloud-python, simply: ::

    pip install soundcloud

Or if you're not hip to the pip: ::

    easy_install soundcloud

Basic Use
---------

To use soundcloud-python, you must first create a `Client` instance,
passing at a minimum the client id you obtained when you `registered
your app`_: ::

    import soundcloud

    client = soundcloud.Client(client_id=YOUR_CLIENT_ID)

The client instance can then be used to fetch or modify resources: ::

    tracks = client.get('/tracks', limit=10)
    for track in tracks.collection:
        print track.title
    app = client.get('/apps/124')
    print app.permalink_url

.. _registered your app: http://soundcloud.com/you/apps/

Authentication
--------------

All `OAuth2 authorization flows`_ supported by the Soundcloud API are
available in soundcloud-python. If you only need read-only access to
public resources, simply provide a client id when creating a `Client`
instance: ::

    import soundcloud

    client = soundcloud.Client(client_id=YOUR_CLIENT_ID)
    track = client.get('/tracks/30709985')
    print track.title

If however, you need to access private resources or modify a resource,
you will need to have a user delegate access to your application. To do
this, you can use one of the following OAuth2 authorization flows.

**Authorization Code Flow**

The `Authorization Code Flow`_ involves redirecting the user to soundcloud.com
where they will log in and grant access to your application: ::

    import soundcloud

    client = soundcloud.Client(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        redirect_uri='http://yourapp.com/callback'
    )
    redirect(client.authorize_url())

Note that `redirect_uri` must match the value you provided when you
registered your application. After granting access, the user will be
redirected to this uri, at which point your application can exchange
the returned code for an access token: ::

    access_token, expires, scope, refresh_token = client.exchange_token(
        code=request.args.get('code'))
    render_text("Hi There, %s" % client.get('/me').username)


**User Credentials Flow**

The `User Credentials Flow`_ allows you to exchange a username and
password for an access token. Be cautious about using this flow, it's
not very kind to ask your users for their password, but may be
necessary in some use cases: ::

    import soundcloud

    client = soundcloud.Client(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        username='jane@example.com',
        password='janespassword'
    )
    print client.get('/me').username

.. _`OAuth2 authorization flows`: http://developers.soundcloud.com/docs/api/authentication
.. _`Authorization Code Flow`: http://developers.soundcloud.com/docs/api/authentication#user-agent-flow
.. _`User Credentials Flow`: http://developers.soundcloud.com/docs/api/authentication#user-credentials-flow

Examples
--------

Resolve a track and print its id: ::

    import soundcloud

    client = soundcloud.Client(client_id=YOUR_CLIENT_ID)

    track = client.get('/resolve', url='http://soundcloud.com/forss/flickermood')

    print track.id

Upload a track: ::

    import soundcloud

    client = soundcloud.Client(access_token="a valid access token")

    track = client.post('/tracks', track={
        'title': 'This is a sample track',
        'sharing': 'private',
        'asset_data': open('mytrack.mp4', 'rb')
    })

    print track.title

Start following a user: ::

    import soundcloud

    client = soundcloud.Client(access_token="a valid access token")
    user_id_to_follow = 123
    client.put('/me/followings/%d' % user_id_to_follow)

Update your profile description: ::

    import soundcloud

    client = soundcloud.Client(access_token="a valid access token")
    client.put('/me', user={
        'description': "a new description"
    })

Proxy Support
-------------

If you're behind a proxy, you can specify it when creating a client: ::

    import soundcloud

    proxies = {
        'http': 'example.com:8000'
    }
    client = soundcloud.Client(access_token="a valid access token",
                               proxies=proxies)

The proxies kwarg is a dictionary with protocols as keys and host:port as values.

Redirects
---------

By default, 301 or 302 redirects will be followed for idempotent methods. There are certain cases where you may want to disable this, for example: ::

    import soundcloud

    client = soundcloud.Client(access_token="a valid access token")
    track = client.get('/tracks/293/stream', allow_redirects=False)
    print track.location

Will print a tracks streaming URL. If ``allow_redirects`` was omitted, a binary stream would be returned instead.

Running Tests
-------------

To run the tests, run: ::

    $ pip install -r requirements.txt
    $ nosetests --with-doctest
    ..................

Success!

Contributing
------------

Contributions are awesome. You are most welcome to `submit issues`_,
or `fork the repository`_.

soundcloud-python is published under a `BSD License`_.

.. _`submit issues`: https://github.com/soundcloud/soundcloud-python/issues
.. _`fork the repository`: https://github.com/soundcloud/soundcloud-python
.. _`BSD License`: https://github.com/soundcloud/soundcloud-python/blob/master/README
