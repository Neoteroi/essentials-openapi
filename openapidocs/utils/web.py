from typing import Any

import httpx

http_client = httpx.Client(verify=False, timeout=20)


class FailedRequestError(Exception):
    def __init__(self, message) -> None:
        super().__init__(
            f"Failed request: {message}. "
            "Inspect the inner exception (__context__) for more information."
        )

    @property
    def inner_exception(self):
        return self.__context__


def ensure_success(response: httpx.Response) -> None:
    if response.status_code < 200 or response.status_code > 399:
        raise FailedRequestError(
            "Response status does not indicate success: "
            f"{response.status_code} {response.reason_phrase}"
        )


def http_get(url: str) -> Any:
    try:
        return http_client.get(url)
    except httpx.HTTPError as http_error:
        raise FailedRequestError(str(http_error)) from http_error
