from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer


def evaluate_msg(msg):
    tb = Blobber(msg, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    blob = tb(msg)
    print(tb.polarity)
evaluate_msg('Ce message est génial merci je suis content')