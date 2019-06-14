from django.test import TestCase

# Create your tests here.
data=[
    {'1':[{'id': 1}, {'name':'jsdk'},{'file':456}]}
    [{'id': 1}, {'name': 'jsdk'}],
    [{'id': 1}, {'name': 'jsdk'}],

]
# data=[
#     {'id': 1,'name':'jsdk'},
#     {'id': 1, 'name': 'jsdk'},
#     {'id': 1, 'name': 'jsdk'}
#
# ]

for singer in data:
    print(singer)
    for info in singer:
        for k,v in info.items():
            print(k,v)
