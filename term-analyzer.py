import spacy, requests
from SPARQLWrapper import SPARQLWrapper, JSON
from bs4 import BeautifulSoup
from tabulate import tabulate
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
                 'rdfURL': ""})


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


# Example scenario text is taken from "Scientific American: Feature Article: The Semantic Web: May 2001
# by TIM BERNERS-LEE, JAMES HENDLER and ORA LASSILA"
text = ("""
The entertainment system was belting out the Beatles' "We Can Work It Out" when the phone rang. When Pete
answered, his phone turned the sound down by sending a message to all the other local devices that had a volume control.
His sister, Lucy, was on the line from the doctor's office: "Mom needs to see a specialist and then has to have a series
of physical therapy sessions. Biweekly or something. I'm going to have my agent set up the appointments." Pete
immediately agreed to share the chauffeuring. At the doctor's office, Lucy instructed her Semantic Web agent through her
handheld Web browser. The agent promptly retrieved information about Mom's prescribed treatment from the doctor's agent,
looked up several lists of providers, and checked for the ones in-plan for Mom's insurance within a 20-mile radius of
her home and with a rating of excellent or very good on trusted rating services. It then began trying to find a match
between available appointment times (supplied by the agents of individual providers through their Web sites) and Pete's
and Lucy's busy schedules. (The emphasized keywords indicate terms whose semantics, or meaning, were defined for the
agent through the Semantic Web.)
In a few minutes the agent presented them with a plan. Pete didn't like it—University Hospital was all the way across
town from Mom's place, and he'd be driving back in the middle of rush hour. He set his own agent to redo the search
with stricter preferences about location and time. Lucy's agent, having complete trust in Pete's agent in the context of
the present task, automatically assisted by supplying access certificates and shortcuts to the data it had already
sorted through.
Almost instantly the new plan was presented: a much closer clinic and earlier times—but there were two
warning notes. First, Pete would have to reschedule a couple of his less important appointments. He checked what they
were—not a problem. The other was something about the insurance company's list failing to include this provider under
physical therapists: "Service type and insurance plan status securely verified by other means," the agent reassured him.
"(Details?)"
Lucy registered her assent at about the same moment Pete was muttering, "Spare me the details," and it was all set.
(Of course, Pete couldn't resist the details and later that night had his agent explain how it had found that provider
even though it wasn't on the proper list.)
""")

doc = nlp(text)

termList = []

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


# find entity of type of terms
print("Finding entity of type & RDF/XML URL of terms...")
for dict_item in termList:
    try:
        dict_item['entityOfType'] = get_entity_of_type(dict_item['term'])
        dict_item['dbpediaURL'] = get_dbpedia_url_of_term(dict_item['term'])
        dict_item['rdfURL'] = get_rdf_xml_url_of_term(dict_item['term'])
    except requests.exceptions.HTTPError:
        print("Term = ", dict_item['term'], " does not have an entity of type!")
print("Finding entity of type of terms...DONE")


# print all stored data
print("Printing all the stored data...\n")
header = termList[0].keys()
rows = [x.values() for x in termList]
print(tabulate(rows, header))
print("\nPrinting all the stored data...DONE\n")


print("Importing RDF data to Neo4j Graph Database...")
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123456"))


def add_rdf(tx, uri):
    tx.run("""CALL semantics.importRDF("%s","RDF/XML")""" % uri)


with driver.session() as session:
    for dict_item in termList:
        if dict_item['rdfURL'] != "":
            session.write_transaction(add_rdf, dict_item['rdfURL'])

driver.close()
print("Importing RDF data to Neo4j Graph Database...DONE")
