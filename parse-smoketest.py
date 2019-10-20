import spacy
import datetime
import logging
logging.basicConfig(level=logging.INFO)

nlp = spacy.load('en_core_web_sm')

print('processing', datetime.datetime.utcnow())
doc = nlp(
    'However in recent times attempts at systematizing this relationship is imposed by the convergence brought about by technological change or data revolution which has enabled use of better observation devices that can be in citizen’s hands. However in recent times attempts at systematizing this relationship is imposed by the convergence brought about by technological change or data revolution which has enabled use of better observation devices that can be in citizen’s hands. However in recent times attempts at systematizing this relationship is imposed by the convergence brought about by technological change or data revolution which has enabled use of better observation devices that can be in citizen’s hands.'
)
print('done', datetime.datetime.utcnow())
doc.to_json()
