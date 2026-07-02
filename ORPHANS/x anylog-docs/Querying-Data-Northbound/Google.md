---
title: Google Drive
description: Demonstration on how to connect to AnyLog and gather data for analysis on Google Drive applicaitons
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

To extract data from AnyLog into Google Drive we recommend using a tool called [Two Minute Reports](https://workspace.google.com/marketplace/app/two_minute_reports/6804555176)
which provides the ability to import data via REST, Database, Social Media and other SEO services. 

## Install 

1. Under _Extensions_ goto _Add-ons_ → _Get add-ons_
!<a href="{{ '/docs/assets/img/googledrive_install_step1.png/' | relative_url }}">extensions → add-ons</a>


2. In the search bar look for "Two Minute Reports" & double click it
!<a href="{{ '/docs/assets/img/googledrive_install_step2.png/' | relative_url }}">software list</a>


3. Install the add-on to your Google Sheets & press "continue"  

| !<a href="{{ '/docs/assets/img/googledrive_install_step3a.png/' | relative_url }}">install screen 1</a> | !<a href="{{ '/docs/assets/img/googledrive_install_step3b.png/' | relative_url }}">install screen 2</a> |
| --- | --- |

4. Google Requires users to confirm - click on the user you'd like to install the application on & press "Allow" 

| !<a href="{{ '/docs/assets/img/googledrive_install_step4a.png/' | relative_url }}">confirm account</a> | !<a href="{{ '/docs/assets/img/googledrive_install_step4b.png/' | relative_url }}">grant permission</a> | 
| --- | --- |


## Executing REST Request

1. Once that's completed launch _Two Minute Reports_: _Extensions_ → _Two Minute_Reports_ → Launch
!<a href="{{ '/docs/assets/img/googledrive_execute_step1/' | relative_url }}">path</a>
**Note**: _Two Minute Reports_ works best when only a single account is logged in.


2. Press "Add+" to connect to a new REST connection
!<a href="{{ '/docs/assets/img/googledrive_execute_step2.png/' | relative_url }}">add</a>


3. Under _Data Source_ set the Type to API Bridge & Fill-out the form

Notice that for the complete form user should specifiy: _Base URL_, _Authentication_ (if set) and headers.    
For demo purposes, I'm using a query that consists of <a href="{{ '/docs/Querying-Data-Northbound/queries/#the-increment-function' | relative_url }}">increments function</a> and returns the data as a list of JSON values without statistics:
```sql
sql aiops format=json:list and stat=false "select increments(hour, 1, timestamp), min(timestamp) as timestamp, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from sic1001_mv where timestamp >= NOW() - 1 week"
```

| !<a href="{{ '/docs/assets/img/googledrive_execute_step3a.png/' | relative_url }}">type</a> | !<a href="{{ '/docs/assets/img/googledrive_execute_step3b.png/' | relative_url }}">form</a> |
| --- | --- |

4. Once the form is complete, test and save the changes - this will validate that the request is valid

| !<a href="{{ '/docs/assets/img/googledrive_execute_step4a.png/' | relative_url }}">test & save</a> | !<a href="{{ '/docs/assets/img/googledrive_execute_step4b.png/' | relative_url }}">confirm</a> | 
| --- | --- |

5. In menu, goto _Data Queries_

!<a href="{{ '/docs/assets/img/googledrive_execute_step5.png/' | relative_url }}">menu options</a>


6. Press _Add+_ to create a new Query Form

!<a href="{{ '/docs/assets/img/googledrive_execute_step6.png/' | relative_url }}">add query form</a>

7. Fill-out the form, setting _Data Source_ to be the same as the the one created earlier & press "Run Query"

!<a href="{{ '/docs/assets/img/googledrive_execute_step7.png/' | relative_url }}">complete form</a>

The steps mentioned above will ultimately result in a table similar to the one shown on the right of the image; with it
users can generate images and graphs as shown on the right side of the image, just like any other data set

!<a href="{{ '/docs/assets/img/googledrive_final_result.png/' | relative_url }}">table & graph</a>
