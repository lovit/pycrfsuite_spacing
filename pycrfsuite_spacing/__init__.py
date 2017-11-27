__version__ = 1.0
__author__ = 'lovit'

from .transform import TemplateGenerator
from .transform import CharacterFeatureTransformer
from .transform import sent_to_chartags
from .transform import sent_to_xy
from .transform import docs_to_xy
from .tagger import PyCRFSuiteSpacing