"""Unit tests with mocked HTTP responses for eurlex functionality."""

from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from eurlex.eurlex import Eurlex


@pytest.fixture
def eur():
    return Eurlex()


@pytest.fixture
def caselaw_query(eur):
    return eur.make_query(resource_type="caselaw", order=True, limit=10)


# --- make_query tests (no mocking needed, pure logic) ---


def test_make_query_returns_string(eur):
    q = eur.make_query(resource_type="caselaw", order=True, limit=10)
    assert isinstance(q, str)
    assert "PREFIX" in q
    assert "limit 10" in q


def test_make_query_directive(eur):
    q = eur.make_query(
        resource_type="directive",
        include_date=True,
        include_force=True,
        include_date_force=True,
        include_date_endvalid=True,
        include_date_transposed=True,
        include_date_lodged=True,
        include_lbs=True,
    )
    assert "DIR" in q
    assert "date" in q


def test_make_query_all_resource_types(eur):
    for rt in [
        "any",
        "directive",
        "regulation",
        "decision",
        "recommendation",
        "international_agreement",
        "caselaw",
        "caselaw_proper",
        "ag_opinion",
        "proposal",
        "national_implementation",
    ]:
        q = eur.make_query(resource_type=rt)
        assert len(q) > 100
        assert "PREFIX" in q


def test_make_query_manual_with_type(eur):
    q = eur.make_query(resource_type="manual", manual_type="JUDG")
    assert "JUDG" in q


def test_make_query_manual_without_type_raises(eur):
    with pytest.raises(Exception):
        eur.make_query(resource_type="manual")


def test_make_query_caselaw_options(eur):
    q = eur.make_query(
        resource_type="caselaw",
        include_advocate_general=True,
        include_court_procedure=True,
        include_court_formation=True,
        include_judge_rapporteur=True,
        include_court_scholarship=True,
        include_ecli=True,
    )
    assert "advocate-general" in q
    assert "ecli" in q


def test_make_query_directive_extras(eur):
    q = eur.make_query(
        resource_type="directive",
        include_eurovoc=True,
        include_author=True,
        include_citations=True,
        include_directory=True,
        include_sector=True,
        include_proposal=True,
    )
    assert "eurovoc" in q
    assert "author" in q
    assert "citation" in q


def test_make_query_sector_filter(eur):
    q = eur.make_query(
        resource_type="directive",
        include_directory=True,
        directory="04.10.30.00",
        limit=10,
    )
    assert "04.10.30.00" in q


def test_make_query_sector_number(eur):
    q = eur.make_query(
        resource_type="directive",
        sector=9,
        limit=10,
    )
    assert "9" in q


def test_make_query_no_order(eur):
    q = eur.make_query(resource_type="caselaw", order=False)
    assert "order by" not in q


def test_make_query_no_corrigenda(eur):
    q = eur.make_query(resource_type="directive", include_corrigenda=False)
    assert "CORRIGENDUM" in q


# --- query_eurlex tests (mock sparql_dataframe) ---


@patch("eurlex.eurlex.sparql_dataframe.get")
def test_query_eurlex_success(mock_get, eur, caselaw_query):
    mock_df = pd.DataFrame({"work": [f"http://example.org/{i}" for i in range(10)]})
    mock_get.return_value = mock_df
    result = eur.query_eurlex(caselaw_query)
    assert len(result) == 10
    mock_get.assert_called_once()


@patch("eurlex.eurlex.sparql_dataframe.get")
def test_query_eurlex_error_returns_empty(mock_get, eur, caselaw_query):
    mock_get.side_effect = Exception("No columns to parse from file")
    result = eur.query_eurlex(caselaw_query)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


# --- get_data tests (mock requests) ---


TITLE_XML = """<?xml version="1.0"?>
<akomaNtoso>
<EXPRESSION_TITLE>
Judgment of the Court # Van Gend en Loos v Administratie der Belastingen # Case 26/62.
</EXPRESSION_TITLE>
</akomaNtoso>"""

TITLE_XML_NO_HASH = """<?xml version="1.0"?>
<akomaNtoso>
<EXPRESSION_TITLE>Council Directive 2006/112/EC</EXPRESSION_TITLE>
</akomaNtoso>"""


@patch("eurlex.eurlex.requests.get")
def test_get_data_title_with_caselaw_metadata(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = TITLE_XML
    mock_get.return_value = mock_response
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "title",
        extract_caselaw_metadata=True,
    )
    assert d["title"] == "Judgment of the Court"
    assert d["parties"] == "Van Gend en Loos v Administratie der Belastingen"
    assert d["case_number"] == "Case 26/62"


@patch("eurlex.eurlex.requests.get")
def test_get_data_title_no_extract(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = TITLE_XML_NO_HASH
    mock_get.return_value = mock_response
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "title",
        extract_caselaw_metadata=False,
    )
    assert "Council Directive" in d["title"]
    assert d["parties"] == "NaN"


@patch("eurlex.eurlex.requests.get")
def test_get_data_title_no_hash_with_extract(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = TITLE_XML_NO_HASH
    mock_get.return_value = mock_response
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "title",
        extract_caselaw_metadata=True,
    )
    assert d["parties"] == "NaN"
    assert d["case_number"] == "NaN"


@patch("eurlex.eurlex.requests.get")
def test_get_data_title_non200_returns_status(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "title",
    )
    assert d["title"] == "404"


@patch("eurlex.eurlex.requests.get")
def test_get_data_text_html(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html; charset=UTF-8"}
    mock_response.content = (
        b"<html><body>Some legal text here that is long enough.</body></html>"
    )
    mock_get.return_value = mock_response
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "text",
    )
    assert isinstance(d, str)
    assert "Some legal text" in d


@patch("eurlex.eurlex.requests.get")
def test_get_data_text_pdf(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/pdf"}
    mock_response.content = b"%PDF-fake"
    mock_get.return_value = mock_response
    with patch("eurlex.eurlex.extract_text", return_value="PDF extracted text"):
        d = eur.get_data(
            "http://publications.europa.eu/resource/cellar/abc123",
            "text",
        )
    assert isinstance(d, str)
    assert "PDF extracted text" in d


@patch("eurlex.eurlex.requests.get")
def test_get_data_text_300_multiple_links(mock_get, eur):
    first_response = MagicMock()
    first_response.status_code = 300
    first_response.content = (
        b'<html><body><a href="http://example.org/doc1">doc1</a></body></html>'
    )

    second_response = MagicMock()
    second_response.status_code = 200
    second_response.headers = {"Content-Type": "text/html"}
    second_response.content = b"<html><body>Document text</body></html>"

    mock_get.side_effect = [first_response, second_response]
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "text",
    )
    assert isinstance(d, str)


@patch("eurlex.eurlex.requests.get")
def test_get_data_ids(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"""<?xml version="1.0"?>
<identifiers>
<VALUE>CELEX:62016CJ0001</VALUE>
<VALUE>ECLI:EU:C:2016:1</VALUE>
</identifiers>"""
    mock_get.return_value = mock_response
    d = eur.get_data(
        "http://publications.europa.eu/resource/cellar/abc123",
        "ids",
    )
    assert len(d) == 2
    assert "CELEX:62016CJ0001" in d


@patch("eurlex.eurlex.requests.get")
def test_get_data_celex_number_converted_to_url(mock_get, eur):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = TITLE_XML_NO_HASH
    mock_get.return_value = mock_response
    eur.get_data("32016R0679", "title")
    call_url = mock_get.call_args[0][0]
    assert call_url == "http://publications.europa.eu/resource/celex/32016R0679"


# --- download_xml tests (mock requests) ---


@patch("builtins.open", mock_open())
@patch("eurlex.eurlex.requests.get")
@patch("eurlex.eurlex.requests.head")
def test_download_xml_object(mock_head, mock_get, eur):
    mock_head_resp = MagicMock()
    mock_head_resp.status_code = 200
    mock_head_resp.url = "http://publications.europa.eu/resource/cellar/redirected"
    mock_head.return_value = mock_head_resp

    mock_get_resp = MagicMock()
    mock_get_resp.content = b"<xml>object notice content</xml>"
    mock_get.return_value = mock_get_resp

    result = eur.download_xml(
        "http://publications.europa.eu/resource/cellar/abc123",
        notice="object",
    )
    assert "object" in result


@patch("builtins.open", mock_open())
@patch("eurlex.eurlex.requests.get")
@patch("eurlex.eurlex.requests.head")
def test_download_xml_branch(mock_head, mock_get, eur):
    mock_head_resp = MagicMock()
    mock_head_resp.status_code = 200
    mock_head_resp.url = "http://publications.europa.eu/resource/cellar/redirected"
    mock_head.return_value = mock_head_resp

    mock_get_resp = MagicMock()
    mock_get_resp.content = b"<xml>branch notice content</xml>"
    mock_get.return_value = mock_get_resp

    result = eur.download_xml(
        "http://publications.europa.eu/resource/cellar/abc123",
        notice="branch",
    )
    assert "branch" in result


@patch("builtins.open", mock_open())
@patch("eurlex.eurlex.requests.get")
@patch("eurlex.eurlex.requests.head")
def test_download_xml_celex_number(mock_head, mock_get, eur):
    mock_head_resp = MagicMock()
    mock_head_resp.status_code = 200
    mock_head_resp.url = "http://publications.europa.eu/resource/celex/32016R0679"
    mock_head.return_value = mock_head_resp

    mock_get_resp = MagicMock()
    mock_get_resp.content = b"<xml>some content</xml>"
    mock_get.return_value = mock_get_resp

    result = eur.download_xml("32016R0679", notice="object")
    assert result


@patch("eurlex.eurlex.requests.head")
def test_download_xml_head_fails(mock_head, eur):
    mock_head_resp = MagicMock()
    mock_head_resp.status_code = 404
    mock_head.return_value = mock_head_resp
    with pytest.raises(AssertionError, match="unsuccessful"):
        eur.download_xml(
            "http://publications.europa.eu/resource/cellar/abc123",
            notice="object",
        )


def test_download_xml_invalid_notice(eur):
    with pytest.raises(AssertionError):
        eur.download_xml(
            "http://publications.europa.eu/resource/cellar/abc123",
            notice="invalid",
        )
