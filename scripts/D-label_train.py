import csv
from tqdm import tqdm 
from textblob.classifiers import MaxEntClassifier
import nltk
import pickle

train_cases = []
with open('coursedata.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in tqdm(reader):
        result = (row[3].lower(), row[1])
        train_cases.append(result)

print("Labels created")
nltk.download('punkt')

classifier = MaxEntClassifier(train_cases)

p = classifier.prob_classify("I love linear algebra!")
print(p.max())

file = open("classifyModel.pickle", "wb")
pickle.dump(classifier, file)
file.close()