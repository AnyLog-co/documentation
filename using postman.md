# How too use Postman as the query interface
Postman is an API platform for building and using APIs. 
For AnyLog purposes, you can run queries through Postman with either SSL enabled or not. 
You can download Postman here: https://www.postman.com/downloads/.
We layout an example below for "GET" requests. 

### Without SSL
To run AnyLog queries using Postman without SSL enabled, follow the following steps:
1. Open Postman
2. Create a collection
3. Add a request
4. Enter the request URL and port number (the URL can also be an IP address)
5. Add 2 header keys: "User-Agent" and "command" with values "AnyLog/1.23" and "[query command]", respectively
![github image](https://user-images.githubusercontent.com/16313057/132929390-0f89b6c7-b88c-4665-a963-2da17645df20.png)
6. Press send, and wait for a response

### With SSL
To run AnyLog queries using Postman with SSL enabled, follow the following steps:
1. Follow steps 1-3 above
2. Enter the request URL and port number with "https://" prepended (the URL can also be an IP address)
![github image](https://user-images.githubusercontent.com/16313057/132929414-7b75bc13-4d51-4a48-b189-6a8a75e41c8f.png)
4. Add 2 header keys: "User-Agent" and "command" with values "AnyLog/1.23" and "[query command]", respectively
5. In "Settings" turn off the toggle for "Enable SSL certificate verification"
![github image](https://user-images.githubusercontent.com/16313057/132929419-282c6933-9c08-40a9-ae16-ef77224ff2fe.png)
7. In "Default Settings" add the certificate (public key) of the certificate authority
8. Add your certificate and private key pair given by the certificate authority
![github image](https://user-images.githubusercontent.com/16313057/132929434-baa81c83-2ba8-467d-8b2d-a0db12bf6544.png)
