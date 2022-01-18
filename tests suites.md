# The Test Suite

As there are multiple deployments options for the nodes in the network, AnyLog is integrated with a test suite allowing
to set test scenarios that are executed and compared to expected results.  

The testing process allows to do the following:
* Execute one or more test queries.
* Organize the output of each query in a special format called ***test format***
* Consider query output (over a given data set) as the ***expected output***.   
* Compare the output of a query to its expected output.
* Reset data on a given network setup and load test data. 

## The test format

When a query is executed, the query params can direct the query result to an output file that is organized in a ***test format***.  
The test format has 3 sections:  
***Header*** - this is an informative section that includes a title, the date and time of the run and the query syntax.  
***body*** - the query output.  
***footer*** - statistical results including the execution time and the number of rows returned by the query.  

The example below demonstrates a query output in a test format:
<pre> 

==========================================================================
Title:    Report Title
Command:  select distinct(value) as value from ping_sensor order by value 
Date:     2022-01-17 19:36:15.559307
==========================================================================
{"value": 2}
{"value": 21}
{"value": 121}
{"value": 201}
{"value": 221}
{"value": 231}
{"value": 241}
{"value": 261}
{"value": 1021}
{"value": 2021}
{"value": 2100}
{"value": 2221}
{"value": 3221}
{"value": 5621}
==========================================================================
Rows:     14
Run Time: 00:00:03
==========================================================================
</pre>  

## The comparison process

Any 2 files in test format can be compared such that:
* Differences in the headers are ignored.
* Differences in the body trigger a failure with a message on the reason and location (line number) of the failure.
* Differences in footer - slower execution time is considered if ***time*** option is enabled.


## The analyze output command

The ***analyze output*** command compares 2 test files to determine if a query was successfully processed.  
Usage:
<pre>
analyze output where file = [file path and name] and source = [file path and name] and option = time
</pre> 
file - the path and file name to the query output that is being tested.   
source - the path and file name to the source output that is trusted.  
option (optional key - value pair) - if time is added, the comparison will trigger a failure is the execution time is higher than the recorded time in the source file.

