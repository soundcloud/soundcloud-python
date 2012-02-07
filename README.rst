=================
soundcloud-python
=================

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

    tracks = client.get('/tracks', order='hotness', limit=10)
    for track in tracks:
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

    client = soundcloud.client(client_id=YOUR_CLIENT_ID)
    track = client.get('/tracks/30709985')
    print track.title

If however, you need to access private resources or modify a resource,
you will need to have a user delegate access to your application. To do
this, you can use one of the following OAuth2 authorization flows.

**User Agent Flow**

The `User Agent Flow`_ involves redirecting the user to soundcloud.com 
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
.. _`User Agent Flow`: http://developers.soundcloud.com/docs/api/authentication#user-agent-flow
.. _`User Credentials Flow`: http://developers.soundcloud.com/docs/api/authentication#user-credentials-flow

Examples
--------

Adding a track to a playlist: ::

    import soundcloud

    client = soundcloud.Client(access_token="a valid access token")

    # get my last playlist
    playlist = client.get('/me/playlists')[0]

    # get ids of contained tracks
    track_ids = [t.id for t in playlist.tracks]
    
    # adding a new track 21778201
    track_ids.append(21778201)

    # map array of ids to array of track objects:
    tracks = map(lambda track_id: dict(track_id=track_id), track_ids)

    # send update/put request to playlist
    playlist = client.put(playlist.uri, playlist={
        'tracks': tracks
    })

    # print the list of track ids of the updated playlist:
    print [t.id for t in playlist.tracks]


Contributing
------------

Contributions are awesome. You are most welcome to `submit issues`_,
`discuss soundcloud-python`_ or `fork the repository`_.

.. _`submit issues`: https://github.com/soundcloud/soundcloud-python/issues
.. _`discuss soundcloud-python`: https://groups.google.com/group/soundcloudapi
.. _`fork the repository`: https://github.com/soundcloud/soundcloud-python
