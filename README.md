# pycrfsuite를 이용한 한국어 띄어쓰기 교정

## Usage

주어진 문장을 feature로 변환하기 위해 다음의 두 가지 클래스를 import 합니다. 

    import sys
    sys.path.append('../')

    from pycrfsuite_spacing import TemplateGenerator
    from pycrfsuite_spacing import CharacterFeatureTransformer

TemplateGenerator와 FeatureTransformer를 이용하면 띄어쓰기가 포함된 문장을 다음과 같이 template에 의하여 정의되는 character feature로 변환해 줍니다. 두 칸 이상의 띄어쓰기는 없다고 가정합니다.

    to_feature = CharacterFeatureTransformer(TemplateGenerator(begin=-2, 
                                                               end=2,
                                                               min_range_length=3,
                                                               max_range_length=3))

    x, y = sent_to_xy('이것도 너프해 보시지', to_feature)
    pprint(x)
    print(y)
    
결과는 아래와 같습니다. 

    [['X[0,2]=이것도'],
     ['X[-1,1]=이것도', 'X[0,2]=것도너'],
     ['X[-2,0]=이것도', 'X[-1,1]=것도너', 'X[0,2]=도너프'],
     ['X[-2,0]=것도너', 'X[-1,1]=도너프', 'X[0,2]=너프해'],
     ['X[-2,0]=도너프', 'X[-1,1]=너프해', 'X[0,2]=프해보'],
     ['X[-2,0]=너프해', 'X[-1,1]=프해보', 'X[0,2]=해보시'],
     ['X[-2,0]=프해보', 'X[-1,1]=해보시', 'X[0,2]=보시지'],
     ['X[-2,0]=해보시', 'X[-1,1]=보시지'],
     ['X[-2,0]=보시지']]
    ['0', '0', '1', '0', '0', '1', '0', '0', '1']
    
모델의 학습은 다음과 같습니다. docs는 ['문장1', '문장 2', ... ] 와 같은 list of str (like) 입니다.

    from pycrfsuite_spacing import PyCRFSuiteSpacing

    correct = PyCRFSuiteSpacing(to_feature)
    correct.train(docs, 'demo_model.crfsuite')

학습된 모델 역시 callable 하며, 다음과 같이 띄어쓰기 교정이 됩니다. 

    correct('이건진짜좋은영화라라랜드진짜좋은영화')
    
    $ '이건 진짜 좋은 영화 라라랜드 진짜 좋은 영화'

## Requires

- python-crfsuite >= 0.9.2

