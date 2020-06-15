import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from bs4 import BeautifulSoup


sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def create_class_query(param):
    query = ("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbp: <http://dbpedia.org/property/>

        SELECT ?label
        WHERE {
            dbr:%s a ?label
        }
    """ % param.title())

    return query


def start_query(myTerm):
    query = create_class_query(myTerm)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    return result


def create_dict(text, rootText, type, index, count):
    return dict({'text': text,
                 'term': rootText,
                 'type': type,
                 'index': index,
                 'count': count,
                 'dbpediaURL': "",
                 'entityOfType': "",
                 'rdfURL': "",
                 'rdfTypes': "",
                 'rdfTypesURL': ""})


def get_dbpedia_url_of_term(term):
    url = 'http://dbpedia.org/resource/' + term.replace(" ", "_")
    return url


def get_entity_of_type(term):
    resp = requests.get(get_dbpedia_url_of_term(term))
    resp.raise_for_status()
    soupSource = BeautifulSoup(resp.text, "html.parser")
    entityOfType = soupSource.find("div", attrs={"class": "page-resource-uri"}).select_one("a:nth-child(1)").text
    # print("Term = ", term, ", An entity of type = ", entityOfType)

    return entityOfType


def get_rdf_xml_url_of_term(term):
    resp = requests.get(get_dbpedia_url_of_term(term))
    resp.raise_for_status()
    soupSource = BeautifulSoup(resp.text, "html.parser")
    url = soupSource.find("link", attrs={"type": "application/rdf+xml"})['href']

    return url


def find_dbo_types_of_term(term):
    resp = requests.get(get_rdf_xml_url_of_term(term))
    resp.raise_for_status()
    soupSource = BeautifulSoup(resp.text, "html.parser")
    results = soupSource.find_all("rdf:type")
    rdfTypesURL = []
    for result in results:
        # if "http://dbpedia.org/ontology/" in str(result):
        #     print(result['rdf:resource'])
        #     print(str(result['rdf:resource']).split("/")[-1])
        # if "owl#Thing" in str(result):
        #     print(result['rdf:resource'])
        #     print(str(result['rdf:resource']).split("#")[-1])
        #     print(result['rdf:resource'])
        if "http://dbpedia.org/ontology/" in str(result) or "owl#Thing" in str(result):
            rdfTypesURL.append(result['rdf:resource'])

    return rdfTypesURL


def parse_dbo_types_from_url(urlList):
    rdfTypes = []
    for url in urlList:
        if "http://dbpedia.org/ontology/" in str(url):
            rdfTypes.append(str(url).split("/")[-1])

        elif "owl#Thing" in str(url):
            rdfTypes.append(str(url).split("#")[-1])

    return rdfTypes


def parse_one_dbo_type_from_url(url):
    if "http://dbpedia.org/ontology/" in str(url):
        return str(url).split("/")[-1]

    elif "owl#Thing" in str(url):
        return str(url).split("#")[-1]