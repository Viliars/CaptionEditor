with open("helpers.txt", "r") as fin:
    text = fin.read().strip()

samples = [[txt] for txt in text.split('\n')]

default_path = ""
