# Using the AnyLog GUI

The AnyLog GUI serves as an example application that interacts with the network.

## Prerequisites
* Install the AnyLog GUI Code
* Install Grafana
* Login to the AnyLog GUI - The default HTTP port that AnyLog GUI listens to is 5000 - On a local machine go to ```http://localhost:5000/```.
* [Login to Grafana](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) - The default HTTP port that AnyLog GUI listens to is 3000 - On a local machine go to ```http://localhost:3000/```.


## Configure Grafana
Change the following configuration options in the .ini configuration file:
Notes: 
- You must restart Grafana for any configuration changes to take effect.
- Optional locations for the Grafana .ini file:
  * Winodws Config: `C:\Program Files\GrafanaLabs\grafana\conf\custom.ini`
  * Linux Config: `/etc/grafana/grafana.ini`
  * For Docker, the Grafana config file name is `grafana.ini`, except it's stored within a Docker volume (if created); if not it is a hidden file. 
[Grafana Docker Documentation](https://grafana.com/docs/grafana/latest/installation/docker/)
  
| Section | Parameter | Value  | Details  |
| ------------- | ------------- | ------------| ------------| 
| auth  | disable_login_form | true |  When false, the HTTP header X-Frame-Options: deny will be set in Grafana HTTP responses which will instruct browsers to not allow rendering. | 
| auth.anonymous | enabled | true | When true, users are able to view Grafana dashboards without logging-in. They are **not** able to change dashboards. |
| security | allow_embedding | true | When false, the HTTP header X-Frame-Options: deny will be set in Grafana HTTP responses which will instruct browsers to not allow rendering. |

## The Grafana API Token 
Create a [Grafana API Token](https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token). 
Note: use admin role allowing to create and update dashboards and folders.


  
### The home dashboard
* [Set the home dashboard for the server](https://grafana.com/docs/grafana/latest/administration/preferences/change-home-dashboard/) - the login process connects to the home dashboard to validate that Grafana is accessible.

    * Navigate to the dashboard you want to set as the home dashboard.
    * Click the star next to the dashboard title to mark the dashboard as a favorite if it is not already.
    * Hover your cursor over the Configuration (gear) icon.
    * Click Preferences.
    * In the Home Dashboard field, select the dashboard that you want to use for your home dashboard. Options include all starred dashboards.
    * Click Save.
    
### The default dashboard
    
## Configure the GUI 


