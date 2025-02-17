Title: Getting Started with Helm Templates: A Practical Guide to Kubernetes Manifests
Date: 2025-02-06
Category: Knowledge Base
Tags: k8s, helm


# Introduction to Helm Templates

Helm Templates generate manifest files, which are YAML-formatted resource descriptions that Kubernetes can understand.

Helm benefits:

- Faster Debugging – Renders Helm charts locally without deploying them to Kubernetes, allowing you to inspect the final YAML output before applying it.
- GitOps Friendly – Enables storing fully rendered Kubernetes manifests in Git for version control and auditing.
- Troubleshooting – Assists in debugging templates before deploying to detect syntax or logic errors.

---

# Basic Helm Template Structure

### **1. Describe the structure of a Helm chart**

A Helm chart is a collection of files that describe a Kubernetes application. The structure of a Helm chart typically looks like this:

```perl
my-chart/
│── charts/               # Subcharts (dependencies) can be placed here
│── templates/            # Contains Helm template files
│   ├── deployment.yaml   # Kubernetes Deployment manifest template
│   ├── service.yaml      # Kubernetes Service manifest template
│   ├── ingress.yaml      # Ingress manifest template (if needed)
│   ├── _helpers.tpl      # Helper functions (e.g., common labels, annotations)
│   ├── NOTES.txt         # Post-installation usage instructions
│   ├── hpa.yaml          # Horizontal Pod Autoscaler template (optional)
│   ├── configmap.yaml    # ConfigMap template (optional)
│   ├── secret.yaml       # Secret template (optional)
│── values.yaml           # Default values for the chart
│── Chart.yaml            # Metadata about the chart (name, version, description)
│── README.md             # Documentation for using the chart
│── .helmignore           # Files to ignore when packaging the chart
```

### **2. Purpose of the templates/ Directory**
The templates/ directory contains the Kubernetes resource templates that Helm will process before deploying. These files are written in YAML but use Go templating (`{{ ... }}`) to inject dynamic values

### **3. Common Template Files**
`deployment.yaml`:

- Defines the Deployment resource, which manages the application pods.
- Uses Helm template syntax to allow customization of replicas, container images, environment variables, etc
- Example snippet:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: {{ .Release.Name }}
spec:
replicas: {{ .Values.replicaCount }}
template:
    spec:
    containers:
        - name: my-app
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

`service.yaml`:

- Defines a Service resource to expose the application internally or externally.
- Example snippet:
```yaml
apiVersion: v1
kind: Service
metadata:
name: {{ .Release.Name }}
spec:
type: {{ .Values.service.type }}
ports:
    - port: {{ .Values.service.port }}
    targetPort: {{ .Values.service.targetPort }}
```

`_helpers.tpl`: is a template helper file in a Helm chart.

- Contains reusable template functions like common labels, annotations, and naming conventions.
- These functions help reduce redundancy and improve maintainability by allowing you to reuse common labels, names, and other template logic across multiple YAML manifests
- Defining Common Labels:
    - This defines a reusable function `"common.labels"` for setting Kubernetes labels.
    - The `Chart.Name` and `Release.Name` values are dynamically inserted.
```yaml
{{- define "common.labels" -}}
app-common: {{ .Chart.Name }}
release-common: {{ .Release.Name }}
chart-common: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end }}
```
- Using `_helpers.tpl` in `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: {{ .Release.Name }}
labels:
    {{- include "common.labels" . | nindent 4 }}
spec:
replicas: {{ .Values.replicaCount }}
template:
    metadata:
    labels:
        {{- include "common.labels" . | nindent 8 }}
```
- Output Example after using the template:
```yaml
# Source: app-demo/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: release-name-app-demo
labels:
    helm.sh/chart: app-demo-0.1.0
    app.kubernetes.io/name: app-demo
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.16.0"
    app.kubernetes.io/managed-by: Helm
    app-common: app-demo
    release-common: release-name
    chart-common: app-demo-0.1.0
spec:
replicas: 1
selector:
    matchLabels:
    app.kubernetes.io/name: app-demo
    app.kubernetes.io/instance: release-name
template:
    metadata:
    labels:
        helm.sh/chart: app-demo-0.1.0
        app.kubernetes.io/name: app-demo
        app.kubernetes.io/instance: release-name
        app.kubernetes.io/version: "1.16.0"
        app.kubernetes.io/managed-by: Helm
        app-common: app-demo
        release-common: release-name
        chart-common: app-demo-0.1.0
    spec:
    serviceAccountName: release-name-app-demo
    securityContext:
```

`NOTES.txt`: 

- Provides post-installation instructions to the user after running commands, which means it will show the content of `NOTES.txt`.
```
helm install app-demo app-demo/
helm status app-demo
```

- Example:
```plain
### helm install app-demo app-demo/
NAME: app-demo
LAST DEPLOYED: Tue Feb  4 23:56:48 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands: OK BRO ( this is edit for testing xD)
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=app-demo,app.kubernetes.io/instance=app-demo" -o jsonpath="{.items[0].metadata.name}")
..... and for the rest of file notes.txt ....
```
---

# **Go Templating in Helm: Basic Syntax, Variables, and Common Functions**

Helm templates use **Go templating language**, which provides powerful features like **variables, functions, loops, and conditionals** to dynamically generate Kubernetes manifests.

### **1. Basic Syntax**
Helm templates use **`{{ ... }}`** to enclose Go template expressions.

A template file can include:

  - **Variables**: Store and reuse values.
  - **Conditionals**: `if`, `else`, `with`.
  - **Loops**: `range` for iterating over lists or maps.
  - **Functions**: Modify values dynamically.

Example:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount | default 1 }}
```
- `.Release.Name` = Helm release name.
- `.Values.replicaCount | default 1` = Use `.Values.replicaCount`, or default to `1`.

---

### **2. Variables**
**Defining Variables**

- Use `{{ $var := value }}` to define a variable.
```yaml
{{- $appName := .Chart.Name }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ $appName }}
```
- `$appName` stores `.Chart.Name` and is reused later.

**Built-in Variables**

| Variable | Description |
|----------|------------|
| `.Release.Name` | The name of the Helm release |
| `.Chart.Name` | The name of the chart |
| `.Chart.Version` | The version of the chart |
| `.Values` | Access values from `values.yaml` |
| `.Files` | Access files inside `chart/templates` |
| `.Capabilities` | Kubernetes API version detection |

---

### **3. Common Functions**
Helm provides several built-in functions.

**(A) `default` – Provide a Default Value**
```yaml
replicas: {{ .Values.replicaCount | default 2 }}
```
- If `replicaCount` is **not set**, it defaults to `2`.

---

**(B) `include` – Reuse Other Templates**
The `include` function allows you to reuse defined templates from `_helpers.tpl`.

- **Example: Defining a helper in `_helpers.tpl`**
```yaml
{{- define "common.labels" -}}
app: {{ .Chart.Name }}
release: {{ .Release.Name }}
{{- end }}
```
- **Using it in `deployment.yaml`**
```yaml
metadata:
  labels:
    {{- include "common.labels" . | nindent 4 }}
```
- `include "common.labels" .` injects the labels from `_helpers.tpl`.
- `nindent 4` ensures proper YAML indentation.

---

**(C) `tpl` – Render Strings as Templates**
The `tpl` function processes dynamic content inside values.

- **Example in `values.yaml`**
```yaml
customMessage: "Welcome to {{ .Release.Name }}!"
```
- **Using it in `configmap.yaml`**
```yaml
data:
  message: {{ tpl .Values.customMessage . }}
```
- `tpl` evaluates `{{ .Release.Name }}` **inside** the string from `values.yaml`.

---

**(D) `toYaml` – Convert Objects to YAML**
Use `toYaml` when dealing with structured values.

- **Example in `values.yaml`**
```yaml
envVars:
  - name: ENV1
    value: "value1"
  - name: ENV2
    value: "value2"
```
- **Using it in `deployment.yaml`**
```yaml
env:
{{- toYaml .Values.envVars | nindent 4 }}
```
- `toYaml` converts the YAML list into properly formatted output.

---

**(E) `quote` and `nquote` – Handle Strings Properly**
- `quote` wraps values in **double quotes**.
- `nquote` removes surrounding quotes.

Example:
```yaml
env:
  API_URL: {{ .Values.apiUrl | quote }}
```
For:
```yaml
apiUrl: http://example.com
```
It renders:
```yaml
env:
  API_URL: "http://example.com"
```

---

**(F) `required` – Ensure a Value is Set**
If a value is missing, `required` returns an error.

Example:
```yaml
image: {{ required "An image repository is required!" .Values.image.repository }}
```
If `.Values.image.repository` is missing, Helm will **fail** with:
```
Error: template: missing required value: An image repository is required!
```

---

### **4. Conditionals (`if`, `else`, `with`)**
**(A) `if` Statement**
```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}
{{- end }}
```
- If `ingress.enabled` is `true`, this block is included.

---

**(B) `else` Statement**
```yaml
replicas: 
{{- if .Values.replicaCount }}
  {{ .Values.replicaCount }}
{{- else }}
  1
{{- end }}
```
- If `replicaCount` exists, it uses the value; otherwise, it defaults to `1`.

---

**(C) `with` Statement (Scoped Variables)**
`with` changes the scope to a nested value.
```yaml
{{- with .Values.service }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .name }}
  ports:
    - port: {{ .port }}
{{- end }}
```
Instead of writing `.Values.service.name` and `.Values.service.port`, we **scope** it under `with`.

---

### **5. Loops (`range`)**
**(A) Loop Over a List**
```yaml
containers:
  {{- range .Values.containers }}
  - name: {{ .name }}
    image: {{ .image }}
  {{- end }}
```
For:
```yaml
containers:
  - name: "app1"
    image: "nginx"
  - name: "app2"
    image: "redis"
```
It renders:
```yaml
containers:
  - name: "app1"
    image: "nginx"
  - name: "app2"
    image: "redis"
```

---

**(B) Loop Over a Dictionary**
```yaml
config:
  {{- range $key, $value := .Values.config }}
  {{ $key }}: {{ $value }}
  {{- end }}
```
For:
```yaml
config:
  LOG_LEVEL: "debug"
  ENV: "production"
```
It renders:
```yaml
config:
  LOG_LEVEL: debug
  ENV: production
```

- In this case `toYaml` works well also xD

---


# Useful commands for developing templates
- Show the template of the specific file only:
```
helm template . --show-only templates/service.yaml
```
- Check templates/manifest error:
```
helm lint
```

# Helm template repo:
- [https://github.com/BlackMetalz/k8s-manifest/tree/main/helm-templates/templates](https://github.com/BlackMetalz/k8s-manifest/tree/main/helm-templates/templates)
- Include some examples with configMap, namespace, secret...
- Examples can be found in [values.yaml](https://github.com/BlackMetalz/k8s-manifest/blob/main/helm-templates/values.yaml)

# Use case with helm templates
Well, we can do a lot of things with helm templates.

Use scenarios: Become a  general template of all helm applications - Each values file is an application in an environment
- Each values file is a application in an environment
```perl
k8s-manifest/
├── helm-templates/
│   ├── ... (other files)
├── helm-services/
│   ├── group1/
│   │   ├── service1.yaml
│   │   ├── service2.yaml
│   ├── group2/
│       ├── notification.yaml
│       ├── api.yaml
```
- You get the idea, right? Next is the Argocd application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-name-here
  namespace: argocd
spec:
  project: development_or_production
  source:
    repoURL: https://github.com/BlackMetalz/k8s-manifest
    targetRevision: main
    path: helm-templates/
    plugin:
      name: argocd-vault-plugin-helm
      env:
        - name: HELM_ARGS
          value: -f /helm-services/group1/service1.yaml
  destination:
    server: which_server_here
    namespace: namespace_here
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```
- With this, we can do a lot of custom modifications to the manifest without manually changing too much. That is why i think helm templates rock and are easier to begin with than jsonnet xD

# Ref
- https://helm.sh/docs/chart_template_guide/
- https://www.xenonstack.com/blog/helm-kubernetes/