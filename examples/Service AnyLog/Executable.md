# Deploy AnyLog Executable

The following provides step-by-step directions for installing AnyLog (executable) on _Ubuntu 22.04 LTS_.    

1. Install requirements
```shell
for cmd in update upgrade ; do apt-get -y ${cmd} ; done 

sudo apt-get install -y bash git openssh-client gcc python3-dev musl-dev
sudo apt-get install -y bash python3 python3-dev python3-pip wget build-essential libffi-dev
sudo python3 -m pip install --upgrade pip

mkdir ~/AnyLog-code ; cd ~/AnyLog-code
```

2. Download and Install AnyLog / EdgeLake Python requirements 
```shell
curl https://raw.githubusercontent.com/EdgeLake/EdgeLake/main/requirements.txt -o ~/AnyLog-code/requirements.txt 
python3 -m pip install --upgrade -r ~/AnyLog-code/requirements.txt
```

3. Download AnyLog - make sure version matches with in terms of Operating System and CPU architecture  
```shell
curl http://173.255.254.34:31900/ubuntu/anylog_v1.3.2404_x86_64 -o ~/AnyLog-code/anylog_v1.3.2404_x86_64 
```

4. Download configurations file
```shell
cd ~/AnyLog-code
git clone https:///github.com/AnyLog-co/docker-compose 
```

5. Update [configuration files](https://github.com/AnyLog-co/docker-compose/tree/os-dev/docker-makefile) & export configurations. We recommend updating the following params: 
   * **base_configs.env**
     * [`LICENSE_KEY`](https://anylog.co/download-anylog/)
     * `NODE_NAME` 
     * `COMPANY_NAME`
     * `LEDGER_CONN`
   * **advance_configs.env**
     * Directories (`ANYLOG_PATH`, `LOCAL_SCRIPTS`, `TEST_DIR`) - when deploying AnyLog as executable we recommend setting 
     the path to `~/AnyLog-code` 
     * `DISABLE_CLI` to _true_ if planned to [run in background](Service.md)
```shell
while IFS= read -r line ; do if [[ $line != \#* ]] && [[ $line != "" ]] && [[ "$line" != '=""' ]] ; then export "${line}" ; fi ; done < ~/AnyLog-code/docker-compose/docker-makefile/master-configs/base_configs.env
while IFS= read -r line ; do if [[ $line != \#* ]] && [[ $line != "" ]] && [[ "$line" != '=""' ]] ; then export "${line}" ; fi ; done < ~/AnyLog-code/docker-compose/docker-makefile/master-configs/advance_configs.env
```

6.Download Deployment scripts
```shell
cd ~/AnyLog-code
git clone https://github.com/AnyLog-co/deployment-scripts
```

7. Start AnyLog
```shell
cd ~/AnyLog-code
chmod -x anylog_v1.3.2404_x86_64
./anylog_v1.3.2404_x86_64 process deployment-scripts/node-deployment/main.al 
```
