# term-analyzer
* Parse the terms from the given text
* Find the entity of type of terms from DBPedia
* Store incoming data and their statistics

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

## Example Output
**term:** Root of the text which is parsed with spaCy.  
**dbpediaURL:** DBPedia URL of the term (if exists).  
**index:** The index of the term within the given document.  
**count:** The count of the term within the given document.  
**text:** The text which is parsed with spaCy.  
**entityOfType:** An entity of type of term in DBPedia.  
**type:** Type of the parsed text.
```
term                 dbpediaURL                                         index    count  text                                    entityOfType             type
-------------------  -----------------------------------------------  -------  -------  --------------------------------------  -----------------------  ------
Beatles              http://dbpedia.org/resource/Beatles                    8        2  Beatles                                 organisation             PROPN
We Can Work It Out   http://dbpedia.org/resource/We_Can_Work_It_Out        13        1  We Can Work It Out                      musical work             VERB
Pete                 http://dbpedia.org/resource/Pete                      23       15  Pete                                    Thing                    PROPN
Lucy                 http://dbpedia.org/resource/Lucy                      53        8  Lucy                                    name                     PROPN
Mom                  http://dbpedia.org/resource/Mom                      136        4  Mom                                     Thing                    PROPN
University Hospital  http://dbpedia.org/resource/University_Hospital      268        1  University Hospital                     hospital                 PROPN
System               http://dbpedia.org/resource/System                     3        1  The entertainment system                Thing                    NOUN
Phone                http://dbpedia.org/resource/Phone                     28        1  his phone                               device                   NOUN
Sound                http://dbpedia.org/resource/Sound                     31        1  the sound                               Thing                    NOUN
Message              http://dbpedia.org/resource/Message                   36        1  a message                               organisation             NOUN
Device               http://dbpedia.org/resource/Device                    42        1  all the other local devices             MusicalPerformer         NOUN
Control              http://dbpedia.org/resource/Control                   47        1  a volume control                        Thing                    NOUN
Sister               http://dbpedia.org/resource/Sister                    51        1  His sister                              mammal                   NOUN
Line                 http://dbpedia.org/resource/Line                      58        1  the line                                Thing                    NOUN
Office               http://dbpedia.org/resource/Office                    63        2  the doctor's office                     Thing                    NOUN
Specialist           http://dbpedia.org/resource/Specialist                71        1  a specialist                            Thing                    NOUN
Series               http://dbpedia.org/resource/Series                    78        1  a series                                Thing                    NOUN
Session              http://dbpedia.org/resource/Session                   83        1  physical therapy sessions               Thing                    NOUN
Agent                http://dbpedia.org/resource/Agent                     95       12  my agent                                Creation103129123        NOUN
Appointment          http://dbpedia.org/resource/Appointment               99        2  the appointments                        Thing                    NOUN
Chauffeuring                                                              109        1  the chauffeuring                                                 NOUN
Browser              http://dbpedia.org/resource/Browser                  128        1  her handheld Web browser                Thing                    NOUN
Information          http://dbpedia.org/resource/Information              134        1  information                             Thing                    NOUN
Treatment            http://dbpedia.org/resource/Treatment                139        1  Mom's prescribed treatment              Thing                    NOUN
List                 http://dbpedia.org/resource/List                     150        3  several lists                           Thing                    NOUN
Provider             http://dbpedia.org/resource/Provider                 152        4  providers                               Thing                    NOUN
One                  http://dbpedia.org/resource/One                      158        1  the ones                                Integer113728499         NOUN
Plan                 http://dbpedia.org/resource/Plan                     161        3  -plan                                   Thing                    NOUN
Insurance            http://dbpedia.org/resource/Insurance                165        1  Mom's insurance                         software                 NOUN
Radius               http://dbpedia.org/resource/Radius                   169        1  a 20-mile radius                        Thing                    NOUN
Home                 http://dbpedia.org/resource/Home                     173        1  her home                                Thing                    NOUN
Rating               http://dbpedia.org/resource/Rating                   177        1  a rating                                Thing                    NOUN
Service              http://dbpedia.org/resource/Service                  186        1  trusted rating services                 Thing                    NOUN
Match                http://dbpedia.org/resource/Match                    195        1  a match                                 software                 NOUN
Time                 http://dbpedia.org/resource/Time                     200        3  available appointment times             Thing                    NOUN
Site                 http://dbpedia.org/resource/Site                     212        1  their Web sites                         Thing                    NOUN
Schedule             http://dbpedia.org/resource/Schedule                 222        1  Lucy's busy schedules                   Thing                    NOUN
Keyword              http://dbpedia.org/resource/Keyword                  227        1  The emphasized keywords                 Thing                    NOUN
Term                 http://dbpedia.org/resource/Term                     229        1  terms                                   Thing                    NOUN
Semantic             http://dbpedia.org/resource/Semantic                 231        1  whose semantics                         book                     NOUN
Meaning              http://dbpedia.org/resource/Meaning                  234        1  meaning                                 Thing                    NOUN
Web                  http://dbpedia.org/resource/Web                      245        1  the Semantic Web                        Thing                    PROPN
Minute               http://dbpedia.org/resource/Minute                   252        1  a few minutes                           organisation             NOUN
Hospital             http://dbpedia.org/resource/Hospital                 268        1  University Hospital                     university               PROPN
Town                 http://dbpedia.org/resource/Town                     275        1  town                                    settlement               NOUN
Place                http://dbpedia.org/resource/Place                    279        1  Mom's place                             Thing                    NOUN
Middle               http://dbpedia.org/resource/Middle                   289        1  the middle                              Thing                    NOUN
Hour                 http://dbpedia.org/resource/Hour                     292        1  rush hour                               organisation             NOUN
Search               http://dbpedia.org/resource/Search                   302        1  the search                              Thing                    NOUN
Preference           http://dbpedia.org/resource/Preference               306        1  stricter preferences                    Thing                    NOUN
Location             http://dbpedia.org/resource/Location                 308        1  location                                Thing                    NOUN
Trust                http://dbpedia.org/resource/Trust                    318        1  complete trust                          Thing                    NOUN
Context              http://dbpedia.org/resource/Context                  325        1  the context                             Thing                    NOUN
Task                 http://dbpedia.org/resource/Task                     330        1  the present task                        Thing                    NOUN
Certificate          http://dbpedia.org/resource/Certificate              337        1  access certificates                     Thing                    NOUN
Datum                http://dbpedia.org/resource/Datum                    342        1  the data                                Thing                    NOUN
Clinic               http://dbpedia.org/resource/Clinic                   362        1  a much closer clinic                    architectural structure  NOUN
Note                 http://dbpedia.org/resource/Note                     373        1  two warning notes                       Thing                    NOUN
Couple               http://dbpedia.org/resource/Couple                   383        1  a couple                                Thing                    NOUN
Problem              http://dbpedia.org/resource/Problem                  399        1  a problem                               Thing                    NOUN
Therapist            http://dbpedia.org/resource/Therapist                419        1  physical therapists                     Thing                    NOUN
Status               http://dbpedia.org/resource/Status                   427        1  Service type and insurance plan status  Thing                    NOUN
Mean                 http://dbpedia.org/resource/Mean                     432        1  other means                             Thing                    NOUN
Details              http://dbpedia.org/resource/Details                  443        1  "(Details                               Thing                    PROPN
Assent               http://dbpedia.org/resource/Assent                   451        1  her assent                              Thing                    NOUN
Moment               http://dbpedia.org/resource/Moment                   456        1  about the same moment                   MusicalComposition       NOUN
Detail               http://dbpedia.org/resource/Detail                   465        2  the details                             Thing                    NOUN
```

