---
layout: default
parent: Northbound
title: Using Postgres to view Data
nav_order: 6
---
# Using Repeatable Queries to update a database with result sets

In EdgeLake, a Repeatable Query is a query placed on the EdgeLake rule engine, executed repeatedly, and configured 
to update a target table with the query results.

A common use case is to provide result sets to BI tools and third-party applications that do not support the _REST_ API.  
For these tools and applications, results sets of queries over the network data are hosted in a database.  
For example, [Tableu](https://www.tableau.com/) and [Lookr](https://developers.google.com/looker-studio) do not support 
the REST API but can leverage Repeatable Queries.

The examples below places the network data in PotgreSQL. 

## Setting up PostgreSQL 
<ol start="1">
   <li><a href="https://www.postgresqltutorial.com/install-postgresql/" target="_blank">Install PostgresSQL</a></li>
   
   <li>In <code>postgresql.conf</code>, update <bold>listen_address</bold> value to allow remote access
      <pre class="code-frame"><code class="language-config">listen_addresses = '*'</code></pre>
   </li>
   
   <li>In <code>pg_hba.conf</code>, add the following line at the bottom of the paga
      <pre class="code-frame"><code class="language-config">host    all            all             0.0.0.0/0               md5</code></pre>
   </li>
   
   <li>Restart PostgresSQL instance</li> 
</ol>

## Executing Query
<ol start="1">
   <li>On EdgeLake connect <code>>system_query</code> to Postgres database
      <pre class="code-frame"><code class="language-anylog">&lt;connect dbms system_query where 
   type=psql and 
   ip=127.0.0.1 and
   port=5432 and 
   user=anylog and 
   password=demo&gt;</code></pre>
   </li>
   
   <li>Execute query - <a href="https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#repeatable-queries" target="_blank">as repeatable query</a>
      <pre class="code-frame"><code class="language-anylog">run client () sql aiops format=table and table=fic11_mv and drop=true "select increments(hour, 1, timestamp), min(timestamp), min(value), avg(value), max(value) from fic11_mv where timestamp >= NOW() - 1 day"</code></pre>
   </li>

   <li>Utilize <code>query explain</code> to view how the results are generated
      <pre class="code-frame"><code class="language-anylog">AL aiops-single-node &lt; query explain
   07 Remote DBMS    : aiops
   07 Remote Table   : fic11_mv
   07 Source Command : select increments(hour, 1, timestamp), min(timestamp), min(value), avg(value), max(value) from fic11_mv where timestamp >= NOW() - 1 day
   07 Remote Query   : select date_trunc('day',timestamp), (extract(hour FROM timestamp)::int / 1), min(timestamp), min(value), SUM(value), COUNT(value), max(value) from fic11_mv where timestamp >= '2022-01-17T18:31:31.442147Z' group by 1,2
   07 Local Create   : create table new_table (increments_1_trunc timestamp without time zone, increments_1_extract integer, min_2 timestamp without time zone, min_3 double precision, SUM__value numeric, COUNT__value integer, max_5 double precision);
   <b>07 Local Query    : select min(min_2), min(min_3), SUM(SUM__value) /NULLIF(SUM(COUNT__value),0), max(max_5) from new_table group by increments_1_trunc,increments_1_extract order by increments_1_trunc,increments_1_extract</b>
   </code></pre></li>
</ol>

Note:
* In the example above, output is placed in table named: **fic11_mv**.
* If **drop** is set to True, every query execution deletes the previous result sets. Users can configure the process to be incremental to the previous result sets.  
* The [Query Options](https://github.com/AnyLog-co/documentation/blob/master/queries.md#query-options) document details the query configuration options.

## Extract Data onto Tableau
<ol start="1">
   <li><a href="https://www.tableau.com/products/desktop/download" target="_blank">Download & Install Tableau</a></li>
   <li>Under <i>Data</i> → <i>Data Sources</i> select PostgresSQL connector type
        <table>
            <tr>
                <td align="center"><img src="../../../imgs/tableau_img2a.png"  /></td>
                <td align="center"><img src="../../../imgs/tableau_img2b.png"  /></td>
            </tr>
        </table>
   </li>
   <li>Fill-out the information to connect to database & Press "Ok"
      <div class="image-frame">
         <img src="../../../imgs/tableau_img3.png"  />
      </div>
   </li>
   <li>Double-click on the table you want to use (in this case <code>new_table</code>) and go to worksheet
      <div class="image-frame">
         <img src="../../../imgs/tableau_img4.png"  />
      </div>
   </li>
</ol>

## Generating Graphs

The <code>system_query</code> database gathers (query) results from the different instances to generate a unified dataset for 
the user. As such, generating graphs from the final results is a bit complicated. 
   * Min 2 - is column <code>MIN(timestamp)</code>
   * Min 3 - is column <code>MIN(value)</code>
   * SUM(SUM__VALUE) / COUNT(new_table_count) -- is column <code>AVG(value)</code>
* MAX 5 - is column <code>MAX(value)</code>
<div class="image-frame">
   <img src="../../../imgs/tableau_img5.png"  />
</div>

To generate a graph, use "Min 2" as _Columns_ and all others for _Rows_
<div class="image-frame">
   <img src="../../../imgs/tableau_img6.png"  />
</div>