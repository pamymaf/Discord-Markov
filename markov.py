import markovify
import json

class Markov:
    def __init__(self):
        self.master_file = 'config/markovs.json'
        self.data = None
        self.load()
        self.process()

    def load(self):
        try:
            with open(self.master_file) as file:
                self.data = json.load(file)
        except(OSError, IOError):
            print("Couldn't load JSON in {}".format(self.json_file))

    def process(self):
        for m in self.data:
            print("Generating cache for "+m['name'])
            with open('logs/'+m['name']+'.txt') as t:
                text = t.read()

            if m['newline']:
                m['model'] = markovify.text.NewlineText()
            else:
                m['model'] = markovify.Text(text)

            self.updatecache(m)

    def updatecache(self, markov):
        while len(markov['cache']) <= 10:
            m = None
            while m == None:
                m = markov['model'].make_sentence()
            markov['cache'].append("\u200b"+m.encode("ascii","backslashreplace").decode("unicode-escape"))

    def getmarkov(self, arg):
        for m in self.master_file:
            if m['name'] == arg:
                msg = m['cache'].pop()
                self.updatecache(m)
                return msg
        return None