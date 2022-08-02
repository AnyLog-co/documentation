The following table provides insight into the different (ENV) configuration options.  

<table>
    <tr>
        <th>Section</th>
        <th>ENV Param</th>
        <th>AnyLog Param</th>
        <th>Description</th>
        <th>Options</th>
        <th>Default</th>
    </tr>
    <tr>
        <td>General</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>NODE_TYPE</td>
        <td>Based on the node type each of the params listed below is set to either True or False.  
            <ul>
                <li><code>deploy_ledger</code></li>
                <li><code>deploy_operator</code></li>
                <li><code>deploy_publisher</code></li>
                <li><code>deploy_query</code></li>
            </ul>
        </td>
        <td>Type of AnyLog node to deploy</td>
        <td>
            <ul>
                <li><code>rest</code> -- A node that's running only TCP & REST, thus can act a testbed for playing/understanding AnyLog</li>
                <li><code>master</code> -- An alternative to blockchain, utilizing a local database to act as blockchain</li>
                <li><code>operator</code> -- Node where data will ultimatly be stored</li>
                <li><code>publisher</code> -- Node used to distribute data among opertor nodes</li>
                <li><code>query</code> -- Node dedicated to querying data</li>
                <li><code>standalone</code> -- A combination of <i>master</i> & <i>operator</i> on a single AnyLog node</li>
                <li><code>standalone-publisher</code> -- A combination of <i>master</i> & <i>publisher</i> on a single AnyLog node</li>
            </ul>
        </td>
        <td>rest</td>
    </tr>
    <tr>
        <td></td>
        <td>NODE_NAME</td>
        <td>node_name</td>
        <td>Node name</td>
        <td></td>
        <td>anylog-node</td>
    </tr>
    <tr>
        <td></td>
        <td>COMPANY_NAME</td>
        <td>company_name</td>
        <td>Company correlated to the AnyLog node</td>
        <td></td>
        <td>New company</td>
    </tr>
    <tr>
        <td></td>
        <td>LOCATION</td>
        <td>loc</td>
        <td>location of the node</td>
        <td></td>
        <td>If user doesn't specify location, then use <a herf="https://ipinfo.io" target="_blank">https://ipinfo.io</a> 
            to get location. If that fails, then set location to <code>0.0, 0.0</code>. 
            <a herf="https://ipinfo.io" target="_blank">ipinfo.io</a> also provides information about:
            <ul>
                <li>country</li>
                <li>state</li>
                <li>city</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td></td>
        <td>COUNTRY</td>
        <td>country</td>
        <td>country where node is located</td>
        <td></td>
        <td>Unknown</td>
    </tr>
    <tr>
        <td></td>
        <td>STATE</td>
        <td>state</td>
        <td>state where node is located</td>
        <td></td>
        <td>Unknown</td>
    </tr>
    <tr>
        <td></td>
        <td>CITY</td>
        <td>city</td>
        <td>city where node is located</td>
        <td></td>
        <td>Unknown</td>
    </tr>
    <tr>
        <td>Authentication</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>AUTHENTICATION</td>
        <td>authentication</td>
        <td>Whether to enable authentication</td>
        <td></td>
        <td>false</td>
    </tr>
    <tr>
        <td></td>
        <td>USERNAME</td>
        <td>username</td>
        <td>Authentication username</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>PASSWORD</td>
        <td>password</td>
        <td>Authentication password</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>AUTH_TYPE</td>
        <td>auth_type</td>
        <td>Authentication type</td>
        <td>
            <ul>
                <li><code>admin</code></li>
                <li><code>user</code></li> 
            </ul>
        </td>
        <td>admin</td>
    </tr>
    <tr>
        <td>Networking</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>ANYLOG_SERVER_PORT</td>
        <td>anylog_server_port</td>
        <td></td>
        <td>AnyLog server port</td>
        <td>32048</td>
    </tr>
    <tr>
        <td></td>
        <td>ANYLOG_REST_PORT</td>
        <td>anylog_rest_port</td>
        <td></td>
        <td>AnyLog rest port</td>
        <td>32049</td>
    </tr>
    <tr>
        <td></td>
        <td>ANYLOG_BROKER_PORT</td>
        <td>anylog_broker_port</td>
        <td></td>
        <td>AnyLog broker port - by default AnyLog doesn't run a broker, unless value is set by user</td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>EXTERNAL_IP</td>
        <td>external_ip</td>
        <td>External IP address</td>
        <td></td>
        <td>System configured IP address</td>
    </tr>
    <tr>
        <td></td>
        <td>LOCAL_IP</td>
        <td>ip</td>
        <td>Local IP address</td>
        <td></td>
        <td>System configured IP address</td>
    </tr>
    <tr>
    <tr>
        <td>Blockchain</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>LEDGER_CONN</td>
        <td>ledger_conn</td>
        <td>Ledger connection information, for a blockchain sync. In certain documents, the variable is called <code>!master_node</code></td>
        <td></td>
        <td><code>!ip:!anylog_server_port</code></td>
    </tr>
    <tr>
        <td></td>
        <td>SYNC_TIME</td>
        <td>sync_time</td>
        <td>How often to sync with the ledger</td>
        <td></td>
        <td>30 seconds</td>
    </tr>
    <tr>
        <td></td>
        <td>SOURCE</td>
        <td>blockchain_source</td>
        <td>location of the source of data</td>
        <td>
            <ul>
                <li>master</li>
                <li>ethereum</li>
            </ul>
        </td>
        <td>master</td>
    </tr>
    <tr>
        <td></td>
        <td>BLOCKCHAIN_DESTINATION</td>
        <td>blockchain_destination</td>
        <td>location where the copy of the blockchain is stored</td>
        <td>
            <ul>
                <li>file</li>
                <li>database</li>
            </ul>
        </td>
        <td>file</td>
    </tr>
    <tr>
        <td>Database</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>DB_TYPE</td>
        <td>db_type</td>
        <td>Physical database type</td>
        <td></td>
        <td>sqlite</td>
    </tr>
    <tr>
        <td></td>
        <td>DB_USER</td>
        <td>db_user</td>
        <td>database user name</td>
        <td></td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>DB_PASSWD</td>
        <td>db_passwd</td>
        <td>database password correlated to user</td>
        <td></td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>DB_IP</td>
        <td>db_ip</td>
        <td>IP address of database</td>
        <td></td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>DB_PORT</td>
        <td>db_port</td>
        <td>Port number of database</td>
        <td></td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>DEFAULT_DBMS</td>
        <td>default_dbms</td>
        <td>Logical database for <i>operator node</i></td>
        <td></td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>DEPLOY_SYSTEM_QUERY</td>
        <td>deploy_system_query</td>
        <td>Whether or not to enable the <code>system_query</code> database for allowing to query data on other nodes on the enabled node</td>
        <td></td>
        <td>false for all except <i>Query Node</i></td>
    </tr>
    <tr>
        <td></td>
        <td>MEMORY</td>
        <td>memory</td>
        <td>Run <i>system_query</i> logical database against SQLite in Memory</td>
        <td></td>
        <td>false</td>
    </tr>
    <tr>
        <td>Operator Specific</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>CLUSTER_NAME</td>
        <td>cluster_name</td>
        <td>Cluster Name</td>
        <td></td>
        <td>new-cluster</td>
    </tr>
    <tr>
        <td></td>
        <td>MEMBER</td>
        <td>member</td>
        <td>Member ID of operator</td>
        <td></td>
        <td>N/a</td>
    </tr>
    <tr>
        <td></td>
        <td>ENABLE_PARTITIONS</td>
        <td>enable_partitions</td>
        <td>Whether or not to enable partitions</td>
        <td></td>
        <td>false</td>
    </tr>
    <tr>
        <td></td>
        <td>TABLE_NAME</td>
        <td>table_name</td>
        <td>Logical table(s) to partition</td>
        <td></td>
        <td>all tables (*)</td>
    </tr>
    <tr>
        <td></td>
        <td>PARTITION_COLUMN</td>
        <td>partition_column</td>
        <td>Timestamp column to partition by</td>
        <td></td>
        <td>insert_timestamp</td>
    </tr>
    <tr>
        <td></td>
        <td>PARTITION_INTERVAL</td>
        <td>partition_interval</td>
        <td>Interval to partition by</td>
        <td>
            <ul>
                <li>hour</li>
                <li>day</li>
                <li>month</li>
            </ul>
        </td>
        <td>14 days</td>
    </tr>
    <tr>
        <td></td>
        <td>PARTITION_KEEP</td>
        <td>partition_keep</td>
        <td>How many sets of intervals to keep</td>
        <td></td>
        <td>6</td>
    </tr>
    <tr>
        <td></td>
        <td>PARTITION_SYNC</td>
        <td>partiton_sync</td>
        <td>How often to remove the oldest partition(s)</td>
        <td>
            <ul>
                <li>hour</li>
                <li>day</li>
                <li>month</li>
            </ul>
        </td>
        <td>1 day</td>
    </tr>
    <tr>
        <td><code>run operator</code> / <code>run publisher</code> params </td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>ARCHIVE</td>
        <td>archive</td>
        <td>Whether to move JSON file(s) to archive</td>
        <td></td>
        <td>true</td>
    </tr>
    <tr>
        <td></td>
        <td>COMPRESS_FILE</td>
        <td>compress_file</td>
        <td>Compress JSON / SQL file(s)</td>
        <td></td>
        <td>true</td>
    </tr>
    <tr>
        <td></td>
        <td>CREATE_TABLE</td>
        <td>create_table</td>
        <td>Based on the JSON file create new table(s)</td>
        <td></td>
        <td>true</td>
    </tr>
    <tr>
        <td></td>
        <td>UPDATE_TSD_INFO</td>
        <td>update_tsd_info</td>
        <td>Update table <code>almgm.tsd_info</code> with information JSON file stored in operator</td>
        <td></td>
        <td>true</td>
    </tr>
    <tr>
        <td></td>
        <td>DBMS_FILE_LOCATION</td>
        <td>dbms_file_location</td>
        <td>The location of a logical database based on the file name.<br/> 
            Given a sample file: <code>{DB_NAME}.{FILE_NAME}.0.json</code>, the logical database is located at 0</td>
        <td></td>
        <td>0</td>
    </tr>
    <tr>
        <td></td>
        <td>TABLE_FILE_LOCATION</td>
        <td>table_file_location</td>
        <td>The location of a the actual table where the content will be stored, based on the file name. <br/> 
            Given a sample file: <code>{DB_NAME}.{FILE_NAME}.0.json</code>, the table name is located at 1</td>
        <td></td>
        <td>1</td>
    </tr>
    <tr>
        <td>Other Settings</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>WRITE_IMMEDIATE</td>
        <td>write_immediate</td>
        <td>Whether to store / send JSON as it comes in rather than wait</td>
        <td></td>
        <td>true</td>
    </tr>
    <tr>
        <td></td>
        <td>THRESHOLD_TIME</td>
        <td>threshold_time</td>
        <td>How often to push data forward</td>
        <td>
            <ul>
                <li>seconds</li>
                <li>minute</li>
                <li>hour</li>
                <li>day</li>
            </ul>
        </td>
        <td>60 seconds</td>
    </tr>
    <tr>
        <td></td>
        <td>THRESHOLD_VOLUME</td>
        <td>threshold_volume</td>
        <td>If volume size surpasses value, then push data forward ("overriding" wait time)</td>
        <td>
            <ul>
                <li>KB</li>
                <li>MB</li>
                <li>GB</li>
            </ul>
        </td>
        <td>10 KB</td>
    </tr>
    <tr>
        <td></td>
        <td>TCP_THREAD_POOL</td>
        <td>tcp_thread_pool</td>
        <td>Number of workers threads that process requests which are send to the provided IP and Port.</td>
        <td></td>
        <td>6</td>
    </tr>
    <tr>
        <td></td>
        <td>REST_TIMEOUT</td>
        <td>rest_timeout</td>
        <td>Amount of time (in seconds) until REST timesout</td>
        <td></td>
        <td>30</td>
    </tr>
    <tr>
        <td></td>
        <td>REST_THREADS</td>
        <td>rest_threads</td>
        <td>number of concurrent threads supporting HTTP requests</td>
        <td></td>
        <td>5</td>
    </tr>
    <tr>
        <td></td>
        <td>QUERY_POOL</td>
        <td>query_pool</td>
        <td>number of threads supporting queries</td>
        <td></td>
        <td>3</td>
    </tr>
</table>

**Keys**
* ENV Param - Docker / Kubernetes environment parameter name 
* AnyLog Param - AnyLog parameter correlated to the ENV parameter 
* Description -  Description of the parameter 
* Options - ENV param options 
* Default - Default value in AnyLog 

 