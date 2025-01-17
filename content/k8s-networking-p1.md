Title: Sharing What I've Learned About Kubernetes Networking - Part 1
Date: 2025-01-17
Category: Knowledge Base
Tags: k8s

In the first part, I will talk about Kubernetes Service, Ingress, and Service Discovery


# Kubernetes Services
In Kubernetes, a Service is a method for exposing a network application that is running as one or more Pods in your cluster.
So how many types of Services? There are 4 types:

![2025-01-17]({static}/images/2025/01/17th_1.png)

### Service type, there is 4 type of service:

1. **ClusterIP**: Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. This is the default ServiceType ( if you don't define the type, it will be ClusterIP)

2. **NodePort**: Exposes the Service on each Node’s IP at a static port (the NodePort). A ClusterIP Service, to which the NodePort Service routes, is automatically created. You’ll be able to contact the NodePort Service, from outside the cluster, by requesting <NodeIP>:<NodePort>. Default port range: 30000-32767

3. **LoadBalancer**: Exposes the Service externally using a cloud provider’s load balancer. NodePort and ClusterIP Services, to which the external load balancer routes, are automatically created.
- If you're running Kubernetes on a cloud provider that supports load balancer services (like AWS, GCP, Azure), then type: LoadBalancer will work as expected
- If you're running Kubernetes on-premises or on a cloud provider that doesn't support load balancers, type: LoadBalancer will not work.

4. **ExternalName**: Maps the Service to the contents of the externalName field (e.g. `my.database.example.com`), by returning a CNAME record with its value.

### Let's dive deep into each section with the use case and example with the manifest so you can imagine it easily!

#### 1. **ClusterIP**: 
I assume you have redis pod already and you want to access it from backend server, backend server is in same k8s cluster
- Manifest demo:
{% highlight yaml %}
apiVersion: v1
kind: Service
metadata:
  name: redis-test-clusterip
  namespace: redis-standalone
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis-test
{% endhighlight %}

- Access it with FQDN: `redis-test-clusterip.redis-standalone.svc.cluster.local:6379`
- Explains: Fully qualified domain name (FQDN) of the Service. The FQDN takes the form `service-name.namespace.svc.cluster.local`, where:
    - `service-name` is the name of the Service.
    - `namespace-name` is the namespace in which the Service resides.
    - `svc` is a static value.
    - `cluster.local` is the default domain for the cluster. This can be customized during cluster setup.
- The DNS service in Kubernetes (like CoreDNS or kube-dns) is responsible for resolving this FQDN to the appropriate Service. When you create a Service, Kubernetes automatically creates a corresponding DNS record. This allows Pods in the cluster to access the Service using the FQDN.

#### 2. **NodePort**: 

# Reference:
- [https://kubernetes.io](https://kubernetes.io/docs/concepts/services-networking/service/)
- [https://bytebytego.com](https://bytebytego.com)