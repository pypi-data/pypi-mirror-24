import codecs
import json


def load(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return json.loads(f.read())
