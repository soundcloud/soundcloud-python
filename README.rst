=================
soundcloud-python
=================

A friendly wrapper around the `Soundcloud API`_. Right now it is just a README file!

.. _Soundcloud API: http://developers.soundcloud.com/

Installation
------------

To install soundcloud-python, simply: ::

    pip install soundcloud

Or if you're not hip to the pip: ::

    easy_install soundcloud

Basic Use
---------

To use soundcloud-python, you must first create a `Client` instance, passing at a minimum the client id you obtained when you `registered your app`_: ::

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

Contributions are awesome. You are most welcome to `submit issues`_, `discuss soundcloud-python`_ or `fork the repository`_.

.. _`submit issues`: https://github.com/soundcloud/soundcloud-python/issues
.. _`discuss soundcloud-python`: https://groups.google.com/group/soundcloudapi
.. _`fork the repository`: https://github.com/soundcloud/soundcloud-python
