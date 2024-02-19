The following is used for AnyLog [Deployment-Console](https://github.com/AnyLog-co/Deployment-Console)
## Configure Grafana
Change the following configuration options in the .ini configuration file:
Notes: 
- You must restart Grafana for any configuration changes to take effect.
- Optional locations for the Grafana .ini file:
  * Winodws Config: `C:\Program Files\GrafanaLabs\grafana\conf\custom.ini`
  * Linux Config: `/etc/grafana/grafana.ini`
  * With Docker, the Grafana config file name is `grafana.ini`. Depending on the deployment, the file is stored in the Docker volume (if created); or optionally is a hidden file.
    Details are available in the [Grafana Docker Documentation](https://grafana.com/docs/grafana/latest/installation/docker/).
    
- The Grafana configuration options are explained at the [Setting](https://grafana.com/docs/grafana/latest/auth/grafana/#settings) section. Below are some relevant configurations:  

| Section | Parameter | Value  | Details  |
| ------------- | ------------- | ------------| ------------| 
| auth  | disable_login_form | false |  'true' hides the Grafana login form. | 
| auth.anonymous | enabled | true | When true, users are able to view Grafana dashboards without logging-in. They are **not** able to change dashboards. |
| security | allow_embedding | true | When false, the HTTP header X-Frame-Options: deny will be set in Grafana HTTP responses which will instruct browsers to not allow rendering. |

## The Grafana API Token 
Create a [Grafana API Token](https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token). 
