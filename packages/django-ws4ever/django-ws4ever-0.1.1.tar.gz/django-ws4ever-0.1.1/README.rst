==============
django-ws4ever
==============

提供基于gevent的websocket的handler

Quick start
-----------
1. Install::

    pip install django_ws4ever


2. Add "ws4ever" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ws4ever',
    ]

3. complete your own websocket handler class::

    from ws4ever.views import BaseWebSocketApplication
    class WebSocketClientApplication(BaseWebSocketApplication):
        def __init__(self, ws):
            pass

        def handle_message(self, kind, payload=None):
            pass

4. set the websocket config path::

    #websocket path and handler class
    WEBSOCKET_PATHS = {
        "/ws": "myproject.views.WebSocketClientApplication"
    }

    # time interval to check zombile websocket connections
    CHECK_ZOMBIE_INTERVAL = 5

    # redis conf
    REDIS_HOST = ""
    REDIS_PASSWORD = ""

5. runserver
    python manage.py runserver

6. test websocket in js::

    var ws = new WebSocket("ws://localhost:8000/ws");
    ws.onopen = function()
    {
       console.log("on open");
       ws.send(JSON.stringify({kind:'kind', payload:'payload'}));
    };
    ws.onmessage = function (evt)
    {
       var received_msg = evt.data;
       console.log("receive message", received_msg);
    };
    ws.onclose = function()
    {
       console.log("Connection is closed...");
    };

7. runserver as usual::

    python manage.py runserver

8. [Optional] if you want to use wsgi to run websocket(ig.use gunicorn), config wsgi like that
  8.1 config project wsgi.py::

    #append to tail, must after  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xx.settings")
    # gunicorn 用的 websocket wsgi
    from geventwebsocket import Resource
    from ws4ever.helpers import get_websocket_sources
    ws_application = Resource(get_websocket_sources())

  8.2 run gunicorn like::

    #replace wsgi path to your own, replace your port
    `gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"   django_ws4ever.wsgi:ws_application --bind 127.0.0.1:8001`

9. [Optional/Advanced] broadcast and receive message
  9.1 can send broadcast by::

    from ws4ever.redis import redis_client, CH_WEBSOCKET_NOTIFY
    rc_main.publish(CH_WEBSOCKET_NOTIFY, json.dumps({'kind':'','payload':'', 'extra':''}))

  9.2 then can handle the messages in WebSocketClientApplication you creaed in 3. above::

    class WebSocketClientApplication(BaseWebSocketApplication):
        ...

        @classmethod
        def handle_redis_message(cls, m):
            #m == {'kind':'','payload':'','extra':''}
            #add your handle code here

