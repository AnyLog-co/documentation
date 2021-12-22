# PowerBI 

## Overview

Like with [Grafana](using%20grafana.md), the AnyLog REST interace provides the ability to generate content for business 
intelligence tools such as [PowerBI](https://powerbi.microsoft.com/en-us/).

## Requirements
* [PowerBI](https://powerbi.microsoft.com/en-us/downloads/)
* An AnyLog node accessible via REST  
* Python3
  * [requests](https://pypi.org/project/requests/)
  * [pandas](https://pypi.org/project/pandas/)

## Steps
1. Open PowerBI 
2. Home → More → Python
3. In the Pop-up use 

[```python
import pandas 
import requests 
 
def extract_data(conn:str, )
]()
```