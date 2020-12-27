import datetime
import gzip
import io

from flask import Response, current_app, request


def get_utc_now() -> datetime.datetime:
    """Returns the utc time independently from system time.

    Returns:
        datetime.datetime: datetime object with utc time
    """
    return datetime.datetime.utcnow()


def gzip_response(resp: Response) -> Response:
    if "gzip" not in request.headers.get("Accept-Encoding", ""):
        return resp

    # not worth to gzip < 1500 bytes
    if resp.is_json and int(resp.headers.get("Content-Length")) > 1500:
        # Get the content and gzip it
        out = io.BytesIO()

        with gzip.GzipFile(fileobj=out, mode="wb") as fp:
            fp.write(resp.get_data())

        # Update resp
        resp.set_data(out.getvalue())
        resp.headers["Content-Encoding"] = "gzip"

    return resp


def set_cors_header(response: Response) -> Response:
    """Enables CORS when using development.

    Args:
        response (Response): The response object to set the headers to.

    Returns:
        Response: Same response object with new headers.
    """
    if current_app.config.get("ENV") == "development":
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Credentials", True)

    return response
