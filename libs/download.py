import asyncio
import logging
import os
from contextlib import closing

import aiohttp


def track_filename(message):
    f = open(os.path.join('.', 'track.txt'), '+a')
    message = "{0}\n".format(message)
    f.write(message)
    f.close()


@asyncio.coroutine
def fetch(destination, url, session, semaphore, chunk_size=1 << 15):
    with (yield from semaphore):
        logging.info('downloading %s', destination)

        try:
            response = yield from session.get(url, timeout=30)
        except asyncio.TimeoutError:
            track_filename(str(destination) + ";" + url)
            print("Sorry, server couldn't be reached.")
            response = yield from session.get(url, timeout=30)

        with closing(response), open(destination, 'wb') as file:
            while True:  # save file
                chunk = yield from response.content.read(chunk_size)
                if not chunk:
                    break
                file.write(chunk)
        logging.info('done %s', destination)

    return destination, (response.status, tuple(response.headers.items()))


def download(urls):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    with closing(aiohttp.ClientSession()) as session:
        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(4)
        download_tasks = (fetch(destination, url, session, semaphore) for destination, url in urls)
        loop.run_until_complete(asyncio.gather(*download_tasks))