# Open Horizon 

Open Horizon is a platform for managing the service software lifecycle of containerized workloads and related machine 
learning assets. It enables autonomous management of applications deployed to distributed web scale fleets of edge 
computing nodes and devices without requiring on-premise administrators.

Open Horizon can be used to easily manage and deploy AnyLog node(s) through their interface.   

* [Platform Website](https://cp-console.ieam42-edge-8e873dd4c685acf6fd2f13f4cdfb05bb-0000.us-south.containers.appdomain.cloud/edge)
* [IBM](https://developer.ibm.com/components/open-horizon/)
* [Linux Foundation](https://www.lfedge.org/projects/openhorizon/)
* [Documentation](https://open-horizon.github.io/)


## Preparing Node for using Open Horizon
1. On the node Update / Upgrade Node 
```shell
for cmd in update upgrade ; sudo apt-get -y ${cmd} ; done 
```

2. [Create API Key](https://www.ibm.com/docs/en/eam/4.3?topic=installation-creating-your-api-key)

3. Declare env variables 
```shell
export HZN_ORG_ID=<COMPANY_NAME> 


export HZN_EXCHANGE_USER_AUTH="iamapikey:<HZN_EXCHANGE_USER_AUTH>"


export HZN_EXCHANGE_URL=<HZN_EXCHANGE_URL>

export HZN_FSS_CSSURL=<HZN_EXCHANGE_URL>
```

4. Install _agent_ and provide admin privlages 
```shell
curl -u "${HZN_ORG_ID}/${HZN_EXCHANGE_USER_AUTH}" -k -o agent-install.sh ${HZN_FSS_CSSURL}/api/v1/objects/IBM/agent_files/agent-install.sh/data

chmod +x agent-install.sh

sudo -s -E ./agent-install.sh -i 'css:' -p IBM/pattern-ibm.helloworld -w '*' -T 120
```

5. Validate **helloworld** sample edge service is running 
```shell
hzn eventlog list -f

<<COMMENT  
"2022-06-13 21:27:13:   Workload service containers for IBM/ibm.helloworld are up and running."
<<COMMENT
```

At the end of the process the Open Horizon should show a new active node 
![Open Horizon node status](../../imgs/OpenHorizon_node_state.png)


