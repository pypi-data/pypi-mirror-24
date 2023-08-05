import asyncio
import concurrent.futures
import logging
import threading
import time
from collections import Mapping
from typing import NamedTuple
from typing import Optional

import aiohttp
from bravado.http_client import HttpClient
from bravado.http_future import FutureAdapter
from bravado.http_future import HttpFuture
from bravado_core.response import IncomingResponse

log = logging.getLogger(__name__)


AsyncioResponse = NamedTuple(
    'AsyncioResponse', [
        ('response', aiohttp.ClientResponse),
        ('remaining_timeout', Optional[float])
    ]
)


loop = None
client_session = None


def run_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def get_loop():
    global loop
    if loop is None:
        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=run_event_loop, args=(loop,), daemon=True)
        thread.start()
    return loop


def get_client_session():
    global client_session
    if client_session:
        return client_session
    client_session = aiohttp.ClientSession(loop=get_loop())
    return client_session


class AioHTTPResponseAdapter(IncomingResponse):
    """Wraps a aiohttp Response object to provide a bravado-like interface
    to the response innards.
    """

    def __init__(self, response: AsyncioResponse):
        self._delegate = response.response
        self._remaining_timeout = response.remaining_timeout

    @property
    def status_code(self):
        return self._delegate.status

    @property
    def text(self):
        future = asyncio.run_coroutine_threadsafe(self._delegate.text(), get_loop())
        return future.result(self._remaining_timeout)

    @property
    def reason(self):
        return self._delegate.reason

    @property
    def headers(self):
        return self._delegate.headers

    def json(self, **_):
        future = asyncio.run_coroutine_threadsafe(self._delegate.json(), get_loop())
        return future.result(self._remaining_timeout)


class AsyncioClient(HttpClient):
    """Asynchronous HTTP client using the asyncio event loop.
    """

    def request(self, request_params, operation=None, response_callbacks=None,
                also_return_response=False):
        """Sets up the request params as per Twisted Agent needs.
        Sets up crochet and triggers the API request in background

        :param request_params: request parameters for the http request.
        :type request_params: dict
        :param operation: operation that this http request is for. Defaults
            to None - in which case, we're obviously just retrieving a Swagger
            Spec.
        :type operation: :class:`bravado_core.operation.Operation`
        :param response_callbacks: List of callables to post-process the
            incoming response. Expects args incoming_response and operation.
        :param also_return_response: Consult the constructor documentation for
            :class:`bravado.http_future.HttpFuture`.

        :rtype: :class: `bravado_core.http_future.HttpFuture`
        """

        client_session = get_client_session()
        data = request_params.get('data', {})
        files = request_params.get('files', {})
        if isinstance(data, Mapping) and files:
            data.update({
                field_name: file_tuple[1]
                for field_name, file_tuple in files
            })

        coroutine = client_session.request(
            method=request_params.get('method') or 'GET',
            url=request_params.get('url'),
            params=request_params.get('params'),
            data=data,
            headers=request_params.get('headers'),
        )

        future = asyncio.run_coroutine_threadsafe(coroutine, get_loop())

        return HttpFuture(
            AsyncioFutureAdapter(future),
            AioHTTPResponseAdapter,
            operation,
            response_callbacks,
            also_return_response,
        )


class AsyncioFutureAdapter(FutureAdapter):
    def __init__(self, future: concurrent.futures.Future) -> None:
        self.future = future

    def result(self, timeout: Optional[float]=None) -> AsyncioResponse:
        start = time.time()
        response = self.future.result(timeout)
        time_elapsed = time.time() - start
        remaining_timeout = timeout - time_elapsed if timeout else None

        return AsyncioResponse(response=response, remaining_timeout=remaining_timeout)
