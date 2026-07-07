---
layout: default
parent: Northbound
title: Using PowerBI
nav_order: 3
---
# EdgeLake with PowerBI 

The following provides insight as to how to generate graphs and images using [Microsoft PowerBI](https://powerbi.microsoft.com/en-us/downloads/) with data from EdgeLake. 
The same process can be done with _Excel_ and other Microsoft tools. 

## Sample REST request
In order to support PowerBI, return data as a list of JSON values without the statistical information.


**Sample cURL request**
<pre class="code-frame"><code class="language-shell">curl -X GET 10.1.2.10:2149 \
    -H 'command: sql aiops format=json:list and stat=false "SELECT date(timestamp) as timestamp, min(value) as min, avg(value) as avg, max(value) as max FROM lic1_mv group by timestamp ORDER by timestamp limit 10"' \
    -H "User-Agent: AnyLog/1.23" \ 
    -H "destination: network" -w "\n"
</code></pre>

**Sample Output** (the data is returned as a list of JSON objects).
<pre class="code-frame"><code class="language-json">[
    {"timestamp": "2021-12-17", "min": 16.07562231854013, "avg": 16.07562231854013, "max": 16.07562231854013},
    {"timestamp": "2021-12-18", "min": 0.7819949317261932, "avg": 37.58098167042068, "max": 85.13897566679766},
    {"timestamp": "2021-12-22", "min": 3.545549704985503, "avg": 44.07391736121831, "max": 75.688516046041},
    {"timestamp": "2021-12-23", "min": 30.13388089233143, "avg": 54.983077931262265, "max": 84.77061503184196},
    {"timestamp": "2021-12-29", "min": 17.614363625825547, "avg": 47.44901351353519, "max": 79.27651061410472},
    {"timestamp": "2021-12-30", "min": 12.324781800659816, "avg": 45.14157473898287, "max": 78.54948001563031},
    {"timestamp": "2022-01-01", "min": 19.389259167237835, "avg": 62.144516285293186, "max": 98.28053568049772},
    {"timestamp": "2022-01-02", "min": 50.596673938692426, "avg": 50.596673938692426, "max": 50.596673938692426},
    {"timestamp": "2022-01-08", "min": 53.17291222256768, "avg": 78.21358089166576, "max": 93.42429844531414},
    {"timestamp": "2022-01-09", "min": 54.664901456750904, "avg": 75.73146536262269, "max": 96.79802926849446}
]
</code></pre>

## Using PowerBI
<ol start="1">
   <li>Under <i>Get Data</i> open <i>Web</i>
      <div class="image-frame"><img src="../../../imgs/powerbi_img1.png" /></div>
   </li>

   <li>In the Advanced option fill-out the <b>URL</b>, and <b>HEADER</b> parameters. Once the form is filled out press "OK"
   <table>
      <tr>
         <td>
<pre class="code-frame"><code class="language-json">{
   "command": "[YOUR QUERY]", 
   "User-Agent": "AnyLog/1.23",  
   "destination": "network"
}</code></pre>
         </td>
         <td><div class="image-frame"><img src="../../../imgs/powerbi_img2.png" /></div></td>
      </tr>
   </table>
   </li>

   <li>Right-click and & select JSON
      <div class="image-frame"><img src="../../../imgs/powerbi_img3.png" /></div>
   </li>

   <li>Right-click on **List** & select _To Table_
      <div class="image-frame"><img src="../../../imgs/powerbi_img4.png" /></div>
   </li>

   <li>Keep defaults (None) and press "OK"
      <div class="image-frame"><img src="../../../imgs/powerbi_img5.png" /></div>
   </li>
   
   <li>Press the button on the right of the column to view list of columns. This will show the different JSON keys 
that’ll be converted to table columns
      <table>
      <tr>
         <td align="center"><img src="../../../imgs/powerbi_img6a.png" /></td>
         <td align="center"><img src="../../../imgs/powerbi_img6b.png" /></td>
      </tr>
      </table>
   </li>

   <li>For each column, you should update to the correct data-type otherwise PowerBI will assume the data type is string
      <div class="image-frame"><img src="../../../imgs/powerbi_img7.png" /></div>
   </li>
   
   <li>Once updated press Close & Apply
      <div class="image-frame"><img src="../../../imgs/powerbi_img8.png" /></div>
   </li>

   <li>From this point you should be able to draw tables & graphs with the data
   <br/>The following shows 3 diagrams, each is assigned to its own query
      <ul style="padding-left: 20px">
         <li>The table shows number of rows per table in the database</li>
         <li>The bar graph shows <i>MIN, MAX, AVG and Row Count</i> difference between 2021 and 2022.</li>
         <li>The line graph uses [increments function](https://github.com/AnyLog-co/documentation/blob/master/queries.md#the-increment-function) to <i>MIN, MAX and AVG</i> over time</li>
      </ul>
      <div class="image-frame"><img src="../../../imgs/powerbi_img9.png" /></div>
   </li>
</ol>

## Error Handling 

When converting raw content into _Text_, [PowerQuery Editor](https://docs.microsoft.com/en-us/power-query/power-query-ui) will show results. However, it will not separate the 
JSON keys into separate columns

<div class="image-frame"><img src="../../../imgs/error_img1.png" /></div>
