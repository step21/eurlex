# pyeurlex package

This is a python module to create SPARQL queries for the EU Cellar repository, run them and subsequently download their data. Notably, it directly supports all resource types. Some parts like the SPARQL queries are based on the R-based [eurlex](https://github.com/michalovadek/eurlex) package by Michal Ovadek, but then I wanted one for python and was not satisfied with existing python packages.

## Status

![Build and Test](https://github.com/step21/eurlex/actions/workflows/build.yaml/badge.svg) | [![codecov](https://codecov.io/gh/step21/eurlex/branch/main/graph/badge.svg?token=5EXROQA8XK)](https://codecov.io/gh/step21/eurlex)

[Coverage Graph](https://codecov.io/gh/step21/eurlex/branch/main/graphs/tree.svg?token=5EXROQA8XK)

## Usage

Import and instantiate the moduel

```
from eurlex import Eurlex
eur = Eurlex()
```

Then you can construct you query. (or alternatively you can use your own or one constructed via the wizard https://op.europa.eu/en/advanced-sparql-query-editor

```
q = eur.make_query(resource_type = "caselaw", order = True, limit = 10)
print(q)
```

Finally, you can run this query.

```
d = eur.query_eurlex(q)  # where q is a query generated in a previous step or a string defined by you
print(d)
```
This will return a pandas data frame of the results. Its columns depend on the the fields that you included. At the moment, not all fields are named properly in the dataframe and you will have to set their name manually if desired.

Once you pick a single url or identifier from the df, you can download a notice or data based on that indentifier. To download the notices as xml, use `download_xml()` as below.

```
x = eur.download_xml("32014R0001", notice="tree") # without the file parameter to specify the filename, the celex number will be used.
print(x)
```

To get data associated with an identifier, use `get_data()`. This will return the data as a string,
```
d = eur.get_data("http://publications.europa.eu/resource/celex/32016R0679", type="text")
print(d)
```

# Why another package/module?

While there was already the R packages by Michal Ovadek, I wanted a python implementation.
There is also https://github.com/seljaseppala/eu_corpus_compiler but that also only does regulatory/legislative documents. Additionally, there is https://pypi.org/project/eurlex/, but it for example does not have a way to generate SPARQL queries and is also very focused on legislation. In addition, while internally it uses SPARQL and cellar as well, its documentation is focused on accessing and processing documents via CELEX number, which is not really helpful to me. Another one is https://github.com/Lexparency/eurlex2lexparency which also seems to focus on legislative documents and 
