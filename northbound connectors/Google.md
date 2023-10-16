# Google Drive

To extract data from AnyLog into Google Drive we recommend using a tool called [Two Minute Reports](https://workspace.google.com/marketplace/app/two_minute_reports/6804555176)
which provides the ability to import data via REST, Database, Social Media and other SEO services. 

## Install 

1. Under _Extensions_ goto _Add-ons_ → _Get add-ons_
![extensions → add-ons](../imgs/googledrive_install_step1.png)


2. In the search bar look for "Two Minute Reports" & double click it
![software list](../imgs/googledrive_install_step2.png)


3. Install the add-on to your Google Sheets & press "continue"  

| ![install screen 1](../imgs/googledrive_install_step3a.png) | ![install screen 2](../imgs/googledrive_install_step3b.png) |
| --- | --- |

4. Google Requires users to confirm - click on the user you'd like to install the application on & press "Allow" 

| ![confirm account](../imgs/googledrive_install_step4a.png) | ![grant permission](../imgs/googledrive_install_step4b.png) | 
| --- | --- |


## Executing REST Request

1. Once that's completed launch _Two Minute Reports_: _Extensions_ → _Two Minute_Reports_ → Launch
![path](../imgs/googledrive_execute_step1)
**Note**: _Two Minute Reports_ works best when only a single account is logged in.


2. Press "Add+" to connect to a new REST connection
![add](../imgs/googledrive_execute_step2.png)


3. Under _Data Source_ set the Type to API Bridge & Fill-out the form

Notice that for the complete form user should specifiy: _Base URL_, _Authentication_ (if set) and headers.    
For demo purposes, I'm using a query that consists of [increments function](../queries.md#the-increment-function) and returns the data as a list of JSON values without statistics:
```sql
sql aiops format=json:list and stat=false "select increments(hour, 1, timestamp), min(timestamp) as timestamp, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from sic1001_mv where timestamp >= NOW() - 1 week"
```

| ![type](../imgs/googledrive_execute_step3a.png) | ![form](../imgs/googledrive_execute_step3b.png) |
| --- | --- |

4. Once the form is complete, test and save the changes - this will validate that the request is valid

| ![test & save](../imgs/googledrive_execute_step4a.png) | ![confirm](../imgs/googledrive_execute_step4b.png) | 
| --- | --- |

5. In menu, goto _Data Queries_

![menu options](../imgs/googledrive_execute_step5.png)


6. Press _Add+_ to create a new Query Form

![add query form](../imgs/googledrive_execute_step6.png)

7. Fill-out the form, setting _Data Source_ to be the same as the the one created earlier & press "Run Query"

![complete form](../imgs/googledrive_execute_step7.png)

The steps mentioned above will ultimately result in a table similar to the one shown on the right of the image; with it
users can generate images and graphs as shown on the right side of the image, just like any other data set

![table & graph](../imgs/googledrive_final_result.png)
