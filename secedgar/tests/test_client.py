import pytest
import requests

from secedgar.client import NetworkClient
from secedgar.utils.exceptions import EDGARQueryError
from secedgar.tests.utils import datapath


@pytest.fixture
def client():
    return NetworkClient()


class MockNoCIKFoundBadResponse:
    """Returns response with 'No matching CIK' message."""

    def __init__(self, *args, **kwargs):
        self.status_code = 200
        with open(datapath('CIK', 'cik_not_found.html')) as f:
            self.text = f.read()


class MockMultipleFilingTypesGoodResponse:
    """Returns response with list of filings (multiple types) for single CIK."""

    def __init__(self, *args, **kwargs):
        self.status_code = 200
        with open(datapath('CIK', 'single_cik_search_result.html'), encoding='iso-8859-1') as f:
            self.text = f.read()


class MockSingleFilingTypeGoodResponse:
    """Returns response with list of single filing type for single CIK."""

    def __init__(self, *args, **kwargs):
        self.status_code = 200
        with open(datapath('CIK', 'single_cik_multiple_filings_10k.html')) as f:
            self.text = f.read()


class MockMultipleCIKResultsGoodResponse:
    """Returns page with multiple results for CIK when validating CIK."""

    def __init__(self, *args, **kwargs):
        self.status_code = 200
        with open(datapath('CIK', 'cik_multiple_results.html')) as f:
            self.text = f.read()


class MockSingleFilingPageGoodResponse:
    """Returns page for one filing for one company."""

    def __init__(self, *args, **kwargs):
        self.status_code = 200
        with open(datapath('CIK', 'single_filing_page.html')) as f:
            self.text = f.read()


class TestClient:
    def test_client_bad_response_raises_error(self, monkeypatch, client):
        monkeypatch.setattr(requests, 'get', MockNoCIKFoundBadResponse)
        with pytest.raises(EDGARQueryError):
            client.get_response('path', {})

    def test_client_good_response_single_filing_type_passes(self, monkeypatch, client):
        monkeypatch.setattr(requests, 'get', MockSingleFilingTypeGoodResponse)
        assert client.get_response('path', {})

    def test_client_good_response_multiple_cik_results_passes(self, monkeypatch, client):
        monkeypatch.setattr(requests, 'get', MockMultipleCIKResultsGoodResponse)
        assert client.get_response('path', {})

    def test_client_good_response_single_filing_passes(self, monkeypatch, client):
        monkeypatch.setattr(requests, 'get', MockSingleFilingPageGoodResponse)
        assert client.get_response('path', {})
