# 🎮 Twitch Streams Data Pipeline

> Complete end-to-end data pipeline for collecting, processing, and analyzing Twitch live stream data in real-time and batch mode, utilizing modern AWS data architecture.

[![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Architecture](#-architecture)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Data Architecture (Medallion)](#-data-architecture-medallion)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation and Setup](#-installation-and-setup)
- [How to Run](#-how-to-run)
- [Monitoring](#-monitoring)
- [EC2 Optimization Tips](#-ec2-optimization-tips)
- [Design Decisions](#-design-decisions)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 About the Project

This project implements a **modern and scalable data pipeline** for capturing, processing, and analyzing live streaming data from Twitch. The solution supports two main workflows:

- **📊 Batch Processing**: Periodic data collection with ETL transformations across layers (Bronze → Silver → Gold)
- **⚡ Real-Time Streaming**: Real-time event ingestion for immediate analytics

The goal is to provide insights into viewing patterns, popular categories, streamer behavior, and platform engagement metrics.

---

## 🏗️ Architecture

### Workflow Diagram

<img width="1245" height="612" alt="twitch-excalidraw" src="https://github.com/user-attachments/assets/fd3c7994-52c8-44ef-a3b4-3e22fbca14b2" />

### Main Components

<div align="center">

| Component | Description | Technology |
|-----------|-------------|------------|
| **Server** | Airflow Hosting & Jobs | ![EC2](https://img.shields.io/badge/EC2-FF9900?style=flat&logo=amazon-ec2&logoColor=white) |
| **Orchestration** | DAG Scheduling & Execution | ![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat&logo=Apache%20Airflow&logoColor=white) |
| **Ingestion** | Twitch API → S3 & SQS | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| **Storage** | Data Lake (Raw/Silver/Gold) | ![S3](https://img.shields.io/badge/S3-569A31?style=flat&logo=amazon-s3&logoColor=white) |
| **Batch Processing** | ETL Transformations | ![Glue](https://img.shields.io/badge/Glue-FF9900?style=flat&logo=amazon-aws&logoColor=white) |
| **Streaming** | Message Queue | ![SQS](https://img.shields.io/badge/SQS-FF4F8B?style=flat&logo=amazon-sqs&logoColor=white) |
| **Real-Time DB** | Event Storage | ![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=flat&logo=amazon-dynamodb&logoColor=white) |
| **Stream Processing** | SQS Consumer → DynamoDB | ![Lambda](https://img.shields.io/badge/Lambda-FF9900?style=flat&logo=aws-lambda&logoColor=white) |
| **Cataloging** | Metadata & Schema | ![Glue](https://img.shields.io/badge/Glue_Catalog-FF9900?style=flat&logo=amazon-aws&logoColor=white) |
| **Query Engine** | SQL Analytics | ![Athena](https://img.shields.io/badge/Athena-232F3E?style=flat&logo=amazon-aws&logoColor=white) |
| **IaC** | Infrastructure as Code | ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white) |
| **Monitoring** | Alerts & Metrics | ![CloudWatch](https://img.shields.io/badge/CloudWatch-FF4F8B?style=flat&logo=amazon-cloudwatch&logoColor=white) ![SNS](https://img.shields.io/badge/SNS-FF4F8B?style=flat&logo=amazon-aws&logoColor=white) |

</div>

---

## 🛠️ Technologies Used

### Orchestration & Workflow
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Cloud & Infrastructure
![AWS EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![AWS S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
![AWS Glue](https://img.shields.io/badge/AWS%20Glue-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=aws-lambda&logoColor=white)
![AWS SQS](https://img.shields.io/badge/Amazon%20SQS-FF4F8B?style=for-the-badge&logo=amazon-sqs&logoColor=white)
![AWS DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)
![AWS Athena](https://img.shields.io/badge/Amazon%20Athena-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS CloudWatch](https://img.shields.io/badge/Amazon%20CloudWatch-FF4F8B?style=for-the-badge&logo=amazon-cloudwatch&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

### Data Processing
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

### Data Format
![Apache Parquet](https://img.shields.io/badge/Apache%20Parquet-50ABF1?style=for-the-badge&logo=apache&logoColor=white)

---

## 📁 Project Structure
```
twitch-streams-pipeline/
│
├── airflow-docker/              # Apache Airflow Configuration
│   ├── dags/
│   │   └── twitch_streams_pipeline.py    # Main DAG
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── stages/                      # Processing Scripts
│   ├── raw/                     # Bronze Layer (Raw)
│   │   ├── get_streams.py       # Twitch API Collection
│   │   ├── upload_s3.py         # S3 Upload
│   │   └── send_sqs.py          # SQS Publishing
│   │
│   ├── silver/                  # Silver Layer (Refined)
│   │   ├── silver_glue.py       # Glue Cleaning Job
│   │   └── upload_glue_silver_script.py
│   │
│   └── gold/                    # Gold Layer (Aggregated)
│       ├── gold_glue.py         # Glue Aggregation Job
│       └── upload_glue_gold_script.py
│
├── streaming_pipeline/          # Real-Time Pipeline
│   └── lambda_sqs_to_timestream/
│       ├── app.py               # Lambda Handler
│       └── requirements.txt
│
├── terraform/                   # Infrastructure as Code
│   ├── main.tf
│   ├── s3.tf
│   ├── glue.tf
│   ├── streaming.tf
│   ├── athena.tf
│   ├── athena_dynamodb_connector.tf
│   ├── monitoring.tf
│   └── backend.tf
│
├── terraform_state/             # Terraform Backend
│   └── main.tf
│
├── .gitignore
└── README.md
```

---

## 🏛️ Data Architecture (Medallion)

This project implements the **Medallion Architecture** (Bronze → Silver → Gold) for data organization and quality:

### 🥉 Bronze Layer (Raw)
- **Format**: Parquet (Snappy compression)
- **Content**: Raw data from Twitch API
- **Frequency**: Every 30 minutes (orchestrated by Airflow on EC2)
- **Schema**: Original data without transformations
- **Location**: `s3://twitch-streams-s3/raw/`
- **Limit**: 100 streams per language per execution (Twitch API provider limitation)

### 🥈 Silver Layer (Refined) - Data Science Layer
- **Format**: Parquet
- **Target Audience**: Data Scientists
- **Purpose**: Clean, validated data ready for exploratory analysis and ML models
- **Transformations**:
  - Null value handling
  - Field renaming to standard conventions
  - Data type conversions
  - Feature Engineering:
    - `tipo_conteudo`: Game vs Non-Game classification
    - `periodo_dia`: Dawn, Morning, Afternoon, Night
    - `horas_assistidas_total`: Engagement metric
- **Location**: `s3://twitch-streams-s3/silver/`

### 🥇 Gold Layer (Aggregated) - Business Intelligence Layer
- **Format**: Parquet
- **Target Audience**: Business Intelligence & Market Intelligence teams
- **Purpose**: Pre-aggregated metrics optimized for dashboards and reports
- **Why Gold instead of Data Warehouse?**: AWS Redshift/RDS are not available in the Free Tier, so the Gold layer serves as a cost-effective alternative for analytical queries
- **Aggregations**:
  - Total streams per day/streamer/category
  - Total streaming minutes
  - Total watch hours
  - Average viewers
  - Peak viewers
- **Dimensions**: Date, Streamer, Category, Content Type, Time Period, Language
- **Location**: `s3://twitch-streams-s3/gold/`

---

## ✨ Features

### 🔄 Batch Pipeline

1. **Extraction (Extract)**
   - Collects live stream data from Twitch API
   - Supports multiple languages (PT, EN, ES)
   - Limit of 100 streams per language per execution (API provider constraint)
   - Calculates stream duration and temporal metrics
   - Runs every 30 minutes via Airflow DAG on EC2

2. **Raw Loading (Load)**
   - Automatic upload to S3 in Parquet format
   - Snappy compression for storage optimization
   - Temporal data organization

3. **Silver Transformation (Transform)**
   - Data cleaning and standardization
   - Business feature enrichment
   - Automatic cataloging via Glue Crawler
   - Optimized for Data Science workflows

4. **Gold Aggregation (Aggregate)**
   - Creates fact tables for analysis
   - Pre-calculated metrics for dashboards
   - Optimized for analytical queries
   - Serves as a Data Warehouse alternative for BI teams

### ⚡ Real-Time Pipeline

1. **SQS Publishing**
   - Each stream event is sent to SQS queue
   - Dead Letter Queue (DLQ) for retry handling
   - Asynchronous and decoupled processing

2. **Lambda Processing**
   - Batch consumption from SQS queue
   - Data transformation and validation
   - DynamoDB writes

3. **DynamoDB Storage**
   - Partition Key: `nome_streamer`
   - Sort Key: `timestamp`
   - Low-latency access for real-time queries
  
### Crawlers
<img width="2506" height="734" alt="image" src="https://github.com/user-attachments/assets/eefa9ee4-e578-4b5d-8271-5ba8822ac185" />

### 📊 Query & Analysis

- **Athena**: SQL queries over S3 data (all layers)
- **Athena-DynamoDB Connector**: SQL queries over real-time DynamoDB data
- **Glue Data Catalog**: Centralized metadata for all tables

- Silver example:
- <img width="2560" height="1488" alt="image" src="https://github.com/user-attachments/assets/55af53fa-bada-43f5-8779-7eadf2e0dd59" />

### 🔔 Monitoring

- **CloudWatch Alarms**: Alerts for DLQ messages
- **SNS Notifications**: Email notifications on failures
- **CloudWatch Logs**: Centralized logs for Lambda and Glue Jobs

---

## 📋 Prerequisites

- **AWS Account** with appropriate permissions
- **AWS EC2 Instance** - **c7i.large** (recommended configuration)
  - Operating System: Amazon Linux 2 / Ubuntu 20.04+
  - Minimum: 4GB RAM, 2 vCPUs
  - Storage: 20GB+ for Docker and logs
- **Terraform** >= 1.0
- **Docker** and **Docker Compose**
- **Python** 3.11+
- **Twitch API Credentials**:
  - `CLIENT_ID`
  - `ACCESS_TOKEN` (must be renewed monthly due to potential expiration based on usage)

---

## 🚀 Installation and Setup

### 0️⃣ EC2 Instance Configuration

**Why c7i.large?**
- **t3.medium**: Was not available in my AWS region at the time
- **t2 instances**: Did not perform well - insufficient resources caused system instability
- **t3.medium with 2GB+ RAM**: Supported the workload but **failed to load Airflow UI correctly** - the interface would freeze, hang, and become unresponsive, preventing real-time monitoring
- **c7i.large**: Provides stable performance with enough memory for Airflow Docker containers to run smoothly without UI freezing

**Create and Configure Instance:**
```bash
# 1. Launch EC2 (via AWS Console or CLI)
# - Type: c7i.large (compute-optimized)
# - AMI: Amazon Linux 2 or Ubuntu 20.04
# - Storage: 20GB gp3
# - Security Group: Open ports 22 (SSH) and 8080 (Airflow UI)

# 2. Connect via SSH
ssh -i your-key.pem ec2-user@your-public-ip

# 3. Install Docker
sudo yum update -y  # Amazon Linux
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# For Ubuntu:
# sudo apt update
# sudo apt install docker.io docker-compose -y

# 4. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 5. Install Terraform
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum install terraform -y

# 6. Install Git
sudo yum install git -y

# 7. Restart session to apply Docker permissions
exit
ssh -i your-key.pem ec2-user@your-public-ip
```

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/twitch-streams-pipeline.git
cd twitch-streams-pipeline
```

### 2️⃣ Configure Environment Variables

Create a `.env` file in the project root:
```env
# Twitch API (Renew monthly - credentials may expire based on usage)
CLIENT_ID=your_client_id
ACCESS_TOKEN=your_access_token

# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=sa-east-1

# S3
S3_BUCKET_NAME=twitch-streams-s3

# SQS
SQS_QUEUE_NAME=Twitch-real-time-sqs
```

**⚠️ Important - Twitch API Credentials:**
- Access tokens must be renewed **every month**
- Expiration depends on usage frequency
- Check Twitch Developer Console regularly

### 3️⃣ Provision AWS Infrastructure
```bash
# Create Terraform backend
cd terraform_state
terraform init
terraform apply

# Provision main resources
cd ../terraform
terraform init
terraform apply
```

### 4️⃣ Start Airflow on EC2

**Why Docker Airflow instead of AWS MWAA?**
- **Cost Efficiency**: AWS Managed Workflows for Apache Airflow (MWAA) is expensive and not available in Free Tier
- **Personal Preference**: Greater control and customization with self-hosted Docker solution
- **Learning Experience**: Better understanding of containerization and orchestration concepts
```bash
cd airflow-docker
docker-compose up -d
```

**Access Airflow UI:**
- Local: `http://localhost:8080` (if using port forwarding)
- Remote: `http://YOUR-EC2-PUBLIC-IP:8080`
- **Username**: admin
- **Password**: admin

**⚠️ Important for EC2:**
- Ensure Security Group allows inbound traffic on port 8080
- For production, consider using a Load Balancer or VPN
- Configure HTTPS for secure access

---

## 💻 How to Run

### Manual DAG Execution

1. Access Airflow UI (`http://YOUR-EC2-PUBLIC-IP:8080`)
2. Enable the `twitch_streams_pipeline` DAG
3. Click "Trigger DAG" for manual execution

### Automatic Execution

The DAG is configured to run **every 30 minutes** automatically via Airflow scheduler running in Docker on EC2.

### Execution Flow
<img width="879" height="576" alt="Captura de Tela 2025-12-05 às 20 55 36" src="https://github.com/user-attachments/assets/3f31b497-3bc9-4d47-9e95-72f862028893" />

**DAG Tasks:**
1. `extract_streams`: Collects data from Twitch API (100 streams/language limit)
2. `load_s3_raw`: Uploads to Bronze layer
3. `publish_sqs`: Publishes for real-time processing
4. `run_silver_etl_job`: Silver transformations (Data Science layer)
5. `run_gold_etl_job`: Gold aggregations (Business Intelligence layer)

---

## 📈 Monitoring

### CloudWatch Dashboards

- **Lambda Metrics**: Invocations, errors, duration
- **Glue Jobs**: Execution status, DPUs consumed
- **SQS**: Messages sent, received, DLQ depth

### Configured Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| DLQ Messages | Visible messages >= 1 | Email via SNS |
| Lambda Errors | Error rate > 5% | Email via SNS |
| Glue Job Failure | Job failed | Email via SNS |

### Logs

- **Airflow Logs on EC2**: `docker logs airflow-docker-airflow-1`
- **Lambda Logs**: CloudWatch Logs `/aws/lambda/Twitch-sqs-dynamodb-lambda`
- **Glue Logs**: S3 `s3://datalake-utils-twitch-streams/glue_logs/`
- **EC2 System Logs**: `/var/log/messages` or `/var/log/syslog`

### Useful EC2 Commands
```bash
# Check Airflow status
docker-compose ps

# View real-time logs
docker-compose logs -f airflow

# Restart Airflow
docker-compose restart

# Stop all containers
docker-compose down

# Check resource usage
htop  # or top
df -h  # disk space
docker system df  # Docker space usage

# Monitor Airflow container
docker stats airflow-docker-airflow-1
```

---

## 💡 EC2 Optimization Tips

### Cost Reduction
- Use **EC2 Spot Instances** for development environments
- Configure **Auto-stop** to halt instance outside business hours
- Monitor with **CloudWatch** to adjust instance size
- Set up **AWS Budgets** alerts

### Performance
- Use **EBS gp3** for better disk I/O
- Configure **swap** if RAM is limited:
```bash
  sudo dd if=/dev/zero of=/swapfile bs=1G count=4
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
```
- Regularly clean old Docker images:
```bash
  docker system prune -a
```
- Monitor container resources:
```bash
  docker stats
```

### Security
- Use **IAM Roles** instead of hardcoded access keys
- Keep Security Group restricted (only necessary IPs)
- Configure **AWS Systems Manager Session Manager** for keyless SSH access
- Enable **CloudWatch Logs** for auditing
- Regularly update Docker images and system packages

---

## 🎯 Use Cases

1. **Trend Analysis**: Identify rising categories and streamers
2. **Schedule Optimization**: Determine best streaming times
3. **Audience Segmentation**: Analysis by language and content type
4. **Engagement Metrics**: Watch hours, peak viewers
5. **Real-Time Alerts**: Notifications about important events

---

## 🏗️ Design Decisions

### Why EC2 c7i.large?
- **t3.medium unavailable**: Was not available in my AWS region
- **t2 poor performance**: Insufficient resources caused instability
- **t3.medium UI freezing**: Despite having 2GB+ RAM, the Airflow web interface would freeze, hang, and become completely unresponsive, preventing real-time DAG monitoring
- **c7i.large solution**: Compute-optimized instance provides stable performance with smooth Airflow UI operation

### Why Docker Airflow on EC2 instead of AWS MWAA?
- **Cost**: AWS Managed Workflows for Apache Airflow is expensive (~$300-600/month) and not Free Tier eligible
- **Control**: Full control over Airflow configuration and versions
- **Learning**: Better hands-on experience with containerization
- **Flexibility**: Easy to customize and extend

### Why Gold Layer instead of Data Warehouse?
- **Free Tier Limitation**: AWS Redshift, RDS, and Aurora are not available in Free Tier
- **Cost Optimization**: S3-based Gold layer provides similar analytical capabilities at fraction of the cost
- **Athena Integration**: Serverless queries on Gold layer serve as DW alternative
- **Scalability**: Can easily migrate to Redshift/Snowflake when budget allows

### Why 100 Streams per Language Limit?
- **API Provider Constraint**: Twitch API limits maximum results to 100 per request
- **Multiple Languages**: Compensate by querying PT, EN, ES (300 total streams per run)
- **Frequency**: Running every 30 minutes provides good coverage

### Layer Target Audiences
- **Silver Layer**: Designed for **Data Scientists** - clean, validated data for ML and exploratory analysis
- **Gold Layer**: Designed for **Business Intelligence & Market Intelligence** teams - pre-aggregated metrics for dashboards and reports

### Twitch API Credentials
- **Monthly Renewal Required**: Access tokens may expire based on usage patterns
- **Expiration Variability**: Depends on API call frequency and Twitch policies
- **Monitoring**: Check Twitch Developer Console regularly to avoid pipeline interruptions

---

## 📧 Contact

**Eduardo Enrico** - aecesani@gmail.com / 11998992809

**Project Link**: [https://github.com/your-username/twitch-streams-pipeline](https://github.com/your-username/twitch-streams-pipeline)

---

## 🙏 Acknowledgments

- [Twitch API Documentation](https://dev.twitch.tv/docs/api/)
- [Apache Airflow](https://airflow.apache.org/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Documentation](https://docs.docker.com/)

---

Made with ❤️
