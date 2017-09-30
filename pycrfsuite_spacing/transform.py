class TemplateGenerator:
    def __init__(self, begin=-2, end=2, min_range_length=2, max_range_length=5, remove_partial=False):
        self.begin = begin
        self.end = end
        self.min_range_length = min_range_length
        self.max_range_length = max_range_length
        self.remove_partial = remove_partial
        self._generate_token_templates()
    
    def _generate_token_templates(self):
        self.templates = []
        for b in range(self.begin, self.end):
            for e in range(b, self.end+1):
                length = (e - b + 1)
                if length < self.min_range_length or length > self.max_range_length: 
                    continue
                if b * e > 0: continue
                if self.remove_partial and b * e == 0: continue
                self.templates.append((b, e))
    
    def __iter__(self):
        for template in self.templates:
            yield template
    
    def tolist(self):
        return self.templates

class CharacterFeatureTransformer:
    def __init__(self, templates):
        self.templates = templates
    def __call__(self, chars, tags=None):
        x =[]
        for i in range(len(chars)):
            xi = []
            e_max = len(chars)
            for t in self.templates:
                b = i + t[0]
                e = i + t[1] + 1
                if b < 0 or e > e_max:
                    continue
                xi.append(('X[%d,%d]' % (t[0], t[1]), chars[b:e]))
            x.append(xi)
        return x

def sent_to_chartags(sent, nonspace=0, space=1):
    chars = sent.replace(' ','')
    tags = [nonspace]*(len(chars) - 1) + [space]
    idx = 0
    for c in sent:
        if c == ' ':
            tags[idx-1] = space
        else:
            idx += 1
    return chars, tags

def sent_to_xy(sent, feature_transformer):
    chars, tags = sent_to_chartags(sent)
    x = [['%s=%s' % (xij[0], xij[1]) for xij in xi] for xi in feature_transformer(chars, tags)]
    y = [str(t) for t in tags]
    return x, y

def docs_to_xy(docs, feature_transformer):
    train_x, train_y = tuple(zip(*[sent_to_xy(doc, feature_transformer) for doc in docs]))
    return train_x, train_y