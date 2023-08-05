# Generate and display a diagram using Plantuml


```python
$ ipython2

In [1]: import nbplatuml

In [2]:

%%plantuml figure1

@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response
@enduml  

````
