# term-analyzer
* Parse the terms from the given text
* Find the entity of type of terms from DBPedia
* Store incoming data and their statistics
* Import data to Neo4j graph database

## Installation
#### spaCy
spaCy is a library for advanced Natural Language Processing in Python and Cython.
```
$ pip install spacy
$ python -m spacy download en_core_web_sm
```

#### SPARQLWrapper
This is a wrapper around a SPARQL service. It helps in creating the query URI and, possibly, convert the result into a more manageable format.
```
$ pip install sparqlwrapper
```

#### BeautifulSoup
Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
```
$ pip install beautifulsoup4
```

#### Tabulate
Pretty-print tabular data in Python, a library and a command-line utility.
```
$ pip install tabulate
```

#### Neo4j Python Driver
The Neo4j Python driver is officially supported by Neo4j and connects to the database using the binary protocol. It aims to be minimal, while being idiomatic to Python.
```
$ pip install neo4j
```

#### Neo4j Server
Since Neo Semantics does not fully support Neo4j 4.x, Neo4j 3.5.17 is used.
Also used plugins:
  - APOC 3.5.0.11
  - Neo Semantics 3.5.0.4
  - Neo4j GraphQL 3.5.15.5


## Example Output
**term:** Root of the text which is parsed with spaCy.  
**dbpediaURL:** DBPedia URL of the term (if exists).  
**rdfURL:** RDF/XML URL of the term (if exists).  
**index:** The index of the term within the given document.  
**count:** The count of the term within the given document.  
**text:** The text which is parsed with spaCy.  
**entityOfType:** An entity of type of term in DBPedia.  
**type:** Type of the parsed text.
```
term                 type    entityOfType             text                                      count  dbpediaURL                                       rdfURL                                            index
-------------------  ------  -----------------------  --------------------------------------  -------  -----------------------------------------------  ----------------------------------------------  -------
Beatles              PROPN   organisation             Beatles                                       2  http://dbpedia.org/resource/Beatles              http://dbpedia.org/data/The_Beatles.rdf               8
We Can Work It Out   VERB    musical work             We Can Work It Out                            1  http://dbpedia.org/resource/We_Can_Work_It_Out   http://dbpedia.org/data/We_Can_Work_It_Out.rdf       13
Pete                 PROPN   Thing                    Pete                                         15  http://dbpedia.org/resource/Pete                 http://dbpedia.org/data/Pete.rdf                     23
Lucy                 PROPN   name                     Lucy                                          8  http://dbpedia.org/resource/Lucy                 http://dbpedia.org/data/Lucy.rdf                     53
Mom                  PROPN   Thing                    Mom                                           4  http://dbpedia.org/resource/Mom                  http://dbpedia.org/data/Mother.rdf                  136
University Hospital  PROPN   hospital                 University Hospital                           1  http://dbpedia.org/resource/University_Hospital  http://dbpedia.org/data/Teaching_hospital.rdf       268
System               NOUN    Thing                    The entertainment system                      1  http://dbpedia.org/resource/System               http://dbpedia.org/data/System.rdf                    3
Phone                NOUN    device                   his phone                                     1  http://dbpedia.org/resource/Phone                http://dbpedia.org/data/Telephone.rdf                28
Sound                NOUN    Thing                    the sound                                     1  http://dbpedia.org/resource/Sound                http://dbpedia.org/data/Sound.rdf                    31
Message              NOUN    organisation             a message                                     1  http://dbpedia.org/resource/Message              http://dbpedia.org/data/Message.rdf                  36
Device               NOUN    MusicalPerformer         all the other local devices                   1  http://dbpedia.org/resource/Device               http://dbpedia.org/data/Device.rdf                   42
Control              NOUN    Thing                    a volume control                              1  http://dbpedia.org/resource/Control              http://dbpedia.org/data/Control.rdf                  47
Sister               NOUN    mammal                   His sister                                    1  http://dbpedia.org/resource/Sister               http://dbpedia.org/data/Sister.rdf                   51
Line                 NOUN    Thing                    the line                                      1  http://dbpedia.org/resource/Line                 http://dbpedia.org/data/Line.rdf                     58
Office               NOUN    Thing                    the doctor's office                           2  http://dbpedia.org/resource/Office               http://dbpedia.org/data/Office.rdf                   63
Specialist           NOUN    Thing                    a specialist                                  1  http://dbpedia.org/resource/Specialist           http://dbpedia.org/data/Specialist.rdf               71
Series               NOUN    Thing                    a series                                      1  http://dbpedia.org/resource/Series               http://dbpedia.org/data/Series.rdf                   78
Session              NOUN    Thing                    physical therapy sessions                     1  http://dbpedia.org/resource/Session              http://dbpedia.org/data/Session.rdf                  83
Agent                NOUN    Creation103129123        my agent                                     12  http://dbpedia.org/resource/Agent                http://dbpedia.org/data/Agent.rdf                    95
Appointment          NOUN    Thing                    the appointments                              2  http://dbpedia.org/resource/Appointment          http://dbpedia.org/data/Appointment.rdf              99
Chauffeuring         NOUN                             the chauffeuring                              1                                                                                                       109
Browser              NOUN    Thing                    her handheld Web browser                      1  http://dbpedia.org/resource/Browser              http://dbpedia.org/data/Browser.rdf                 128
Information          NOUN    Thing                    information                                   1  http://dbpedia.org/resource/Information          http://dbpedia.org/data/Information.rdf             134
Treatment            NOUN    Thing                    Mom's prescribed treatment                    1  http://dbpedia.org/resource/Treatment            http://dbpedia.org/data/Treatment.rdf               139
List                 NOUN    Thing                    several lists                                 3  http://dbpedia.org/resource/List                 http://dbpedia.org/data/List.rdf                    150
Provider             NOUN    Thing                    providers                                     4  http://dbpedia.org/resource/Provider             http://dbpedia.org/data/Provider.rdf                152
One                  NOUN    Integer113728499         the ones                                      1  http://dbpedia.org/resource/One                  http://dbpedia.org/data/1_(number).rdf              158
Plan                 NOUN    Thing                    -plan                                         3  http://dbpedia.org/resource/Plan                 http://dbpedia.org/data/Plan.rdf                    161
Insurance            NOUN    software                 Mom's insurance                               1  http://dbpedia.org/resource/Insurance            http://dbpedia.org/data/Insurance.rdf               165
Radius               NOUN    Thing                    a 20-mile radius                              1  http://dbpedia.org/resource/Radius               http://dbpedia.org/data/Radius.rdf                  169
Home                 NOUN    Thing                    her home                                      1  http://dbpedia.org/resource/Home                 http://dbpedia.org/data/Home.rdf                    173
Rating               NOUN    Thing                    a rating                                      1  http://dbpedia.org/resource/Rating               http://dbpedia.org/data/Rating.rdf                  177
Service              NOUN    Thing                    trusted rating services                       1  http://dbpedia.org/resource/Service              http://dbpedia.org/data/Service.rdf                 186
Match                NOUN    software                 a match                                       1  http://dbpedia.org/resource/Match                http://dbpedia.org/data/Match.rdf                   195
Time                 NOUN    Thing                    available appointment times                   3  http://dbpedia.org/resource/Time                 http://dbpedia.org/data/Time.rdf                    200
Site                 NOUN    Thing                    their Web sites                               1  http://dbpedia.org/resource/Site                 http://dbpedia.org/data/Site.rdf                    212
Schedule             NOUN    Thing                    Lucy's busy schedules                         1  http://dbpedia.org/resource/Schedule             http://dbpedia.org/data/Schedule.rdf                222
Keyword              NOUN    Thing                    The emphasized keywords                       1  http://dbpedia.org/resource/Keyword              http://dbpedia.org/data/Keyword.rdf                 227
Term                 NOUN    Thing                    terms                                         1  http://dbpedia.org/resource/Term                 http://dbpedia.org/data/Term.rdf                    229
Semantic             NOUN    book                     whose semantics                               1  http://dbpedia.org/resource/Semantic             http://dbpedia.org/data/Semantics.rdf               231
Meaning              NOUN    Thing                    meaning                                       1  http://dbpedia.org/resource/Meaning              http://dbpedia.org/data/Meaning.rdf                 234
Web                  PROPN   Thing                    the Semantic Web                              1  http://dbpedia.org/resource/Web                  http://dbpedia.org/data/Web.rdf                     245
Minute               NOUN    organisation             a few minutes                                 1  http://dbpedia.org/resource/Minute               http://dbpedia.org/data/Minute.rdf                  252
Hospital             PROPN   university               University Hospital                           1  http://dbpedia.org/resource/Hospital             http://dbpedia.org/data/Hospital.rdf                268
Town                 NOUN    settlement               town                                          1  http://dbpedia.org/resource/Town                 http://dbpedia.org/data/Town.rdf                    275
Place                NOUN    Thing                    Mom's place                                   1  http://dbpedia.org/resource/Place                http://dbpedia.org/data/Place.rdf                   279
Middle               NOUN    Thing                    the middle                                    1  http://dbpedia.org/resource/Middle               http://dbpedia.org/data/Middle.rdf                  289
Hour                 NOUN    organisation             rush hour                                     1  http://dbpedia.org/resource/Hour                 http://dbpedia.org/data/Hour.rdf                    292
Search               NOUN    Thing                    the search                                    1  http://dbpedia.org/resource/Search               http://dbpedia.org/data/Searching.rdf               302
Preference           NOUN    Thing                    stricter preferences                          1  http://dbpedia.org/resource/Preference           http://dbpedia.org/data/Preference.rdf              306
Location             NOUN    Thing                    location                                      1  http://dbpedia.org/resource/Location             http://dbpedia.org/data/Location.rdf                308
Trust                NOUN    Thing                    complete trust                                1  http://dbpedia.org/resource/Trust                http://dbpedia.org/data/Trust.rdf                   318
Context              NOUN    Thing                    the context                                   1  http://dbpedia.org/resource/Context              http://dbpedia.org/data/Context.rdf                 325
Task                 NOUN    Thing                    the present task                              1  http://dbpedia.org/resource/Task                 http://dbpedia.org/data/Task.rdf                    330
Certificate          NOUN    Thing                    access certificates                           1  http://dbpedia.org/resource/Certificate          http://dbpedia.org/data/Certificate.rdf             337
Datum                NOUN    Thing                    the data                                      1  http://dbpedia.org/resource/Datum                http://dbpedia.org/data/Datum.rdf                   342
Clinic               NOUN    architectural structure  a much closer clinic                          1  http://dbpedia.org/resource/Clinic               http://dbpedia.org/data/Clinic.rdf                  362
Note                 NOUN    Thing                    two warning notes                             1  http://dbpedia.org/resource/Note                 http://dbpedia.org/data/Note.rdf                    373
Couple               NOUN    Thing                    a couple                                      1  http://dbpedia.org/resource/Couple               http://dbpedia.org/data/Couple.rdf                  383
Problem              NOUN    Thing                    a problem                                     1  http://dbpedia.org/resource/Problem              http://dbpedia.org/data/Problem.rdf                 399
Therapist            NOUN    Thing                    physical therapists                           1  http://dbpedia.org/resource/Therapist            http://dbpedia.org/data/Therapy.rdf                 419
Status               NOUN    Thing                    Service type and insurance plan status        1  http://dbpedia.org/resource/Status               http://dbpedia.org/data/Status.rdf                  427
Mean                 NOUN    Thing                    other means                                   1  http://dbpedia.org/resource/Mean                 http://dbpedia.org/data/Mean.rdf                    432
Details              PROPN   Thing                    "(Details                                     1  http://dbpedia.org/resource/Details              http://dbpedia.org/data/Detail.rdf                  443
Assent               NOUN    Thing                    her assent                                    1  http://dbpedia.org/resource/Assent               http://dbpedia.org/data/Assent.rdf                  451
Moment               NOUN    MusicalComposition       about the same moment                         1  http://dbpedia.org/resource/Moment               http://dbpedia.org/data/Moment.rdf                  456
Detail               NOUN    Thing                    the details                                   2  http://dbpedia.org/resource/Detail               http://dbpedia.org/data/Detail.rdf                  465
```
## Visualization of Neo4j Graph Database

![Image of Neo4j Graph Database](https://github.com/akngmskvk/term-analyzer/blob/master/images/neo4j-graph-1.png)
