# term-analyzer
* Parse the terms from the given text by using spaCy nlp feature
* Analyze terms by creating SPARQL queries with SPARQLWrapper to find their entity of types
* Then find terms whose entity of type is class

## Installation
#### spaCy
```
$ pip install spacy
$ python -m spacy download en_core_web_sm
```

#### SPARQLWrapper
```
$ pip install sparqlwrapper
```

### Example Output
```
--------------------------
-----Class Terms List-----
--------------------------
1 . Term =  Sound
2 . Term =  Device
3 . Term =  Agent
4 . Term =  List
5 . Term =  Hospital
6 . Term =  Town
7 . Term =  Place
```

