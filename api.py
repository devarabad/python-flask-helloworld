import socket

from flask import Flask
from redis import Redis \
                  , RedisError

# Connect to Redis
redis = Redis(host                      = "redis"
              , db                      = 0
              , socket_connect_timeout  = 2
              , socket_timeout          = 2)

# Flask App
app   = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
  try:
    visits = redis.incr("visits:%s" % socket.gethostname())
  except RedisError as re:
    visits = "--"
    print(str(re))

  html  = \
    "<h3>Hello World!</h3>" \
    "<b>Hostname:</b> {hostname}<br/>" \
    "<b>Visits:</b> {visits}<br>"

  return html.format(hostname=socket.gethostname(), visits=visits)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)