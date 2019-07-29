# pubsubview

redisのpubsubビューワー


## install 
```
python3 -m venv venv --prompt pubsubview
source venv/bin/activate.fish
pip install -U pip
pip install -r requirements.txt
```

## run
```
python main_server.py
```

## config

```:env.py:
# DEV
DEVFLG = True

# REDIS settings
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_CHANNEL = "channel"


# Flask settings
FLASK_PORT = 5000
```
