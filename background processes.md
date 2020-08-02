# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background threads:

1. A listener for the AnyLog messaging. Activated by the command: ```run tcp server```
2. A listener for a user REST request.  Activated by the command: ```run rest server```
3. An automated Operator process. Activated by the command: ```run operator```
4. An automated Publisher process. Activated by the command: ```run publisher```
5. An automated Blockchain Synchronizer. Activated by the command: ```run blockchain sync```
6. A scheduler process. Activated by the command ```run scheduler```

