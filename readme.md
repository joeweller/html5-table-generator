# Intro to Html5TableGenerator
Html5TableGenerator will accept either a .csv/.tsv file or a nested list of values and will return a html table.
It also features the ability to use classes found within the CSS/JS web framework: Bootstrap4

# Usage
Html5TableGen may only take in __one__ source argument; __file__ or __list__

```python3
from tablegen import Html5TableGenerator

# generate a table from a local .csv file
table_csv = Html5TableGenerator(
        file='path-to-file.csv',
        file_type='csv',
        footer=True,
        bs=False,
)

# print html table to screen
print(table_csv.output())


# generate a table from a nested list

data_list = [
        ['DOB', 'Name', 'Location'],
        ['02/1989', 'Bill', 'Spain'],
        ['12/1984', 'Pat', 'India'],
]

table_data = Html5TableGenerator(
        data=data_list,
        bs=True,
        footer=False,
)
        
# print html table to screen
print(table_data.output())
```
