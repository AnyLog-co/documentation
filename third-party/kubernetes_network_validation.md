# Kubernetes Network Validation 

When using Kubernetes with multiple nodes, validating connectivity between machines (worker and/or control-plane nodes) 
is critical for diagnosing networking, DNS, or CNI plugin issues. Below are common and practical methods—suited for 
both Kubernetes experts and first-time interns—to verify node-to-node connectivity in a Kubernetes cluster.

When using Kubernetes with multiple nodes, validating connectivity between machines (worker and/or control-plane nodes) is essential for diagnosing networking, DNS, or CNI plugin issues. This guide outlines **basic network validation steps** that can be followed by both Kubernetes experts and first-time interns.

> ⚠️ These steps should be run on **two or more nodes** in parallel to verify communication between containers across 
nodes.

1. Deploy a debug Pod on each node - use simple networking images like _busybox_ or _nicolaka/netshoot_ allows to do 
basic network testing.

```yaml
# file name: network_test,yaml
apiVersion: v1
kind: Pod
metadata:
  name: net-debug
  labels:
    app: net-debug
spec:
  containers:
  - name: net-debug
    image: nicolaka/netshoot
    command: ["/bin/sh"]
    args: ["-c", "sleep infinity"]
  restartPolicy: Never
  nodeSelector:
    kubernetes.io/hostname: <NODE_NAME>
```
> Replace <NODE_NAME> with actual node hostname (you can get it with `kubectl get nodes -o wide`)

2. Deploy Pod
```shell
kubectl apply -f network_test,yaml
```

3. Attach into the Pod's shell interfaces to test
```shell
kubectl exec -it net-debug -- /bin/bash
ping <Other-Node-IP>
curl http://<Other-Pod-IP>:<Port>
```
> detach from the session without terminating the pod: Ctrl + p, then Ctrl + q.


**Notes**
* Ensure that each debug pod is scheduled on a different node. 
* If DNS resolution fails inside the pod, try testing with raw IPs first. 
* For clusters with NetworkPolicies, ensure they allow inter-pod traffic. 
* Use hostNetwork: true in the pod spec if you want to test host-level network access (not usually needed for basic checks).


