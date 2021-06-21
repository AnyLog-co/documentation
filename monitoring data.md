# Monitoring data

Nodes in the network can collect and monitor data in 2 ways:  
1.  By organizing the data in persistent storage in database tables that are hosted on operator nodes.
This approach allows viewing current and historical data by issuing queries to the database tables. This process of adding data 
    to tables is explained in the section: [Adding Data to Nodes in the Network](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#adding-data-to-nodes-in-the-network).
    
2. By configuring a node to monitor streaming/ingested data and track the recently added data. 
   This process allows evaluating ingested data as it streams into the node and apply monitoring and alerts on the most recent data.
   
## Configuring monitoring on streaming data

Using the command ***data monitor*** users can track data streamed to a node for storage and processing.  

Usage: 
<pre>
data monitor where dbms = [dbms name] and intervals = [counter] and time = 1 minute and time_column = timestamp and value_column = value
</pre>


Example: 
<pre>
data monitor where dbms = dmci and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
</pre>
