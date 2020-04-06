import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

print("hey")

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

for entity in doc.noun_chunks:
    # check for pronouns
    if entity.root.pos_ != "PRON":
        myTerm = entity.root.lemma_
        # print(entity.text, " --> ", entity.root.lemma_)
        # check if the term is not in the list
        if myTerm not in termList:
            # add term to the term list
            termList.append(myTerm)


print("----------List----------\n------------------------")
for term in termList:
    print(term)