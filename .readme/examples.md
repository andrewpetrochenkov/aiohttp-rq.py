```bash
$ export AIOHTTP_RQ_REQUEST_QUEUE="aiohttp-rq-request"
$ export AIOHTTP_RQ_RESPONSE_QUEUE="aiohttp-rq-response"
$ export AIOHTTP_RQ_EXCEPTION_QUEUE="aiohttp-rq-exception"
$ export AIOHTTP_RQ_TTL_DNS_CACHE=3600 # optional
$ python3 -m aiohttp_rq 50 # 50 workers

```

redis client
```python
import redis

REDIS = redis.Redis(host='localhost', port=6379, db=0)
```

#### Redis push

```python
value=json.dumps(dict(
    url='https://domain.com',
    method="GET",
    headers=None,
    data=None,
    allow_redirects=True
))
REDIS.rpush('aiohttp-rq-request',*values)
```

#### Redis pull

```python
item_list = REDIS.lrange('aiohttp-rq-response',0,-1)
data_list = list(map(lambda i:i.encode('utf-8'),item_list))

item_list = REDIS.lrange('aiohttp-rq-exception',0,-1)
data_list = list(map(lambda i:i.encode('utf-8'),item_list))
```
