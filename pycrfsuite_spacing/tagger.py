import pycrfsuite
from .transform import docs_to_xy
from .transform import sent_to_xy

class PyCRFSuiteSpacing:
    def __init__(self, to_feature, tagger=None, verbose=False,
                 feature_vocabulary=None,
                 feature_minfreq=0, max_iterations=100):
        self.tagger = tagger
        self.to_feature = to_feature
        self.verbose = verbose
        self.feature_vocabulary = feature_vocabulary
        self.params = {'feature.minfreq':max(0,feature_minfreq),
                       'max_iterations':max(1, max_iterations)
                      }
        
        if type(tagger) == 'str':
            try:
                self.load_tagger(tagger)
            except Exception as e:
                print(e)
                self.tagger = None

    def __call__(self, sent):
        return self.correct(sent)
    
    def train(self, docs, model_fname):
        if not self.feature_vocabulary:
            self.feature_vocabulary = self._scan_features(docs)
        trainer = pycrfsuite.Trainer(verbose=self.verbose)
        if self.verbose:
            print('begin appending data to trainer')
        for sent in docs:
            x, y = sent_to_xy(sent, self.to_feature)
            if len(x) != len(y):
                continue
            x = [[xij for xij in xi if xij in self.feature_vocabulary] for xi in x]
            trainer.append(x, y)
        if self.verbose:
            print('all data are appended to trainer. begin training')
        trainer.set_params(self.params)
        trainer.train(model_fname)
        self.load_tagger(model_fname)
    
    def _scan_features(self, docs):
        from collections import defaultdict
        min_count = self.params['feature.minfreq']
        
        feature_vocabulary = defaultdict(int)
        if self.verbose:
            print('feature scanning: begin with min_count={}'.format(min_count))
        
        for sent in docs:
            x, _ = sent_to_xy(sent, self.to_feature)
            for xi in x:
                for xij in xi:
                    feature_vocabulary[xij] += 1
        if self.verbose:
            print('feature scanning ... {} -> '.format(len(feature_vocabulary)), end='')
            
        feature_vocabulary = {feature for feature, count in feature_vocabulary.items() if count >= min_count}
        if self.verbose:
            print('{} with min_count={}'.format(len(feature_vocabulary), min_count))
            
        return feature_vocabulary
        
    def load_tagger(self, model_fname):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model_fname)
    
    def correct(self, sent):
        x, y0 = sent_to_xy(sent, self.to_feature)
        y1 = []

        b = 0
        for i in range(len(x)):
            if y0[i] == '1':
                y1 += self.tagger.tag(x[b:i+1])[:-1] + ['1']
                b = i+1
        return ''.join([ci if yi == '0' else ci+' ' for ci, yi in zip(sent.replace(' ',''), y1)]).strip()