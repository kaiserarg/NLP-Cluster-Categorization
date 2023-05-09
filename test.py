from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import recall_score, precision_score

A=[['a','b','c'],['d','e','f','g']]
B=[['a','b'],['d','f','g']]

multi = MultiLabelBinarizer()

A_new = multi.fit(A).transform(A)
B_new = multi.transform(B)

precision_score(A_new,B_new,average='samples')
recall_score(A_new, B_new, average='samples')

input_list = [('pewdiepie', 'Gaming'), ('NASA', 'Gaming'), ('Dan', 'Gaming'), ('Mark', 'Science'), ('Jane', 'Cooking'), ('John', 'Cooking')]

categories = {}

for name, category in input_list:
    if category not in categories:
        categories[category] = []
    categories[category].append(name)

result = list(categories.values())
print(result)

