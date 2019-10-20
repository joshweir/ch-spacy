import spacy
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import neuralcoref
from nlp_architect.pipelines.spacy_bist import SpacyBISTParser

nlp = spacy.load('en_core_web_sm')
nlp.replace_pipe("parser", SpacyBISTParser())
neuralcoref.add_to_pipe(nlp)

print('processing', datetime.datetime.utcnow())
doc = nlp(
    'However in recent times attempts at systematizing this relationship is imposed by the convergence brought about by technological change or data revolution which has enabled use of better observation devices that can be in citizen’s hands. However in recent times attempts at systematizing this relationship is imposed by the convergence brought about by technological change or data revolution which has enabled use of better observation devices that can be in citizen’s hands. However in recent times attempts at systematizing this relationship is imposed by the convergence brought about by technological change or data revolution which has enabled use of better observation devices that can be in citizen’s hands.'
)
print('done', datetime.datetime.utcnow())
doc.to_json()
doc._.coref_clusters
