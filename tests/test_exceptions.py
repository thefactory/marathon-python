import json

import requests

from marathon.exceptions import MarathonHttpError, InternalServerError


def test_400_error():
    fake_response = requests.Response()
    fake_message = "Invalid JSON"
    fake_details = [{"path": "/taskKillGracePeriodSeconds", "errors": ["error.expected.jsnumber"]}]
    fake_response._content = json.dumps({"message": fake_message, "details": fake_details}).encode()
    fake_response.status_code = 400
    fake_response.headers['Content-Type'] = 'application/json'

    exc = MarathonHttpError(fake_response)
    assert exc.status_code == 400
    assert exc.error_message == fake_message
    assert exc.error_details == fake_details


def test_503_error():
    fake_response = requests.Response()
    fake_response._content = """<head>
<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1"/>
<title>Error 503 </title>
</head>
<body>
<h2>HTTP ERROR: 503</h2>
</body>
</html>"""
    fake_response.reason = "reason"
    fake_response.status_code = 503

    exc = InternalServerError(fake_response)
    assert exc.status_code == 503
    assert exc.error_message == "reason"
    assert not hasattr(exc, 'error_details')
