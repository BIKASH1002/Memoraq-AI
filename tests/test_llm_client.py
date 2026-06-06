import pytest
from google.genai.errors import APIError

from src import llm_client


class FakeModels:
    def __init__(self, results):
        self.results = iter(results)
        self.calls = 0

    def generate_content(self, **kwargs):
        self.calls += 1
        result = next(self.results)
        if isinstance(result, Exception):
            raise result
        return result


class FakeClient:
    def __init__(self, results):
        self.models = FakeModels(results)


class FakeResponse:
    text = "Generated memo"


def api_error(code):
    return APIError(code, {"status": "UNAVAILABLE", "message": "Busy"})


def set_fake_client(monkeypatch, results):
    client = FakeClient(results)
    monkeypatch.setattr(llm_client.genai, "Client", lambda api_key: client)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(llm_client.time, "sleep", lambda delay: None)
    return client


def test_retries_busy_api_errors(monkeypatch):
    client = set_fake_client(
        monkeypatch,
        [api_error(503), api_error(429), FakeResponse()],
    )
    retries = []

    result = llm_client.generate_decision_memo(
        "prompt",
        on_retry=lambda attempt, max_retries, delay: retries.append(
            (attempt, max_retries, delay)
        ),
    )

    assert result == "Generated memo"
    assert client.models.calls == 3
    assert retries == [(1, 2, 1), (2, 2, 2)]


def test_does_not_retry_non_busy_api_errors(monkeypatch):
    client = set_fake_client(monkeypatch, [api_error(400)])

    with pytest.raises(APIError):
        llm_client.generate_decision_memo("prompt")

    assert client.models.calls == 1


def test_raises_after_busy_api_retries_are_exhausted(monkeypatch):
    client = set_fake_client(
        monkeypatch,
        [api_error(503), api_error(503), api_error(503)],
    )

    with pytest.raises(APIError):
        llm_client.generate_decision_memo("prompt")

    assert client.models.calls == 3
