# Managing Data files

A Publisher Node sends data to one or multiple servers. A server may be down and the data may not be transferred to the server. In addition, when the data is processed by the Operator, the data load may fail.  
The status of each data file is registered on the Publisher Node and the Operator Node. Each node updates the status and satisfies queries on the status of each file.
  
### The structure of the data files 
The data files contain Time Series Data (TSD) that is organized in JSON format.
Each file name follows a convention that is described below:

#### The file naming convention

File name is structured as follows:
<pre>
[DBMS name].[Table Name].[Partition].[ID device].[ID Operator].[Timestamp].[Hash Value of Data].[File Type]
</pre>

To monitor the status of the data filesWe monitor the state of each file in a process described below: