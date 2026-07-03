Title: Kustomize: Quick Introduction and Integration with Other Tools and Examples
Date: 2025-02-03
Category: Knowledge Base
Tags: k8s

Kustomize introduces a template-free way to customize application configuration that simplifies the use of off-the-shelf applications. Now, built into `kubectl` as `apply -k`.

# The feature of Kustomize you may want to hear most: Environment-specific Customization
-  It allows you to overlay configuration changes for different environments (e.g., dev, staging, production) without duplicating YAML files. Other features i don't mention in this post xD

### Example Kustomize Directory Structure
```
app/
│── base/
│   ├── deployment.yaml
│   ├── kustomization.yaml
│
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │
    ├── staging/
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │
    └── prod/
        ├── kustomization.yaml
        ├── deployment-patch.yaml
```

### Example Kustomize Configurations
- I will use Strategic Merge Patch for this example! For more examples you can take a look at refs or here: https://github.com/kubernetes-sigs/kustomize/tree/master/examples
##### **Base data:**
- `app/base/kustomization.yaml`
```yaml
resources:
  - deployment.yaml
```

- `app/base/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-registry/my-app:latest  # Image to be updated dynamically
        ports:
        - containerPort: 8080
```

##### **Dev Overlays:**
- `app/overlays/dev/kustomization.yaml`
```yaml
resources:
  - ../../base

patches:
  - path: deployment-patch.yaml
```

- `app/overlays/dev/deployment-patch.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2  # Override the base replica count for dev
```

##### **Output example:**

```yaml
# kustomize build app/overlays/dev/
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - image: my-registry/my-app:dev-latest
        name: my-app
        ports:
        - containerPort: 8080
```

##### **Rest for Prod / Staging**
- You just need to make a new file and directory in the correct folders:
```
# Prod
app/overlays/prod/deployment-patch.yaml
app/overlays/prod/kustomization.yaml
# Staging
app/overlays/staging/deployment-patch.yaml
app/overlays/staging/kustomization.yaml
```
- So you don't need to duplicate your manifest.
- The configuration is easier to modify for each environment.

# It seems clean but is it useable, any examples?
Yes, Deploy with ArgoCD. Here is an example
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/my-org/my-gitops-repo.git
    targetRevision: main
    path: app/overlays/dev  # Change to staging/prod for other envs
  destination:
    server: https://kubernetes.default.svc
    namespace: my-namespace
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

# Oh, I see, but how do you generate those manifests in kustomize format? Don't tell me that you are doing them manually.
### Here are some ways to generate them:
- Using kubectl Commands:
```
kubectl create deployment my-app --image=my-image --dry-run=client -o yaml > base/deployment.yaml
kubectl create service clusterip my-app --tcp=80:80 --dry-run=client -o yaml > base/service.yaml
```
- Bash script (this sucks xD):
```yaml
# Create Base Deployment
cat <<EOF > $MANIFESTS_DIR/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-registry/my-app:latest
        ports:
        - containerPort: 8080
EOF
```
- To be honest, they are only visible for simple applications, for complex applications you may want to use [jsonnet](https://github.com/google/jsonnet). I will write a post for the `jsonnet` tutorial later if i have enough time and knowledge.

# Validator
- Some good uses of kustomize are to validate yaml and make sure they are in a good format before applying them into the k8s cluster (although there are too many ways to do this xD)
- Example manifest error:
```
resources:
  - ../../base

patches:
  - path: deployment-patch.yaml
szdas
```
- Validate: 
```
kustomize build app/overlays/dev/
Error: invalid Kustomization: yaml: line 7: could not find expected ':'
```

# Conclusion:
- For more details and a completed tutorial, please visit those links in `Ref`.
- Kustomize is a great to to avoid duplicates in the yaml manifest.
- It can be combined with other tools like Helm and ArgoCD to make GitOps deployment.
- This post is a place i saved my learning progress to not forget easily.

# Ref
- [https://kustomize.io/](https://kustomize.io/)
- [https://github.com/kubernetes-sigs/kustomize/tree/master](https://github.com/kubernetes-sigs/kustomize/tree/master)
- [https://www.densify.com/kubernetes-tools/kustomize/](https://www.densify.com/kubernetes-tools/kustomize/)
- [https://glasskube.dev/blog/patching-with-kustomize/](https://glasskube.dev/blog/patching-with-kustomize/)
- [https://chatgpt.com/](https://chatgpt.com/) xDD
