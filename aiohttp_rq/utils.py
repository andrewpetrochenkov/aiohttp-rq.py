import io
import json
import logging
import os
import sys
import uuid

import aiohttp


CONNECTOR_LIMIT = int(os.getenv("AIOHTTP_RQ_CONNECTOR_LIMIT", 100))
CONNECTOR_LIMIT_PER_HOST = int(os.getenv("AIOHTTP_RQ_CONNECTOR_LIMIT_PER_HOST", 0))
CHUNK_SIZE = int(os.getenv("AIOHTTP_RQ_CHUNK_SIZE", 100 * 1024))  # 100 KB Default
TTL_DNS_CACHE = int(os.getenv("AIOHTTP_RQ_TTL_DNS_CACHE", 10))  # 10 Default

TIMEOUT_TOTAL = os.getenv("AIOHTTP_RQ_TIMEOUT_TOTAL", None)
TIMEOUT_CONNECT = os.getenv("AIOHTTP_RQ_TIMEOUT_CONNECT", None)
TIMEOUT_SOCK_CONNECT = os.getenv("AIOHTTP_RQ_TIMEOUT_SOCK_CONNECT", None)
TIMEOUT_SOCK_READ = os.getenv("AIOHTTP_RQ_TIMEOUT_SOCK_READ", None)

def get_aiohttp_connector():
    # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.TCPConnector
    return aiohttp.TCPConnector(
        limit=CONNECTOR_LIMIT,  # default 100
        limit_per_host=CONNECTOR_LIMIT_PER_HOST,  # default 0
        ttl_dns_cache=TTL_DNS_CACHE
        #enable_cleanup_closed=True,
    )

def get_aiohttp_timeout():
    # https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientTimeout
    kwargs = {
        'total':TIMEOUT_TOTAL,
        'connect':TIMEOUT_CONNECT,
        'sock_connect':TIMEOUT_SOCK_CONNECT,
        'sock_read':TIMEOUT_SOCK_READ,
    }
    return aiohttp.ClientTimeout(
        **{k: int(v) for k, v in kwargs.items() if v is not None}
    )

def get_client_session_kwargs():
    return dict(
        connector=get_aiohttp_connector(),
        timeout=get_aiohttp_timeout()
    )

async def write_content(response,content_path):
    f = io.BytesIO()
    try:
        while True:
            chunk = await response.content.read(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)
        content_dir = os.path.dirname(content_path)
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
        with open(str(content_path), "wb") as fd:
            fd.write(f.getbuffer())
    finally:
        f.close()
