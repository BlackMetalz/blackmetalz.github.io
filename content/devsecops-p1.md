Title: Practical DevSecOps: Securing the Pipeline from Code to Deployment - Part 1
Date: 2025-02-10
Category: Knowledge Base
Tags: devsecops

### This series will contain 3 parts:
- Part 1. Secure Coding Practices: Tools and Techniques for DevSecOps. (**We are here!**)
- Part 2. Hardening and Monitoring: Benchmarking and Runtime Security in DevSecOps.
- Part 3. Automating Security: Integrating DevSecOps into CI/CD with Jenkins.


# Introduction to DevSecOps

DevSecOps is an approach that integrates security practices within the DevOps process. It involves:

- **Security Integration**: Embedding security throughout the entire development lifecycle
- **Automation**: Implementing security controls and tests automatically
- **Collaboration**: Fostering cooperation between development, operations, and security teams
- **Continuous Security**: Making security a continuous process rather than an afterthought

The main goal is to deliver secure applications without compromising development speed by:

1. Incorporating security testing in CI/CD pipelines
2. Automating security gates and controls
3. Using infrastructure as code with security policies
4. Implementing continuous security monitoring
5. Managing vulnerabilities throughout the application lifecycle

This approach ensures that security is not a bottleneck but rather an integrated part of the development process.

# Component in this Part
1. Talisman
2. Mutation Testing:
    - PIT (PITest) for Java
    - Mutmut for Python
    - Gremlins for Golang
3. Sonarqube
4. Dependency Checks

---
# 1. Talisman
Talisman is a tool that scans git changesets to ensure that potential secrets or sensitive information do not leave the developer's workstation.

### Why should we use Talisman?

- Let me give you an example, [**Dev put AWS keys on Github. Then BAD THINGS happened**](https://www.theregister.com/2015/01/06/dev_blunder_shows_github_crawling_with_keyslurping_bots/)


- There are 2 things that happen in this scenario:
    - Dev pushed Amazon S3 keys to Github account.
    - Hackers use Amazon S3 keys to create 140 servers for Bitcoin to farm itself.

- I think you will be curious why it is only an S3 key but Hackers are able to create new EC2 instances, i bet there are some misconfigured for IAM Policies like this:
```yaml
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

The first one can be avoided if we use Talisman. Pre-commit / Pre-push hooks can be installed on the developer's workstations to avoid them (They can bypass this step also). We are all human and errors are hard to avoid, that is why we should use tools/policies to recheck if we are doing wrong xD.

### Install
- Visit [https://thoughtworks.github.io/talisman/docs/installation](https://thoughtworks.github.io/talisman/docs/installation) 
- For a demo, i will install only for a Single Project
```bash
# Download the talisman binary
curl https://thoughtworks.github.io/talisman/install.sh > ~/install-talisman.sh
chmod +x ~/install-talisman.sh
# Install to a single project (as pre-push hook)
cd my-git-project
~/install-talisman.sh
```
- Output expected:
```bash
Downloading talisman_linux_amd64 from https://github.com/thoughtworks/talisman/releases/download/v1.32.0/talisman_linux_amd64
Downloading checksums from https://github.com/thoughtworks/talisman/releases/download/v1.32.0/checksums
talisman_linux_amd64: OK

Talisman successfully installed to '.git/hooks/pre-push'.
```

### Usage
- Here is small a demo with Golang: [demo-repo](https://gist.github.com/BlackMetalz/08ec9f3e985c7796f65ae36b06004f35)
- What happens when i try to push?

```bash
# git add .
# git commit -m "init"
[main 92047ab] init
 1 file changed, 25 insertions(+)
 create mode 100644 main.go
# git push
Welcome to Kienlt Gitlab
Talisman Scan: 3 / 3 <---------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%  

Talisman Report:
+---------+------------------------------------------------------+----------+
|  FILE   |                        ERRORS                        | SEVERITY |
+---------+------------------------------------------------------+----------+
| main.go | Expected file to not contain                         | high     |
|         | base64 encoded texts such as:                        |          |
|         | "kG1234abcd5678efgh90ijklmnop12345678ABCD"           |          |
+---------+------------------------------------------------------+----------+
| main.go | Expected file to not contain                         | high     |
|         | base64 encoded texts such as:                        |          |
|         | "sk_test_51ABCDEfghiJKLMNOpqrsTUVW"                  |          |
+---------+------------------------------------------------------+----------+
| main.go | Expected file to not contain                         | high     |
|         | base64 encoded texts such as:                        |          |
|         | "ghp_ABC123DEF456GHI789JKLmnopqrstuvwxyz"            |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern                             | low      |
|         | :     AWS_ACCESS_KEY =                               |          |
|         | "AKIA4XXXXXXXXXXXXXXXXX"                             |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern                             | low      |
|         | :     AWS_SECRET_KEY =                               |          |
|         | "kG1234abcd5678efgh90ijklmnop12345678ABCD"           |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern                             | low      |
|         | :     DB_PASSWORD =                                  |          |
|         | "sup3r_s3cr3t_p@ssw0rd"                              |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern :     DB_CONNECTION =       | low      |
|         | "postgresql://admin:password123@localhost:5432/mydb" |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern                             | low      |
|         | :     STRIPE_SECRET_KEY =                            |          |
|         | "sk_test_51ABCDEfghiJKLMNOpqrsTUVW"                  |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern :                           | high     |
|         | AWS_ACCESS_KEY =                                     |          |
+---------+------------------------------------------------------+----------+
| main.go | Potential secret pattern :                           | high     |
|         | AWS_SECRET_KEY =                                     |          |
+---------+------------------------------------------------------+----------+


If you are absolutely sure that you want to ignore the above files from talisman detectors, consider pasting the following format in .talismanrc file in the project root

fileignoreconfig:
- filename: main.go
  checksum: 9676d51e34a4b78de22369c9cd8febf8e820f0ae13999b36a5b0b550dde223ca
version: ""

Talisman done in 40.339315ms
error: failed to push some refs to 'ssh://git.kienlt.local:22/kienlt/talisman-test.git'
```

- It works as expected, the secrets are not able to push. And it even tells us how to ignore them if they are not secret xD

---
# 2. Mutation Testing
Mutation testing is essentially a way of testing your unit tests. By introducing small changes (mutations) to your source code and running your unit tests against these modified versions, you can verify if your tests are capable of catching the errors. If your unit tests detect and fail on these mutations, it indicates that your tests are robust and effective. If not, it suggests that your tests might need improvement

Since there is no framework for multiple languages, i will try to go one by one with Python explain since I'm confident with it most. Hope it will not be too longs xD

### Little explains:

1. Mutation testing works by:
    - Making small changes (mutations) to your source code
    - Running your test suite against each mutation
    - Checking if the tests fail (mutation killed) or pass (mutation survived)

2. Without tests:
    - There's nothing to verify if the mutations break the code
    - The tool can't determine if a mutation was "killed" or "survived"
    - There's no way to calculate mutation coverage

### 2.1. Golang
- Repo: [https://github.com/BlackMetalz/mutation-testing-golang](https://github.com/BlackMetalz/mutation-testing-golang)

### 2.2. Java
- Repo: [https://github.com/BlackMetalz/mutation-testing-Java](https://github.com/BlackMetalz/mutation-testing-Java)

### 2.3. Python
- Repo: [https://github.com/BlackMetalz/mutation-testing-python](https://github.com/BlackMetalz/mutation-testing-python)
- You may want to read the repo first, below is just a highlight of how mutation testing works.
- Create simple function `calculator.py`:
```python
def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    return a - b

def multiply(a: int, b: int) -> int:
    return a * b

def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```
- Create a simple test: `calculator_test.py`:
```
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(6, 2) == 3.0
    assert divide(5, 2) == 2.5
    # This will raise a survivor in mutation testing
    """
    with pytest.raises(ValueError):
        divide(1, 0)
    """
    # This will not raise a survivor in mutation testing
    # Test division by zero error message explicitly
    try:
        divide(1, 0)
        pytest.fail("Expected ValueError")  # Should not reach this line
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"
```

- Output example:
```
- Mutation testing starting -

These are the steps:
1. A full test suite run will be made to make sure we
   can run the tests successfully and we know how long
   it takes (to detect infinite loops for example)
2. Mutants will be generated and checked

Results are stored in .mutmut-cache.
Print found mutants with `mutmut results`.

Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.
🙁 Survived.         This means your tests need to be expanded.
🔇 Skipped.          Skipped.

mutmut cache is out of date, clearing it...
1. Running tests without mutations
⠴ Running...Done

2. Checking mutants
⠋ 7/7  🎉 7  ⏰ 0  🤔 0  🙁 0  🔇 0
```

---
# 3. Sonarqube
- Is a Static Application Security Testing

### Purpose:
- SonarQube is a continuous code quality and security tool that performs static code analysis.
- It helps to detect code smells, bugs, security vulnerabilities, and duplications in your codebase.

### How it Works:
- SonarQube analyzes the source code without executing it
- It uses various rules and patterns to identify issues in the code.
- The analysis results are displayed on a dashboard, providing a clear overview of the code quality

### Metrics:
- Code Smells: Maintainability issues that do not necessarily indicate a bug but could lead to potential problems.
- Bugs: Errors in the code that could cause incorrect behavior.
- Vulnerabilities: Security issues that could be exploited.
- Duplications: Duplicate code blocks that should be consolidated.
- Coverage: The percentage of code covered by tests.

### Use Cases:
- Continuous integration and delivery pipelines.
- Monitoring code quality over time.
- Ensuring compliance with coding standards and best practices.
- Identifying and fixing security vulnerabilities.

### Optional
- There is a config for Code Quality Gate status, that only checks for Code Smell, not `Coverage`

### Example for Sonarqube

- This link include Sonarqube integrated with Jenkins Pipeline[**My DevOps Journey: with Jenkins, ArgoCD, and GitOps Tools**](https://medium.com/@kienlt.qn/my-devops-journey-with-jenkins-argocd-and-gitops-tools-e61a57201361) 

---
# 4. Dependency Checks
- Dependency-Check is a Software Composition Analysis (SCA) tool that attempts to detect publicly disclosed vulnerabilities contained within a project's dependencies.
### Common way to dependency checks in several languages:
- Java: `mvn dependency-check:check`
- Python: pip-audit ( I don't like `safety` since it required login to run xD)
```bash
# Install pip-audit
pip install pip-audit
# Usage
Cmd: pip-audit 
Found 1 known vulnerability in 1 package
Name Version ID             Fix Versions
---- ------- -------------- ------------
pip  22.0.2  PYSEC-2023-228 23.3
# Upgrade:
python3 -m pip install pip==23.3
Collecting pip==23.3
......
Successfully installed pip-23.3
# after upgrade
pip-audit 
No known vulnerabilities found
```
- Golang: I would go for govulncheck
`govulncheck` is a tool provided by the Go team to check for known vulnerabilities in Go modules
```bash
# Install:
go install golang.org/x/vuln/cmd/govulncheck@latest
# Check with project: https://github.com/BlackMetalz/KubeNotifyPlus
govulncheck ./...
=== Symbol Results ===

Vulnerability #1: GO-2025-3447
    Timing sidechannel for P-256 on ppc64le in crypto/internal/nistec
  More info: https://pkg.go.dev/vuln/GO-2025-3447
  Standard library
    Found in: crypto/internal/nistec@go1.23.2
    Fixed in: crypto/internal/nistec@go1.23.6
    Platforms: ppc64le
    Example traces found:
      #1: utils/k8s.go:62:18: utils.GetPodLogs calls io.Copy, which eventually calls nistec.P256Point.ScalarBaseMult
      #2: utils/k8s.go:62:18: utils.GetPodLogs calls io.Copy, which eventually calls nistec.P256Point.ScalarMult
      #3: utils/mysql.go:23:23: utils.InitMySQL calls sql.Open, which eventually calls nistec.P256Point.SetBytes

Vulnerability #2: GO-2025-3420
    Sensitive headers incorrectly sent after cross-domain redirect in net/http
  More info: https://pkg.go.dev/vuln/GO-2025-3420
  Standard library
    Found in: net/http@go1.23.2
    Fixed in: net/http@go1.23.5
    Example traces found:
      #1: utils/k8s.go:53:28: utils.GetPodLogs calls rest.Request.Stream, which calls http.Client.Do
      #2: utils/telegram.go:38:24: utils.sendTelegramMessage calls http.Post

Vulnerability #3: GO-2025-3373
    Usage of IPv6 zone IDs can bypass URI name constraints in crypto/x509
  More info: https://pkg.go.dev/vuln/GO-2025-3373
  Standard library
    Found in: crypto/x509@go1.23.2
    Fixed in: crypto/x509@go1.23.5
    Example traces found:
      #1: utils/k8s.go:58:2: utils.GetPodLogs calls http.cancelTimerBody.Close, which eventually calls x509.CertPool.AppendCertsFromPEM
      #2: utils/k8s.go:62:18: utils.GetPodLogs calls io.Copy, which eventually calls x509.Certificate.Verify
      #3: utils/k8s.go:62:18: utils.GetPodLogs calls io.Copy, which eventually calls x509.Certificate.VerifyHostname
      #4: utils/helper.go:20:14: utils.SendResponse calls fmt.Fprintln, which eventually calls x509.HostnameError.Error
      #5: utils/k8s.go:58:2: utils.GetPodLogs calls http.cancelTimerBody.Close, which eventually calls x509.ParseCertificate
      #6: utils/k8s.go:35:46: utils.SetupK8sClient calls kubernetes.NewForConfig, which eventually calls x509.ParseECPrivateKey
      #7: utils/k8s.go:35:46: utils.SetupK8sClient calls kubernetes.NewForConfig, which eventually calls x509.ParsePKCS1PrivateKey
      #8: utils/k8s.go:35:46: utils.SetupK8sClient calls kubernetes.NewForConfig, which eventually calls x509.ParsePKCS8PrivateKey
      #9: utils/mysql.go:23:23: utils.InitMySQL calls sql.Open, which eventually calls x509.ParsePKIXPublicKey

Your code is affected by 3 vulnerabilities from the Go standard library.
This scan found no other vulnerabilities in packages you import or modules you
require.
Use '-show verbose' for more details.
```
Solution: upgrade the go version to fix it xD.


# Ref
- https://chatgpt.com/ xD
- https://github.com/thoughtworks/talisman
- https://www.geeksforgeeks.org/software-testing-mutation-testing/
- https://www.aquasec.com/cloud-native-academy/supply-chain-security/owasp-dependency-check/