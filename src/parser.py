#!/usr/bin/python3
import spacy
import logging;
logging.basicConfig(level=logging.INFO)
# import neuralcoref
import json
import datetime

class ChProcess(object):
  def __init__(self, model_name): 
    self.nlp = spacy.load(model_name)
    # disabled = self.nlp.disable_pipes("tagger")
    # self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))
    # neuralcoref.add_to_pipe(self.nlp)

  def to_json(self, data, args):
    collapse_punctuation = False
    collapse_phrases = False
    output = []

    print('processing nlp')
    print('processing', datetime.datetime.utcnow())
    # docs = self.nlp.pipe([data])
    docs = [self.nlp(data)]
    print('done processing nlp')
    print(datetime.datetime.utcnow())
    for doc in docs:
      if collapse_punctuation:
        spans = []
        for word in doc[:-1]:
          if word.is_punct:
            continue
          if not word.nbor(1).is_punct:
            continue
          start = word.i
          end = word.i + 1
          while end < len(doc) and doc[end].is_punct:
            end += 1
          span = doc[start: end]
          spans.append(
            (span.start_char, span.end_char, word.tag_, word.lemma_, word.ent_type_)
          )
        for span_props in spans:
          self.doc.merge(*span_props)

      if collapse_phrases:
        for np in list(doc.noun_chunks):
          np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)

      # print(doc.to_json())
      # output = json.loads(doc.to_json())
      
      words = [{'text': w.text, 'tag': w.tag_, 'dep': w.dep_, 'head': w.head.i, 'index': w.i, 'ent': w.ent_type_, 'idx': w.idx} for w in doc]
      # arcs = []
      # for word in doc:
      #   if word.i < word.head.i:
      #     arcs.append(
      #       {
      #           'start': word.i,
      #           'end': word.head.i,
      #           'label': word.dep_,
      #           'text': str(word),
      #           'dir': 'left'
      #       })
      #   elif word.i > word.head.i:
      #     arcs.append(
      #       {
      #           'start': word.head.i,
      #           'end': word.i,
      #           'label': word.dep_,
      #           'text': str(word),
      #           'dir': 'right'
      #       })

      print('processing corefs')
      print(datetime.datetime.utcnow())
      mentions = []
      clusters = []
      resolved = []
      # if doc._.has_coref:
      #   mentions = [{'start':    mention.start_char,
      #                 'end':      mention.end_char,
      #                 'text':     mention.text,
      #                 'resolved': cluster.main.text
      #               }
      #               for cluster in doc._.coref_clusters
      #               for mention in cluster.mentions]
      #   clusters = list(list(span.text for span in cluster)
      #                   for cluster in doc._.coref_clusters)
      #   resolved = doc._.coref_resolved

      sentences = []
      for s in list(doc.sents):
        sentences.append({ 'start': s.start, 'end': s.end })

      doutput = {}
      doutput['text'] = doc.text
      doutput['sents'] = sentences
      doutput['words'] = words
      doutput['mentions'] = mentions
      doutput['clusters'] = clusters
      doutput['resolved'] = resolved
      output.append(doutput)
    
    # return {'words': words, 'arcs': arcs, 'mentions': mentions, 'clusters': clusters, 'resolved': resolved}
    return output
