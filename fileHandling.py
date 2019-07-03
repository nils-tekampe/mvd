import re


def carriesValidVersionInformation(file):
    m = re.search(r'V[0-9]+\.[0-9]+\.[0-9]+', file)
    return (m is not None)
    
    

