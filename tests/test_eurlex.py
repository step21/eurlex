import pytest

import eurlex
from eurlex import __version__
from eurlex.eurlex import Eurlex

limit = 10


@pytest.fixture
def eurlex_inst():
    eur = Eurlex()
    return eur


@pytest.fixture
def some_query(eurlex_inst):
    q = eurlex_inst.make_query(resource_type="caselaw", order=True, limit=limit)
    return q


def test_make_query(some_query):
    print(some_query)
    assert some_query
    assert "PREFIX" in some_query


def test_make_query_directive(eurlex_inst):
    # TODO - split this so each test only tests on thing
    directive_query = eurlex_inst.make_query(
        resource_type="directive",
        include_date=True,
        include_force=True,
        include_date_force=True,
        include_date_endvalid=True,
        include_date_transposed=True,
        include_date_lodged=True,
        include_lbs=True,
    )
    assert directive_query
    assert "PREFIX" in directive_query


def test_query_eurlex(some_query):
    # query, endpoint
    eur = Eurlex()
    q = eur.query_eurlex(some_query)
    assert len(q) == 10


# eur.download_xml("http://publications.europa.eu/resource/celex/32016R0679", notice="object", filename="test.xml")
#       >>> eur.download_xml("32016R0679", notice="object", filename="test.xml")
# 21         >>> eur.download_xml("32014R0001", notice="tree")
# 22         >>> eur.download_xml("32014R0001", notice="branch")
def test_download_xml(eurlex_inst):
    x = eurlex_inst.download_xml(
        "http://publications.europa.eu/resource/celex/32016R0679",
        notice="object",
        filename="test.xml",
    )
    # x = eurlex_inst.download_xml("http://publications.europa.eu/resource/celex/32016R0679", notice = "tree" filename = "test.xml")
    # x = eurlex_inst.download_xml("http://publications.europa.eu/resource/celex/32016R0679", notice = "branch" filename = "test.xml")

    # url, notice, filename, languages, mode
    assert "xml" in x


def test_get_data(eurlex_inst):
    # url, data_type, notice, languages, include_breaks
    d = eurlex_inst.get_data("61962CJ0026", data_type="text")
    assert d
    assert len(d) > 500


"""Test extraction of metadata where extraction should work"""


def test_get_data_extract_succeed(eurlex_inst):
    d = eurlex_inst.get_data(
        "http://publications.europa.eu/resource/cellar/7979a0c9-5699-4b63-b48d-13d8f1a6cc22",
        "title",
        extract_caselaw_metadata=True,
    )
    assert d["parties"] != "NaN"
    assert d["case_number"] != "NaN"


"""Test data extraction where it is expected to fail"""


def test_get_data_extract_fail(eurlex_inst):
    d = eurlex_inst.get_data(
        "http://publications.europa.eu/resource/cellar/a01cca15-ed79-4ea3-bd7a-5f3aa57cbcda",
        "title",
        extract_caselaw_metadata=True,
    )
    assert d["title"] != "NaN"
    assert d["parties"] == "NaN"
    assert d["case_number"] == "NaN"


"""Testing getting the title without metadata extraction"""


def test_get_data_no_extract(eurlex_inst):
    d = eurlex_inst.get_data(
        "http://publications.europa.eu/resource/cellar/7979a0c9-5699-4b63-b48d-13d8f1a6cc22",
        "title",
        extract_caselaw_metadata=False,
    )
    assert len(d["title"]) > 50
    assert d["parties"] == "NaN"
    assert d["case_number"] == "NaN"
