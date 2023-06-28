from os import listdir
import string
from pickle import dump
from pickle import load

def load_doc(filename):
    file = open(filename, encoding = "utf-8")
    text = file.read()
    file.close()
    return text

def load_stories(directory):
    all_stories = list()
    for name in listdir(directory):
        filename = directory + '/' + name
        doc = load_doc(filename)
        story, highlights = split_story(doc)
        all_stories.append({'stories': story, 'highlights': highlights})
    return all_stories

#hi :)
# hihihihihi
# >:D    :)))))    :DDDDDDDDDDDDDDD
# >:)
# nplease ignore the above, thank you       ^_^

def split_story(doc):
    index = doc.find('@highlight')
    story, highlights = doc[:index], doc[index:].split('@highlight')
    highlights = [h.strip() for h in highlights if len(h) > 0]
    return story, highlights

def clean_lines(lines):
    cleaned = list()
    table = str.maketrans('','', string.punctuation)
    for line in lines:
        index = line.find('(CNN) -- ')
        if index > -1:
            line = line[index + len('(CNN)'):]
            line = line.split()
            line = [word.lower() for word in line]
            line = [w.translate(table) for w in line]
            line = [word for word in line if word.isalpha()]
            cleaned.append(' '.join(line))
            cleaned = [c for c in cleaned if len(c) > 0]
    return cleaned

directory = '/Users/bennettye/Downloads/cnn/stories'
stories = load_stories(directory)
print('Loaded Stories %d' % len(stories))

for example in stories:
    example['stories'] = clean_lines(example['stories'].split('\n'))
    example['highlights'] = clean_lines(example['highlights'])

dump(stories, open('cnn_dataset.pkl', 'wb'))
stories = load(open('cnn_dataset.pkl', 'rb'))
print('Loaded Stories %d' % len(stories))