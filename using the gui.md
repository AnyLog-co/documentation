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
    
- The Grafana configuration options are explained at the [Setting](https://grafana.com/docs/grafana/latest/auth/grafana/#settings) section. Below are some relevant configurations:  

| Section | Parameter | Value  | Details  |
| ------------- | ------------- | ------------| ------------| 
| auth  | disable_login_form | false |  'true' hides the Grafana login form. | 
| auth.anonymous | enabled | true | When true, users are able to view Grafana dashboards without logging-in. They are **not** able to change dashboards. |
| security | allow_embedding | true | When false, the HTTP header X-Frame-Options: deny will be set in Grafana HTTP responses which will instruct browsers to not allow rendering. |

## The Grafana API Token 
Create a [Grafana API Token](https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token). 
Note: use admin role allowing to create and update dashboards and folders.

    
