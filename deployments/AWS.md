# AWS Setup

The following provides directions for using an EC2 AWS instance(s) to configure and deploy AnyLog.  

Directions for [deploying an AnyLog Node](deploying_node.md) 

## Create a new AWS instance
0. Create an account and/or log into [AWS](https://aws.amazon.com/) 

1. Create a [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html)

2. Create a [new security](https://docs.aws.amazon.com/vpc/latest/userguide/security-groups.html) group per node type. 

The image below, shows sample configuration for an AnyLog (Operator) node; this includes _SSH_ access, _TCP_ and _REST_, as well 
as _Broker_ if configured for Operator or Publisher node. 
* **Master Node** - Default TCP: 32048 | Default REST: 32049 
* **Query Node** - Default TCP: 32348 | Default REST: 32349
* **Remote-CLI** which usually seats on the same physical machine as the Query node requires port 31800 to be open. 
* **Operator Node** - Default TCP: 32148 | Default REST: 32149 | (Default) Broker: 32150
* **Publisher Node**: Default TCP: 32248 | Default REST: 32249 | (Default) Broker: 32250
* **Generic / REST Node**: Default TCP: 32548 | Default REST: 32549 | (Default) Broker: 32550

 
![image](../imgs/aws_sample_security_group.png)

3. Create a new EC2 instance that's associated with the corresponding _security group_.  

4. Configure a static IP address 

    a. Create an [Elastic IP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html). 
This is very important as AWS provides a new IP each time a node is rebooted.

    b. [Associate Elastic IP with Instance](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html)

5. Repeat steps 3 and 4 for each new AWS instance

If you're using a [different regions](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html) 
for your AnyLog instance, then the TCP binding needs to be enabled. 



 


