import spacy, requests
from SPARQLWrapper import SPARQLWrapper, JSON
from bs4 import BeautifulSoup
from tabulate import tabulate
import pickle
from neo4j import GraphDatabase

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

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


############################################################################
########                       Reading Text                         ########
############################################################################

# Example scenario text is taken from "Scientific American: Feature Article: The Semantic Web: May 2001
# by TIM BERNERS-LEE, JAMES HENDLER and ORA LASSILA"
f = open("input-text.txt", "r")
text = f.read()

termList = []
# flag to load list from the stored file or not
loadListFromFile = True

if loadListFromFile:
    # loading list from the stored file
    with open("list-store.txt", 'rb') as f:
        termList = pickle.load(f)

else:

    ############################################################################
    ########                       Parsing Terms                        ########
    ############################################################################

    doc = nlp(text)

    # parse terms
    print("Parsing terms...")
    # entities
    for entity in doc.ents:
        if entity.root.pos_ != "NUM" and entity.root.pos_ != "ADV" and entity.root.pos_ != "NOUN":
            myTerm = entity.text.replace("\n", " ").title()
            isMatched = False

            for index, dict_item in enumerate(termList):
                if myTerm == dict_item['term']:
                    termList[index]['count'] += 1
                    isMatched = True

            if not isMatched:
                termList.append(create_dict(entity.text.replace("\n", " "), myTerm, entity.root.pos_, entity.root.i, 1))

    # noun chunks
    for noun in doc.noun_chunks:

        if noun.root.pos_ != "PRON":
            myTerm = noun.root.lemma_.title()
            isMatched = False

            for index, dict_item in enumerate(termList):
                if myTerm == dict_item['term']:
                    termList[index]['count'] += 1
                    isMatched = True

            if not isMatched:
                termList.append(create_dict(noun.text.replace("\n", " "), myTerm, noun.root.pos_, noun.root.i, 1))
    print("Parsing terms...DONE")

    ############################################################################
    ########                     Creating List                          ########
    ############################################################################

    # find entity of type of terms
    print("Finding entity of type & RDF/XML URL of terms...")
    for dict_item in termList:
        try:
            dict_item['entityOfType'] = get_entity_of_type(dict_item['term'])
            dict_item['dbpediaURL'] = get_dbpedia_url_of_term(dict_item['term'])
            dict_item['rdfURL'] = get_rdf_xml_url_of_term(dict_item['term'])
            dict_item['rdfTypesURL'] = find_dbo_types_of_term(dict_item['term'])
            dict_item['rdfTypes'] = parse_dbo_types_from_url(dict_item['rdfTypesURL'])
        except requests.exceptions.HTTPError:
            print("Term = ", dict_item['term'], " does not have an entity of type!")

    print("Finding entity of type of terms...DONE")

    # storing list to a file
    with open("list-store.txt", 'wb') as f:
        pickle.dump(termList, f)

# print all stored data
print("Printing all the stored data...\n")
header = termList[0].keys()
rows = [x.values() for x in termList]
print(tabulate(rows, header))
print("\nPrinting all the stored data...DONE\n")

############################################################################
########                          Neo4j                             ########
############################################################################

print("Importing RDF data to Neo4j Graph Database...")
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123456"))
session = driver.session()


def check_node(name, url):
    query = """
        MATCH (a:Node {name: '%s', url: '%s'})
        RETURN (COUNT(a))
        """ % (name, url)
    results = session.run(query)

    for result in results:
        count = result[0]

    if count == 0:
        # node does not exist
        return True
    else:
        # node exists
        return False


def create_node(name, url):
    if check_node(name, url):
        query = """
                MERGE (a:Node {name: '%s', url: '%s'})
                """ % (name, url)
        results = session.run(query)
        return True
    else:
        print("Node is already existent")
        return False


def create_relationship(fromName, fromUrl, toName, toUrl):
    query = """
            MATCH (a:Node), (b:Node)
            WHERE a.name='%s' AND a.url='%s' AND b.name='%s' AND b.url='%s'
            MERGE  (a)-[:TYPE_OF]->(b)
            """ % (fromName, fromUrl, toName, toUrl)
    results = session.run(query)


for term in termList:
    # if rdf type list is not empty
    if term['rdfTypes']:
        fromName = term['term']
        fromUrl = term['rdfURL']
        # create term node if not existent and continue
        if create_node(fromName, fromUrl):
            for rdfType in term['rdfTypesURL']:
                toName = parse_one_dbo_type_from_url(rdfType)
                toUrl = rdfType
                # create entity type node if not existent
                create_node(toName, toUrl)
                # create relationship between term and type
                create_relationship(fromName, fromUrl, toName, toUrl)


driver.close()
print("Importing RDF data to Neo4j Graph Database...DONE")


############################################################################
########                    Neo4j with NeoSemantic                  ########
############################################################################

# print("Importing RDF data to Neo4j Graph Database with NeoSemantics...")
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123456"))
#
#
# def add_rdf(tx, uri):
#     tx.run("""CALL semantics.importRDF("%s","RDF/XML")""" % uri)
#
#
# with driver.session() as session:
#     for dict_item in termList:
#         if dict_item['rdfURL'] != "":
#             session.write_transaction(add_rdf, dict_item['rdfURL'])
#
# driver.close()
# print("Importing RDF data to Neo4j Graph Database with NeoSemantics...DONE")
