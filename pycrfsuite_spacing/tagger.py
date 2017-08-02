import pycrfsuite
from .transform import docs_to_xy
from .transform import sent_to_xy

class PyCRFSuiteSpacing:
    def __init__(self, to_feature, tagger=None, verbose=False):
        self.tagger = tagger
        self.to_feature = to_feature
        self.verbose = verbose
        
        if type(tagger) == 'str':
            try:
                self.load_tagger(tagger)
            except Exception as e:
                print(e)
                self.tagger = None

    def __call__(self, sent):
        return self.correct(sent)
    
    def train(self, docs, model_fname):        
        train_x, train_y = docs_to_xy(docs, self.to_feature)
        trainer = pycrfsuite.Trainer(verbose=self.verbose)
        for x, y in zip(train_x, train_y):
            if len(x) != len(y):
                continue
            trainer.append(x, y)
        trainer.train(model_fname)
        self.load_tagger(model_fname)
    
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