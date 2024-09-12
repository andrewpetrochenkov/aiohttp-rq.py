+   logging
    +   `DEBUG`, `ERROR` level messages
    +   `logging.conf` support
+   request `id`
    +   input: `id` required
    +   output: `request_id`
    +   `AIOHTTP_RQ_DIR`/`id` content path

redis data format:
+   request: `id`, `method`,`url`, `headers`, `data`,`allow_redirects`
+   response: `request_id`, `status`, `headers`
+   request exception: `request_id`, `exc_class`, `exc_message`

