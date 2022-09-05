"""
* Python module to create eurlex cellar queries, query eurlex for metadata of documents with sparql queries, and subsequently download associated documents and notices.
"""
import os
import re
import requests
import sparql_dataframe


try:
    from typing import Literal, get_args
except ImportError:
    from typing_extensions import Literal, get_args
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import pandas as pd
from halo import Halo
from fire import Fire


class Eurlex:
    """The sole class of the pyeurlex module."""

    def __init__(
        self,
        endpoint="http://publications.europa.eu/webapi/rdf/sparql",
        sparql_query="",
    ):
        self.endpoint = endpoint
        self.sparql_query = sparql_query
        # self.document_type = document_type
        # self.output_dir = output_dir

    # Language = ""ENG":"English""
    # Supported resource types if manual_type is not used
    _RESOURCE_TYPES = Literal[
        "any",
        "directive",
        "regulation",
        "decision",
        "recommendation",
        "international_agreement",  # AGREE_INTERNATION
        "caselaw",
        "caselaw_proper",
        "ag_opinion",  # Advocate General Opinion (OPIN_AG)
        "manual",
        "proposal",
        "national_implementation",
    ]
    # This method constructs a SPARQL query to query the EU Cellar endpoint """
    def make_query(
        self,
        resource_type: _RESOURCE_TYPES = "caselaw",
        # language="ENG",  # could also add literals etc for these
        manual_type: str = "",
        directory=None,
        sector=None,
        include_corrigenda: bool = False,
        include_celex: bool = True,
        include_lbs: bool = False,
        include_date: bool = False,
        include_date_force: bool = False,
        include_date_endvalid: bool = False,
        include_date_transposed: bool = False,
        include_date_lodged: bool = False,
        include_force: bool = False,
        include_eurovoc: bool = False,
        include_author: bool = False,
        include_citations: bool = False,
        include_court_procedure: bool = False,
        include_ecli: bool = False,
        include_advocate_general: bool = False,
        include_judge_rapporteur: bool = False,
        include_court_formation: bool = False,
        include_court_scholarship: bool = False,
        include_proposal: bool = False,
        include_directory: bool = False,
        include_sector: bool = False,
        order: bool = False,
        limit: int = None,
    ):
        """
        Construct a SPARQL query to retrieve documents from EU Cellar repository

        This function adds bits of SPARQL code together. It does some type and sanity checking, but it is likely still possible to make get nonsensical queries, and not the full range that is possible with handcoded SPARQL is supported. As an example, some language filtering is done to get mostly English results, but this is not consistent and no other language can be specified at the moment.
        Possible resource types can be found at http://publications.europa.eu/resource/authority/resource-type

        Parameters
        ----------
        resource_type: _RESOURCE_TYPES
            Defines the most common resources supported, mapping to one or more resource types in the EU semantic data structure. Possible options are any, directive, regulation, decision ,recommendation, international_agreement, caselaw, caselaw_proper, ag_opinion, manual, proposal, national_implementation
            Default: caselaw
        manual_type: string
            A string that specifies a custom resource type as set out in official documentation, if pre-defined resource types are not sufficient. Possible types can be found here: http://publications.europa.eu/resource/authority/resource-type This is a string that is inserted into the query, so it is possible to specify multiple types, but this is not checked for validity.
            Default: None
        directory: string
            A string that specifies a directory to filter on. This is a string that is inserted into the query, so it is possible to specify multiple directories, but this is not checked for validity.
            Default: None
        sector: string
            A string that specifies a sector to filter on. This is a string that is inserted into the query, so it is possible to specify multiple sectors, but this is not checked for validity.
            Default: None
        include_corrigenda: bool
            Whether to include corrigenda in the results. Corrigenda are documents that correct errors in previous documents.
            Default: False
        include_celex: bool
            Whether to include CELEX numbers in the results.
            Default: True
        include_lbs: bool
            Whether to include the legal basis of documents (legislation) in the results.
            Default: False
        include_date: bool
            Whether to include the date of documents in the results.
            Default: False
        include_date_force: bool
            Whether to include the date entering into force of acts/documents in the results.
            Default: False
        include_date_endvalid: bool
            Whether to include the date of the end of validity of acts/documents in the results.
            Default: False
        include_date_transposed: bool
            Whether to include the date of the transposition deadline for directives in the results.
            Default: False
        include_date_lodged: bool
            Whether to include the date of when a court case was lodged with the court.
            Default: False
        include_force: bool
            Whether to include a field to specify if the legislation is in force or not.
            Default: False
        include_eurovoc: bool
            Whether to include the Eurovoc terms associated with the document in the results.
            Default: False
        include_author: bool
            Whether to include the author(s) of the document in the results.
            Default: False
        include_citations: bool
            Whether to include the citations (CELEX-labeled) in the results.
            Default: False
        include_court_procedure: bool
            Whether the results include the type of court procedure and outcome.
            Default: False
        include_ecli: bool
            Whether to include the ECLI identifier for court documents in the results.
            Default: False
        include_advocate_general: bool
            Whether to include the advocate general's opinion in the results.
            Default: False
        include_judge_rapporteur: bool
            The results include the judge rapporteur.
            Default: False
        include_court_formation: bool
            Whether to include the court formation in the results.
            Default: False
        include_court_scholarship: bool
            Whether to include court-curated, relevant scholarship in the results.
            Default: False
        include_proposal: bool
            Results include the CELEX of the proposal of the adopted legal act.
            Default: False
        include_directory: bool
            Results include the EURLEX directory code.
            Default: False
        include_sector: bool
            Results include the EURLEX sector code.
            Default: False
        order: bool
            Whether to order the results by IDs
        limit: int
            The maximum number of results to return. If None, all results are returned.
            Default: None
        Returns
        -------
        string
            SPARQL query
        Examples
        --------
        >>> from eurlex import Eurlex
        >>> eur = Eurlex()
        >>> eur.make_query(resource_type = "directive", include_advocate_general = False, include_ecli = False) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        PREFIX ...
        >>> eur.make_query(resource_type = "caselaw", order = True, limit = 10) # doctest: +ELLIPSIS
        PREFIX ...
        >>> eur.make_query(resource_type = "ag_opinion", order = True, limit = 10) # doctest: +ELLIPSIS
        PREFIX ...
        >>> eur.make_query(resource_type = "manual", manual_type = "SWD") # doctest: +ELLIPSIS
        PREFIX ...
        """
        if __name__ == "__main__":
            spinner = Halo(text="Appending query text...", spinner="line")
            spinner.start()
        assert resource_type is not None, "resource_type must be specified"
        assert resource_type in get_args(
            self._RESOURCE_TYPES
        ), f"'{resource_type}' is invalid - valid options are {get_args(self._RESOURCE_TYPES)}"
        if resource_type == "manual":
            assert (
                len(manual_type) > 2
            ), f"{manual_type} is invalid - please specify a proper type from http://publications.europa.eu/resource/authority/resource-type"
        if resource_type in ["caselaw", "manual", "any"] and include_court_procedure:
            raise Exception(
                "Resource and variable requested are incompatible"
            )  # improve exception handling
        if include_date_transposed and resource_type != "directive":
            raise Exception("Transposition date only available for directives.")

        query = """PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
  PREFIX annot: <http://publications.europa.eu/ontology/annotation#>
  PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
  PREFIX dc:<http://purl.org/dc/elements/1.1/>
  PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
  PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX owl:<http://www.w3.org/2002/07/owl#>
  select distinct ?work ?type"""

        # add parameter for celex id
        if include_celex:
            query += " ?celex"
        # add parameter for date
        if include_date:
            query += " ?date"
        if include_date_force:
            query += " ?dateforce"
        if include_date_endvalid:
            query += " ?dateendvalid"
        if include_date_transposed:
            query += " ?datetranspos"
        if include_date_lodged:
            query += " ?datelodged"
        if include_lbs:
            assert (
                resource_type != "caselaw"
            ), "legal basis variable not compatible with caselaw resource type"
            query += " ?lbs ?lbcelex ?lbsuffix"
        if include_force:
            assert (
                resource_type != "caselaw"
            ), "force variable not compatible with caselaw resource type"
            query += " ?force"
        if include_eurovoc:
            query += " ?eurovoc"
        if include_court_procedure:
            query += " ?courtprocedure"
        if include_ecli:
            query += " ?ecli"
        if include_author:
            query += " ?author"
        if include_citations:
            query += " ?citationcelex"
        if include_directory:
            query += " ?directory"
        if include_sector:
            query += " ?sector"
        if include_advocate_general:
            query += " ?ag"
        if include_judge_rapporteur:
            query += " ?jr"
        if include_court_formation:
            query += " ?cf"
        if include_court_scholarship:
            query += " ?scholarship"
        if include_proposal:
            query += " ?proposal"
        if resource_type == "any":
            query += " where{"
        if resource_type != "any":
            query += " where{ ?work cdm:work_has_resource-type ?type."
        if directory:
            assert isinstance(directory, "str"), "directory code must be of type string"
            query += (
                """ VALUES (?value)
                    { (<http://publications.europa.eu/resource/authority/fd_555/"""
                + directory
                + """>)
                    (<http://publications.europa.eu/resource/authority/dir-eu-legal-act/"""
                + directory
                + """>)
                    }
                    {?work cdm:resource_legal_is_about_concept_directory-code ?value.
                    }
                    UNION
                    {?work cdm:resource_legal_is_about_concept_directory-code ?directory.
                    ?value skos:narrower+ ?directory.
                    }"""
            )
            # maybe use textwrap.dedent() to not have unneessary or hindering whitespace in the query
        if sector:
            assert isinstance(sector, int), "sector code must be of type integer"
            assert sector in range(0, 10), "sector code must be between 0 and 9"
            query += (
                """?work cdm:resource_legal_id_sector ?sector.
                    FILTER(str(?sector)='"""
                + sector
                + "')"
            )
        if resource_type == "directive":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/DIR>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_IMPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_DEL>)"""
        if resource_type == "recommendation":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/RECO>||?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_DEC>||
                   ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_DIR>||
                   ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_OPIN>||
                   ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_RES>||
                   ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_REG>||
                   ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_RECO>||
                   ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_DRAFT>)"""
        if resource_type == "regulation":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/REG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_IMPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_FINANC>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_DEL>)"""
        if resource_type == "international_agreement":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_INTERNATION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/EXCH_LET>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_PROT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ACT_ADOPT_INTERNATION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ARRANG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/CONVENTION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_AMEND>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_ADOPT_INTERNATION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_ADOPT_INTERNATION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_ADOPT_INTERNATION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/MEMORANDUM_UNDERST>)"""
        if resource_type == "decision":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/DEC>||
            ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_ENTSCHEID>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_IMPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_DEL>)||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_FRAMW>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JOINT_DEC>)"""
        if resource_type == "caselaw":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/JUDG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ORDER>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/OPIN_JUR>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/THIRDPARTY_PROCEED>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/GARNISHEE_ORDER>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/RULING>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JUDG_EXTRACT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/INFO_JUDICIAL>)"""
        if resource_type == "caselaw_proper":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/JUDG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ORDER>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/RULING>)"""
        if resource_type == "ag_opinion":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/VIEW_AG>||
            ?type=<http://publications.europa.eu/resource/authority/resource-type/OPIN_AG>)"""
        if resource_type == "proposal":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DIR>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_REG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DEC>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DEC_IMPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_REG_IMPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DIR_IMPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_RECO>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JOINT_PROP_DEC>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JOINT_PROP_ACTION>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JOINT_PROP_REG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JOINT_PROP_DIR>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_RES>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_AMEND>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_OPIN>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DECLAR>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DEC_FRAMW>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_DEL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/RECO_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/RES_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_IMPL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_IMPL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_IMPL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DIR_DEL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/REG_DEL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ACT_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ACT_DEL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/ACT_IMPL_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DECLAR_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/DEC_FRAMW_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/JOINT_ACTION_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROT_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/COMMUNIC_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_EUMS_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_INTERINSTIT_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_INTERNATION_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AGREE_UBEREINKOM_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/BUDGET_DRAFT>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/BUDGET_DRAFT_PRELIM>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/BUDGET_DRAFT_PRELIM_SUPPL>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/BUDGET_DRAFT_SUPPL_AMEND>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AMEND_PROP>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AMEND_PROP_DIR>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AMEND_PROP_REG>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/AMEND_PROP_DEC>||
  ?type=<http://publications.europa.eu/resource/authority/resource-type/PROP_DEC_NO_ADDRESSEE>)"""
        if resource_type == "national_implementation":
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/MEAS_NATION_IMPL>)"""
        if resource_type == "manual" and manual_type and len(manual_type) > 1:
            query += """ FILTER(?type=<http://publications.europa.eu/resource/authority/resource-type/" + manual_type + ">)"""
        if include_corrigenda is False and resource_type != "caselaw":
            query += """ FILTER not exists{?work cdm:work_has_resource-type <http://publications.europa.eu/resource/authority/resource-type/CORRIGENDUM>}"""
        if include_celex:
            query += """OPTIONAL{?work cdm:resource_legal_id_celex ?celex.}"""
        if include_date:
            query += """OPTIONAL{?work cdm:work_date_document ?date.}"""
        if include_date_force:
            query += """OPTIONAL{?work cdm:resource_legal_date_entry-into-force ?dateforce.}"""
        if include_date_endvalid:
            query += """OPTIONAL{?work cdm:resource_legal_date_end-of-validity ?dateendvalid.}"""
        if include_date_transposed:
            query += (
                """OPTIONAL{?work cdm:directive_date_transposition ?datetranspos.}"""
            )
            # query += """OPTIONAL{?work cdm:resource_legal_date_transposition ?datetransposed.}"""
        if include_date_lodged:
            query += """OPTIONAL{?work cdm:resource_legal_date_request_opinion ?datelodged.}"""
        if include_lbs and resource_type != "caselaw":
            query += """ OPTIONAL{?work cdm:resource_legal_based_on_resource_legal ?lbs.
    ?lbs cdm:resource_legal_id_celex ?lbcelex.
    OPTIONAL{?bn owl:annotatedSource ?work.
    ?bn owl:annotatedProperty <http://publications.europa.eu/ontology/cdm#resource_legal_based_on_resource_legal>.
    ?bn owl:annotatedTarget ?lbs.
    ?bn annot:comment_on_legal_basis ?lbsuffix}}"""
        if include_force:
            query += """ OPTIONAL{?work cdm:resource_legal_in-force ?force.}"""
        if include_eurovoc:
            query += """ OPTIONAL{?work cdm:work_is_about_concept_eurovoc ?eurovoc. graph ?gs
    { ?eurovoc skos:prefLabel ?subjectLabel filter (lang(?subjectLabel)="en") }.}"""  # TODO - option to not filter by EN  here
        # Additionally/optionally - eurovocLabel. FILTER (LANGMATCHES(LANG(?eurovocLabel), "en")) .
        # FILTER(LANG(?datasetTitle)= "" || LANG(?datasetTitle) = "en").}
        if include_author:
            query += """ OPTIONAL{?work cdm:work_created_by_agent ?authorx.
                   ?authorx skos:prefLabel ?author. FILTER(lang(?author)='en')}."""  # TODO - option to not filter by EN/follow language setting
        if include_citations:
            query += """ OPTIONAL{?work cdm:work_cites_work ?citation.
                ?citation cdm:resource_legal_id_celex ?citationcelex.}"""
        if include_court_procedure:
            query += """ OPTIONAL{?work cdm:case-law_has_type_procedure_concept_type_procedure ?proc.
        ?proc skos:prefLabel ?courtprocedure. FILTER(lang(?courtprocedure)='en')}."""  # TODO - Option not to filter on EN or on other language
        if include_advocate_general:
            query += """ OPTIONAL{?work cdm:case-law_delivered_by_advocate-general ?agx.
                ?agx cdm:agent_name ?ag.}"""
        if include_judge_rapporteur:
            query += """ OPTIONAL{?work cdm:case-law_delivered_by_judge ?jrx.
                ?jrx cdm:agent_name ?jr.}"""
        if include_court_formation:
            query += """ OPTIONAL{?work cdm:case-law_delivered_by_court-formation ?cfx.
                ?cfx skos:prefLabel ?cf. FILTER(lang(?cf)='en')}."""  # TODO - Option not to filter on EN or on other language
        if include_court_scholarship:
            query += """ OPTIONAL{?work cdm:case-law_article_journal_related ?scholarship.}"""
        if include_proposal:
            query += """ OPTIONAL{?work cdm:resource_legal_adopts_resource_legal ?adoptedx.
                ?adoptedx cdm:resource_legal_id_celex ?proposal.}"""
        if include_ecli:
            query += """ OPTIONAL{?work cdm:case-law_ecli ?ecli.}"""
        if include_directory:
            query += """ OPTIONAL{?work cdm:resource_legal_is_about_concept_directory-code ?directory.}"""
        if include_sector:
            query += """ OPTIONAL{?work cdm:resource_legal_id_sector ?sector.}"""
        # add filter to only include latest version (inspired by eurlex R package)
        query += """ FILTER not exists{?work cdm:do_not_index "true"^^<http://www.w3.org/2001/XMLSchema#boolean>}."""
        if order:
            query += """} order by ?date"""
            # TODO - add option to order by different fields
        else:
            # This adds the closing curly braces to the query
            query += """}"""
        if limit and limit is not None and isinstance(limit, int):
            query += " limit " + str(limit)
        # somehow this was added in R: FILTER not exists{?work cdm:do_not_index \"true\"^^<http://www.w3.org/2001/XMLSchema#boolean>}. }
        if __name__ == "__main__":
            spinner.stop()
        # TODO add formatting option from server format=application%2Fsparql-results%2Bjson (from https://publications.europa.eu/webapi/rdf/sparql)
        # some postprocessing to get rid of newlines
        return query.replace("\n", "")  # .replace("\t", " ")

    """Query the Cellar endpoint with a specific SPARQL query and return a pandas dataframe"""

    def query_eurlex(
        self, query, endpoint="http://publications.europa.eu/webapi/rdf/sparql"
    ):
        """
        Query eurlex for documents with a SPARQL query
        Parameters:
        -----------
        query: str
            SPARQL query compatible with the EU Cellar endpoint
        endpoint: str
            The endpoint to query. Default is the EU Cellar endpoint
            Default: http://publications.europa.eu/webapi/rdf/sparql
        Returns:
        --------
            df: pandas.DataFrame of the results
        Examples:
        ---------
        >>> from eurlex import Eurlex
        >>> eur = Eurlex()
        >>> eur.query_eurlex("PREFIX dcat: <http://www.w3.org/ns/dcat#> PREFIX odp:  <http://data.europa.eu/euodp/ontologies/ec-odp#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT * WHERE { ?d a dcat:Dataset } LIMIT 10")
        """
        if __name__ == "__main__":
            spinner = Halo(text="Querying EU SPARQL endpoint ...", spinner="line")
            spinner.start()
        # TODO rename columns - also check for date with regex such as [0-9]{4}\-[0-9]+?\-[0-9]+$
        data_frame = pd.DataFrame()
        # sparql.setReturnFormat(JSON)
        # convert?
        try:
            data_frame = sparql_dataframe.get(endpoint, query)
        except Exception as e:
            print("There was an error when performing the query: ", e)
        if __name__ == "__main__":
            spinner.stop()
        return data_frame

    notice_type: Literal = ["tree", "branch", "object"]

    "Downloads an XML notice of a given type, based on a Cellar resource"
    # TODO consolidate the repetitive parts of get_data and download_xml
    def download_xml(
        self,
        url: str,
        notice: notice_type,
        filename: str = None,
        languages: list = ["en", "fr", "de"],
        mode: str = "wb",
    ):
        """Downloads the XML notice for a given notice type, when supplied with a URL or CELEX number.
        Parameters
        ----------
        url: str
            The URL or CELEX number of the notice to download
        notice: str
            The type of notice to download. Can be one of "tree", "branch", "object"
        Default: "object"
        filename: str
            The filename to save the XML notice to. If not supplied, the filename will be the CELEX number
        Default: None
        languages: list
            A list of languages to download the notice in. If the notice is not available in the language, it will be skipped.
        Default: ["en", "fr", "de"]
        mode: str
            The mode to open the file in.
        Default: "wb"

        Returns
        -------
        None

        Examples
        --------
        >>> from eurlex import Eurlex
        >>> eur = Eurlex()
        >>> eur.download_xml("http://publications.europa.eu/resource/celex/32016R0679", notice="object", filename="test.xml")
        >>> eur.download_xml("32016R0679", notice="object", filename="test.xml")
        >>> eur.download_xml("32014R0001", notice="tree")
        >>> eur.download_xml("32014R0001", notice="branch")
        """
        assert url, "URL has to be specified"
        filename = os.path.basename(url)
        assert notice, "Notice type has to be specified"
        assert (
            notice in self.notice_type
        ), "Notice type must be set as one of {}".format(self.notice_type)
        language_header = ""
        for lang in range(0, len(languages)):
            if lang == 0:
                language_header += languages[0] + ", "
            elif lang == 1:
                language_header += languages[1] + ";q=0.8, "
            elif lang == 2:
                language_header += languages[2] + ";q=0.7"
            else:
                print("Only three languages at a time are supported")
        print("The language header is: {}".format(language_header))
        if (url[:4] == "http" and re.fullmatch(".*cellar.*", url)) or (
            url[:4] == "http" and re.fullmatch(".*celex.*", url)
        ):
            print(
                "Assuming URL to be a valid, http based EU Cellar resource: {}".format(
                    url
                )
            )
        else:
            # Additional testing?
            # if (stringr::str_detect(url,"celex.*[\\(|\\)|\\/]")){
            # assume it is a CELEX number
            url = "http://publications.europa.eu/resource/celex/" + url
            print("The CELEX url is: {}".format(url))
        accept_header = "application/xml; notice=" + notice
        if notice == "object":
            head = requests.head(
                # redirects to cellar url so redirects are necessary
                url,
                headers={"Accept": accept_header},
                allow_redirects=True,
            )
        else:
            head = requests.head(
                url,
                headers={"Accept-Language": language_header, "Accept": accept_header},
                allow_redirects=True,
            )
        assert head.status_code == 200, "The http request was unsuccessful {}".format(
            head.status_code
        )
        file_content = requests.get(head.url).content
        with open(filename, mode) as writer:
            writer.write(file_content)
        return str(
            file_content
        )  # TODO alternatively, offer to return instead of saving to file (or make separate function)

    data_types: Literal = ["title", "text", "ids", "notice"]

    "Download data/documents from EU Cellar based on a given resource URL"

    def get_data(
        self,
        url,
        data_type: data_types,
        notice: notice_type = None,
        languages: list = ["en", "fr", "de"],
        include_breaks: bool = False,
        extract_caselaw_metadata: bool = False,
    ):
        """This function takes a URL or Celex number and returns data, such as the title, text, the id, or notices.
        Parameters
        ----------
        url
            The URL or CELEX number to download/access
        data_type
            The data type to download. Valid options are title, text, ids or notice. This parameter is required.
        notice
            The type of notice to download.
        languages
            A list of the prefered languages, from most preferred to least preferred. Currently, the code does not check whether the languages are named correctly or exist.
            Default: ["en", "fr", "de"]
        include_breaks
            Whether or not to insert page breaks into text.
            Default: False
        extract_caselaw_metadata
            For the title, tries to break it down into case name, parties and case number.
            Default: False
        Returns
        -------
            out: The relevant response as str
        Examples
        --------
        >>> from eurlex import Eurlex
        >>> eur = Eurlex()
        >>> eur.get_data("http://publications.europa.eu/resource/celex/32016R0679", data_type = "text")
        >>> eur.get_data("32016R0679")
        >>> eur.get_data("32014R0001")
        """

        assert url, "The URL or CELEX number is necessary to retrieve data"
        assert (
            data_type
        ), "The type of the data to be parsed is necessary"  # TODO - maybe just parse all in one go?
        assert (
            data_type in self.data_types
        ), "The type of data to be parsed has to be one of title, text, ids or notice"
        if data_type == "notice":
            assert (
                notice is not None and notice in self.notice_type
            ), "The type of notice to be processed has to be provided"
        if data_type != "title":
            assert (
                extract_caselaw_metadata is False
            ), "Case law metadata can only be extracted from titles (of caselaw)"
        # TODO
        # Ok, it is a bit weird to filter language not in CELLAR but in http header
        language_header = ""
        for lang in range(0, len(languages)):
            if lang == 0:
                language_header += languages[0] + ", "
            elif lang == 1:
                language_header += languages[1] + ";q=0.8, "
            elif lang == 2:
                language_header += languages[2] + ";q=0.7"
            else:
                print("Only three languages at a time are supported")

        if url[:4] == "http" and re.fullmatch(".*cellar.*", url):
            if __name__ == "__main__":
                print("Assuming URL to be a valid, http based EU Cellar resource")
        else:
            if not url[:4] == "http":
                # TODO - Add additional testing?
                # if (stringr::str_detect(url,"celex.*[\\(|\\)|\\/]")){
                # assume it is a CELEX number
                url = "http://publications.europa.eu/resource/celex/" + url
                if __name__ == "__main__":
                    print("The CELEX url is: {}".format(url))

        if data_type == "title":
            out = ""
            try:
                if __name__ == "__main__":
                    print("Getting title data...")
                response = requests.get(
                    url,
                    headers={
                        "Accept-Language": language_header,
                        "Accept": "application/xml; notice=object",
                    },
                )
            except Exception as e:
                print("There was an error during data retrieval: {}", e)
            if response.status_code == 200:
                html = BeautifulSoup(response.text, "xml")
                out = str(html.find("EXPRESSION_TITLE").get_text())
                if extract_caselaw_metadata and "#" in out:
                    title = out.split("#")[0].strip()
                    parties = out.split("#")[1].strip().strip(".")
                    case_number = out.split("#")[2].strip().strip(".")

                    out = {
                        "title": title,
                        "parties": parties,
                        "case_number": case_number,
                    }
                if __name__ == "__main__":
                    print(out)
            else:
                if __name__ == "__main__":
                    print("No content retrieved: {}", response.status_code)
                out += str(response.status_code)

        elif data_type == "text":
            out = ""
            try:
                if __name__ == "__main__":
                    print("Getting text data...")
                response = requests.get(
                    url,
                    headers={
                        "Accept-Language": language_header,
                        "Content-Language": language_header,
                        "Accept": "text/html, text/html;type=simplified, text/plain, application/xhtml+xml, application/xhtml+xml;type=simplified, application/pdf, application/pdf;type=pdf1x, application/pdf;type=pdfa1a, application/pdf;type=pdfx, application/pdf;type=pdfa1b, application/msword",
                    },
                )
            except Exception as e:
                print("There was an error during gathering data: {}", e)

            if response.status_code == 200:
                if __name__ == "__main__":
                    print("Got a {} reponse, great!".format(response.status_code))
                out = self.read_data(response)

            elif response.status_code == 300:
                html = BeautifulSoup(response.content, "html.parser")
                links_html = html.find_all("a", href=True)
                links = []
                for link in links_html:
                    links.append(link["href"])
                print("Found multiple links: {}", links)
                multiout = ""
                for link in links:
                    multiresponse = requests.get(
                        url,
                        headers={
                            "Accept-Language": language_header,
                            "Content-Language": language_header,
                            "Accept": "text/html, text/html;type=simplified, text/plain, application/xhtml+xml, application/xhtml+xml;type=simplified, application/pdf, application/pdf;type=pdf1x, application/pdf;type=pdfa1a, application/pdf;type=pdfx, application/pdf;type=pdfa1b, application/msword",
                        },
                    )
                    if multiresponse.status_code == 200:
                        print(str(multiresponse.status_code))
                        print(multiresponse.text)
                        multiout += (
                            self.read_data(multiresponse) + "---documentbreak---"
                        )
                    else:
                        multiout += "NaN"
                print(multiout)
                out = multiout
            elif response.status_code == 406:
                out += "NaN" + str(
                    response.status_code
                )  # TODO ok this is a pretty ... thing to do
                if __name__ == "__main__":
                    print("missingdoc")
            else:
                if __name__ == "__main__":
                    print("No content retrieved {}", response)
            if not include_breaks:
                out = out.replace("---documentbreak---", "").replace(
                    "---pagebreak---", ""
                )

        elif data_type == "ids":
            out = ""
            response = requests.get(
                url,
                headers={
                    "Accept-Language": language_header,
                    "Accept": "application/xml; notice=identifiers",
                },
            )
            if response.status_code == 200:
                xml = BeautifulSoup(response.content, "xml")
                out = xml.find_all("VALUE")
                temp = []
                for v in out:
                    temp.append(v.get_text())
                out = temp
                if __name__ == "__main__":
                    print(out)
            else:
                out += str(response.status_code)
        elif data_type == "notice":
            out = ""
            accept_header = "application/xml; notice=" + notice
            if (
                notice == "object"
            ):  # if notice is of type object, there is no language header
                response = requests.get(url, headers={"Accept": accept_header})
            else:
                response = requests.get(
                    url,
                    headers={
                        "Accept-Language": language_header,
                        "Accept": accept_header,
                    },
                )
            if response.status_code == 200:
                if __name__ == "__main__":
                    print("Retrived notice successfully.")
                    print(response.text)
                out += response.text
            else:
                out = str(response.status_code)
                if __name__ == "__main__":
                    print(f"Something might have gone wrong: {response.status_code}")
        else:
            return "You should not be here."
        if out:
            return out
        else:
            return 1

    # Reads response data and processes it to get the text, based on the content type
    def read_data(self, response):
        """This function takes a response object, and returns text as a string. This text is parsed from a html, or a pdf. MS Word is not supported for now.
        (the doc test currently only tests this function indirectly, as it is called from get_data(), but for testing it separately in doctest quite some things would have to be changed)
        Parameters
        ----------
            response: A repsonse object that was returned from a previous request for data of type text from the EU Cellar repository
        Returns
        -------
            ret:
        Examples
        --------
        >>> from eurlex import Eurlex
        >>> eur = Eurlex()
        >>> eur.get_data("32016R0679", type="text")
        """
        # check content type to be html?
        content_type = response.headers.get("Content-Type")
        if "text/html" in content_type:
            html = BeautifulSoup(response.content, "html.parser")
            ret = html.find("body").get_text()
            return ret + "---pagebreak---"
        elif "application/pdf" in content_type:
            text = extract_text(response.content)
            return text + "---pagebreak---"
        elif "application/msword" in content_type:
            # would probably use python-docx to implement this
            ret = "The Word format is not suppported at present"
            print(ret)
            return ret
        # len('Error: unsupported content type: application/xhtml+xml;charset=UTF-8')
        else:
            ret = f"Error: unsupported content type: {content_type}"
            print(ret)
            return ret


# The main function. It uses the fire framework to expose the functions of the module on the command line
def main(argv=None):
    print("This is a CLI interface for pyeurlex")
    Fire(Eurlex)


if __name__ == "__main__":
    main()
