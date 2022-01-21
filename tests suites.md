# The Test Suite

As there are multiple deployments options for the nodes in the network, AnyLog is integrated with a test suite allowing
to set test scenarios that are executed and compared to expected results.  

The testing process allows to do the following:
* Assign a query to a ***test case*** to validate correct execution result.
* Output of each ***test case*** is organized in a special format called ***test format***.
* Output of a ***test case*** can be considered as ***expected output*** (over the ***test data set***).   
* Output of a new run of a ***test case*** (over the test data set) can be compared against the expected output.
* Reset data on a given network setup, and load test data set.
* Group test queries in a ***test suite*** such that the tests is the suite can be executed by a single call.
* Include test cases and test suites in the scheduler such that these tests are executed periodically.
* Update a database with test results allowing monitoring and alerts based on tests results.

## The test format

When a query is executed, the query params can make the query a ***test case*** and direct the query result to an output
file that is organized in a ***test format***.    
The test format has 3 sections:  
***Header*** - an informative section that includes a title, the date and time of the run and the query syntax.  
***body*** - the ***test case*** output.  
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

The ***analyze output*** command compares 2 test files, each represents the result set of a ***test case***, 
to determine if the test case was executed successfully.  

Usage:
<pre>
analyze output where file = [file path and name] and source = [file path and name] and option = time
</pre> 

***file*** - the path and file name to the query output that is being tested.   
***source*** - the path and file name to the source output that is trusted.  
***option*** (optional key - value pairs) - if ***time*** is added (option = time), the comparison will trigger a failure 
if the execution time is higher than the recorded time in the source file.  

Example:
<pre>
analyze output where file = !test_dir/test_file3.out and source = !test_dir/test_file2.out and include = time
</pre> 

## Directing a query output to a file and organizing the output in a test format

Using the query options, the query output can be directed to a file in a test format.  
The query options explained detailed in the [query options](https://github.com/AnyLog-co/documentation/blob/master/queries.md#query-options) section.  
The following key-value pairs provided in the query options section are used to direct the query to a file in a test format:

| key    | value           | Details                          | Default Value |
| ------ | --------------- | -------------------------------- | --------------|
| file   | path and file name | the file with the output data |               |
| test   | True / False       | enable test format            | False         |
| title  | any data string    | added to the header section   | None          |

The following example generates an output file, named query_1.out, in the folder with a name assigned to "test_dir".  
The output file is in a ***test format*** similar to the example in section [The test format](#the-test-format).
<pre>
sql lsl_demo format=json and stat=true and test = true and  file = !test_dir\query_1.out and title = "Data set #35" "select distinct(value) as value from ping_sensor order by value"
</pre> 

## Executing a query and returning the comparison to the trusted output

Using the query options, the query output can be compared to expected output.  
To enable execution of a query and compare the query output to expected results, include the key-value pairs that enable the output
to a file in a test format and include the following:

| key    | value           | Details                          | Default Value |
| ------ | --------------- | -------------------------------- | --------------|
| source   | path and file name | the file with the expected results |        |
| option   | time       | enable time comparison       | None          |

Example:

<pre>
sql lsl_demo format=json and stat=true and test = true and file = !test_dir\* and source= !test_dir\query_1.out and title = "Data set #35" "select distinct(value) as value from ping_sensor order by value"
</pre> 

Notes:
* If file name is asterisk, the system will generate a unique file name to the query output (in the folder assigned to "test_dir").
* If the comparison finds identical results, the created file is deleted. Otherwise, the created file remains at the designated folder.
* If option (with the value ***time***) is not provided, the comparison will ignore the execution time.

## The test case command

If an output file of a query is organized in a ***test format*** (hereon source file), the header section includes the query information.  
The command ***test case*** retrieves the query and the needed information from the header, executes the query and
compares the output to the source file.  

Usage:
<pre>
test case where source = [file path and name] and dest = [destination for messages]
</pre> 

The following example reads the query and query information from the source file "output_test.out", execute the query and 
compares the output of the execution to the source file.
<pre>
test case where source = !test_dir/output_test.out and dest = stdout
</pre> 

## The test suite command

The command ***test suite*** operates like ***test case*** on all the source files in a given directory.
Users can organize multiple test-cases in folders and sub-folders and test all the test cases in a single call.

Usage:
<pre>
test suite where source = [file path and name] and dest = [destination for messages] and subdir = [true/false]
</pre> 
* Source file name and file type can be prefixed with asterisk to consider only files with the name prefix ot type prefix.  
* If subdir is set to true, the files in the subdirectories are considered in the process.

The following examples considers designated files as ***test case*** files: 
<pre>
test case where source = !test_dir/*.out and dest = stdout
test case where source = !test_dir/*.o* and dest = stdout and subdir = true
</pre> 

