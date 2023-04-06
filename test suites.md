# The Test Suite

Nodes in the network can consider queries and their outputs as test cases and group the test cases in test suites.   
This setup allows testing of processes of different deployments of the AnyLog Network in a simple and unified way.  
Using this setup a single command can trigger one or more tests on one or more nodes, whereas the results of the tests 
from all the participating nodes can be stored in a database and queried from a single point (like time series data that is managed by the network).    
In addition, users can leverage the functionality to test processes which are external to AnyLog and require comparisons of 
execution outputs to expected outputs.   

The testing processes provide the following:
* Assign a query to a _test case_ to validate correct execution output.
* Output of each _test case_ is organized in a special format called _test format_.
* Output of a _test case_ can be considered as **expected output** (over the _test data set_).   
* Output of a new run of a _test case_ (over the test data set) can be compared against the expected output.
* Reset data on a given network setup, and load test data set.
* Group test queries in a _test suite_ such that the tests is the suite can be executed by a single call.
* Include test cases and test suites in the scheduler such that tests are executed periodically.
* Update a database with test results allowing monitoring and alerts based on tests results.

## The test format

When a query is executed, the query params can make the query a _test case_ and direct the query result to an output
file that is organized in a _test format_.    
The test format has 3 sections:  
* **Header** - an informative section that includes a title, the date and time of the run, the query syntax, dbms used 
and output format of the returned rows.    
* **Body** - the _test case_ output.  
* **Footer** - statistical results including the execution time and the number of rows returned by the query.  

The example below demonstrates a query output in a test format:
```output 
==========================================================================
Title:    List Unique Values
Date:     2022-01-21 10:20:28.681237
Command:  select distinct(value) as value from ping_sensor order by value 
DBMS:     lsl_demo
Format:   json:output
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
```  

## The comparison process

Any 2 files in test format can be compared such that:
* Differences in the headers are ignored.
* Differences in the body trigger a failure with a message on the reason and location (line number) of the failure.
* Differences in footer - slower execution time is considered if **time** option is enabled.


## The `analyze` output command

The `analyze output` command compares 2 test files, each represents the result set of a _test case_, 
to determine if the test case was executed successfully.  

**Usage**:
```anylog
analyze output where file = [file path and name] and source = [file path and name] and option = time
``` 

_file_ - the path and file name to the query output that is being tested.   
_source_ - the path and file name to the source output that is trusted.  
_option_ (optional key - value pairs) - if **time** is added (option = time), the comparison will trigger a failure 
if the execution time is slower than the recorded time in the source file.  

**Example**:
```anylog
analyze output where file = !test_dir/test_file3.out and source = !test_dir/test_file2.out and option = time
``` 

## Directing a query output to a file and organizing the output in a test format

Using the [query options](queries.md#query-options), 
the query output can be directed to a file and organized as a test format.  
   
The following key-value pairs (added to the query in the query options section) are used to direct the query to a file in a test format:

| key    | value           | Details                               | Default Value |
| ------ | --------------- | ------------------------------------- | --------------|
| test   | True / False       | enable test format                  | False         |
| title  | any data string    | added to the header section         |               |
| file   | path and file name | the file to include the output data |               |

Note: If file name is prefixed with asterisk, the system will extend the output file name with a string making the file name unique.

The following example generates an output file in the folder with a name assigned to "test_dir". The asterisk on the file
name extends the name created to make the output name unique. The output file is in a _test format_ similar to the example 
in section [the test format](#the-test-format) above.

```anylog
run client () sql lsl_demo format=json and stat=true and test = true and  file = !test_dir\query_*.out and title = "Data set #35" "select distinct(value) as value from ping_sensor order by value"
``` 

## Executing a query and comparing the output to the trusted output

Using the query options, the query output can be compared to expected output. To enable execution of a query and compare 
the query output to expected results, include the key-value pairs that enable the output to a file in a test format and 
include the following:

| key    | value           | Details                          | Default Value |
| ------ | --------------- | -------------------------------- | --------------|
| source   | path and file name | the file with the expected results |        |
| option   | time       | enable time comparison       | False          |

**Example**:
```anylog
run client () sql lsl_demo format=json and stat=true and test = true and file = !test_dir\test_*.test and source = !test_dir\query_1.out and title = "Data set #35" "select distinct(value) as value from ping_sensor order by value"
``` 

**Notes**:
* If file name is asterisk, the system will generate a unique file name to the query output (in the folder assigned to "test_dir").
* If the comparison finds identical results, the created file is deleted. Otherwise, the created file remains at the designated folder.
* If option (with the value **time**) is not provided, the comparison will ignore the execution time.

## The test case command

The command _test case_ retrieves the query and the needed information from the header of a source file (organized in a _test format_), 
executes the query and compares the output to the source file.  

Usage:
```anylog
test case where source = [file path and name] and inform = [destination for messages] and time = [true/false] and dest = [destination nodes]
``` 

* The value assigned to the **time** key determines if the comparison considers execution time.
  

* The value assigned to **dest** is optional - if included, it specifies the Operator nodes to use.    
For example: (127.32.52.103:20048, 127.60.34.43:20048).  
  If not specifies, all the Operators with relevant data participate in the query process.
  

* The values assigned to the **inform** key determine where the test results are aggregated. The optional values are detailed 
in the chart below:    
  
| value    |  Details                          |
| ------ | -------------------------------------|
| stdout | the stdout of the machine executing the query |
| stdout@ip:port | the stdout of a target node with the IP and port |
| dbms.dbms_name.table_name@ip:port | As time series data at the target table at the target node  |

Note: 
1. The IP and Port to message the output of a different node is the TCP port published by the node.
2. The IP and Port to update the database of a different node is the REST port published by the node.
3. Multiple inform values are allowed.

The following example reads the query and query information from the source file "output_test.out", execute the query and 
compares the output of the execution to the source file.  
The test results are delivered to the screen as well as to a remote operator node to update the table "testing" in the database "qa". 
```anylog
test case where source = !test_dir/output_test.out and inform = stdout and inform = dbms.qa.testing@!qa_node
``` 


The example below shows the output of a test failure. The output identifies the reason for the failure:
```anylog
    {"result"   : "Failed", 
    "Title"     : "List Unique Values", 
    "Reason"    : "The value for the key 'timestamp' in line 11 is different: '2019-10-11 10:15:53.150009' vs. '2019-10-11 10:15:53.15000", 
    "File"      : "D:\Node\AnyLog-Network\data\test\run_of_test_1642789228.out", 
    "Trusted"   : "D:\Node\AnyLog-Network\data\test\test_1642789228.out"}
``` 

## The test suite command

The command **test suite** operates like **test case** on all the source files in a given directory.
Users can organize multiple test-cases in folders and sub-folders and test all the test cases in a single call.

Usage:
```anylog
test suite where source = [file path and name] and inform = [destination for messages] and subdir = [true/false] and time = [true/false]
``` 
* Source file name and file type can be prefixed with asterisk to consider only files with the name prefix ot type prefix.  
* If subdir is set to true, the files in the subdirectories are considered in the process.
* The value assigned to the **time** key determines if the comparison considers execution time.  

The following examples process the _test cases_ files identified by the key **source**: 
```anylog
test suite where source = !test_dir/test_*.out and and inform = dbms.qa.testing@!dest_node
test suite where source = !test_dir/test_*.o* and dest = stdout and subdir = true
``` 


