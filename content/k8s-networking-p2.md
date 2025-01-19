Title: Sharing What I've Learned About Kubernetes Networking - Part 2
Date: 2025-01-20
Category: Knowledge Base
Tags: k8s

In the second part, I will talk about Container network interface (CNI), Cilium CNI and Network policies


# CNI

### What is CNI:
- Is a framework for configuring network interfaces in Linux container , providing connectivity and ensure network isolation.
- CNI Plugin standarize and simplify Kubernetes networking.

### How CNI Works:
- CNI works by invoke network plugin that handle network configuration for containers. When a container is created, the container runtime call the CNI plugin to setup the container network interface
- Works in K8S:
```
Kube API --> Kubelet --> Container Runtime --> create container, network namespace
                                           --> invoke CNI, create network configuration for veth then map it with container network
```

### CNI specification:
- A Json configuration file that specifies the desired network setup.
- Standard commands: ADD, DEL, CHECK to manage network interfaces.
- Plugin must handle these command and return results in predefined format.

### CNI community popularity:
The following table summarizes different GitHub metrics to give you an idea of each project's popularity and activity levels. This data was collected in December 2024.


| Provider |  Stars | Forks | Contributors |
|----------| -------|-------|--------------|
| Canal    |  718   | 100   | 20           |
| Flannel  |  8.9k  | 2.9k  | 234          |
| Calico   |  6.1k  | 1.4k  | 360          |
| Weave    |  6.6k  | 672   | 84           |
| Cilium   |  20.5k | 3k    | 868          |

# Cilium CNI

# Network policies

# Conclusion

# Reference:
- [https://ranchermanager.docs.rancher.com/](https://ranchermanager.docs.rancher.com/)