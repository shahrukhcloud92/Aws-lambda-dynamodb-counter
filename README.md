# Aws-lambda-dynamodb-counter
An event-driven, decoupled serverless web app deployed on AWS. Utilizes S3 for hosting, API Gateway for RESTful routing, and AWS Lambda (Python) with DynamoDB atomic counters to deliver high-concurrency, real-time visitor tracking with strict IAM least-privilege security.

# High-Concurrency Serverless Visitor Counter Architecture

An event-driven, completely decoupled serverless web application deployed on AWS infrastructure. This repository showcases cloud-native patterns, automated atomic state updates, optimized execution runtimes, and strict adherence to the IAM Principle of Least Privilege.

---

## 🏗️ System Architecture

The architecture relies entirely on AWS managed services to eliminate server management overhead, maximize cost efficiency, and isolate business logic tiers:
<img width="2816" height="1536" alt="system architecture" src="https://github.com/user-attachments/assets/142019cc-b5dd-402c-aa89-5fcb3137292e" />


* **Frontend Delivery:** Static assets (HTML5/CSS3/JavaScript) decoupled from the server tier and hosted cost-effectively via **Amazon S3**.
* **API Entry Point:** **Amazon API Gateway** manages incoming REST requests, enforces CORS traffic control validation, and routes requests natively to compute resources.
* **Compute Layer:** An ephemeral **AWS Lambda** function handles single-responsibility compute execution only when triggered.
* **State Persistence:** **Amazon DynamoDB** serves as a fast, single-digit millisecond NoSQL database utilizing decoupled keys for fast key-value lookups.

---

## 🛠️ Key Technical Deep-Dives

### 1. High-Concurrency Safe Increments (DynamoDB Atomic Counters)
To protect data accuracy under high traffic concurrency, this architecture rejects standard "Read-Modify-Write" application cycles which cause race conditions. Instead, it utilizes DynamoDB **Atomic Counters** executing a native `ADD` update expression via the Boto3 SDK:
* Updates are pushed directly onto the database engine cluster layer natively.
* Eliminates application-level concurrency locking mechanisms, allowing infinite read/write scaling.

### 2. Ephemeral Function Execution Performance
The microservice is optimized inside a **Python 3.12** runtime using structural exception wrappers:
* Global variables reuse connections across execution invocations, minimizing operational latency.
* Structured JSON validation isolates failure blocks, ensuring the frontend client never hangs if database bottlenecks occur.

---

## 📸 Deployment & Verification Evidence

### 1. User Interface & Frontend Tier
Static resume assets hosted securely via an Amazon S3 bucket endpoint, executing an asynchronous JavaScript Fetch API call to update the live counter component on page load.

<!-- ATTACH YOUR FRONTEND SCREENSHOT DIRECTLY BELOW THIS LINE -->
![S3 Static Frontend Deployment](./1%20front-end.png)
<img width="1366" height="768" alt="1 front end" src="https://github.com/user-attachments/assets/761ca186-e04b-404e-848e-5db6c3daea94" />


### 2. API Gateway Orchestration
RESTful routing setup showing the dedicated `/count` resource and its corresponding `GET` and `OPTIONS` (CORS preflight) method configurations.

<!-- ATTACH YOUR API GATEWAY SCREENSHOT DIRECTLY BELOW THIS LINE -->
![API Gateway Method Execution](./4%20api.png)
<img width="1366" height="768" alt="4 api" src="https://github.com/user-attachments/assets/4d42f052-c86a-4db7-bbf0-94d3171bcef7" />


### 3. Serverless Compute Execution
The optimized Python 3.12 handler script managing event payloads, catching runtime exceptions, and returning CORS-compliant response headers.

<!-- ATTACH YOUR LAMBDA CODE SCREENSHOT DIRECTLY BELOW THIS LINE -->
![AWS Lambda Function Business Logic](./3%20backend%20lambda.png)
<img width="1366" height="768" alt="3 backend lambda" src="https://github.com/user-attachments/assets/64bfd9b8-d7e2-493f-ba35-526de9f684f4" />


### 4. NoSQL Data Persistence
The production DynamoDB target table utilizing a specific primary key scheme (`ID: visitors`) to maintain state persistence with high-concurrency accuracy.

<!-- ATTACH YOUR DYNAMODB TABLE SCREENSHOT DIRECTLY BELOW THIS LINE -->
![Amazon DynamoDB Session Storage](./2%20database.png)
<img width="1366" height="768" alt="2 database" src="https://github.com/user-attachments/assets/2a16e612-9b3f-4e02-adcc-993c283469ed" />


---

## 🧠 Trade-Offs & Production Architecture Evolution

While highly optimal for specific baseline applications, a real-world enterprise infrastructure deployment would expand upon this implementation with several crucial modifications:

* **The CORS Wildcard Vulnerability:** The Lambda function currently exposes `'Access-Control-Allow-Origin': '*'`. In enterprise scenarios, wildcard origins create cross-domain security issues.
  * *The Fix:* Implement explicit domain string matching or move infrastructure behind **Amazon CloudFront** to run both S3 assets and API endpoints on the exact same origin domain name.
* **DDoS Infrastructure Bill-Shock:** Because AWS Lambda and API Gateway scale almost limitlessly, malicious actors loop scripts to intentionally inflate computing costs.
  * *The Fix:* Add **AWS WAF (Web Application Firewall)** directly over the ingress paths to block rate-abusive IP addresses and limit payload counts.
