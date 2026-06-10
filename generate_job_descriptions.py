"""
generate_job_descriptions.py - Creates 6 diverse job descriptions for testing.

Run once to populate the job_descriptions/ folder:
    python generate_job_descriptions.py
"""

import os
import textwrap


JOB_DESCRIPTIONS = [
    # ────────────────────────────────────────────────────────────
    # 1. Senior Python Backend Engineer
    # ────────────────────────────────────────────────────────────
    {
        "filename": "jd_senior_python_backend.txt",
        "content": textwrap.dedent("""\
            JOB TITLE: Senior Python Backend Engineer
            COMPANY: FinSecure Technologies
            LOCATION: Bangalore, Karnataka (Hybrid)
            EXPERIENCE: 5+ years

            ABOUT THE ROLE
            We are looking for a Senior Python Backend Engineer to join our
            payments platform team. You will design and build high-throughput
            APIs, optimize database performance, and mentor junior engineers.
            Our stack is Python-heavy with Django and FastAPI powering critical
            financial services.

            RESPONSIBILITIES
            • Design and implement scalable RESTful APIs using Django/FastAPI
            • Architect microservices for high-availability payment processing
            • Optimize PostgreSQL queries and implement caching strategies (Redis)
            • Build CI/CD pipelines and maintain deployment infrastructure
            • Conduct code reviews and mentor junior developers
            • Collaborate with product and data teams on feature development
            • Write comprehensive tests and maintain documentation

            REQUIRED SKILLS
            • 5+ years of professional Python development
            • Strong experience with Django or FastAPI frameworks
            • Proficiency with PostgreSQL and Redis
            • Experience with AWS cloud services (EC2, S3, RDS, Lambda)
            • Solid understanding of RESTful API design principles
            • Experience with Docker and containerization
            • Strong problem-solving and communication skills

            PREFERRED SKILLS
            • Experience with Celery and async task processing
            • Knowledge of Kubernetes and container orchestration
            • Experience with message queues (RabbitMQ, Kafka)
            • Familiarity with Terraform or other IaC tools
            • Contributions to open-source Python projects

            MUST-HAVE REQUIREMENTS
            • Minimum 5 years of Python experience
            • Production experience with Django or FastAPI
            • Hands-on PostgreSQL experience
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 2. Machine Learning Engineer
    # ────────────────────────────────────────────────────────────
    {
        "filename": "jd_ml_engineer.txt",
        "content": textwrap.dedent("""\
            JOB TITLE: Machine Learning Engineer
            COMPANY: DataMinds AI
            LOCATION: Mumbai, Maharashtra (Remote-Friendly)
            EXPERIENCE: 3+ years

            ABOUT THE ROLE
            Join our AI team to build and deploy production machine learning
            systems. You will work on NLP, recommendation systems, and MLOps
            infrastructure, taking models from research to production at scale.

            RESPONSIBILITIES
            • Develop and deploy ML models for NLP and recommendation use cases
            • Build end-to-end ML pipelines from data preprocessing to model serving
            • Implement experiment tracking and model versioning
            • Optimize model performance and inference latency
            • Design and maintain feature engineering pipelines
            • Collaborate with data scientists and software engineers
            • Stay current with latest ML/NLP research and techniques

            REQUIRED SKILLS
            • 3+ years of experience in machine learning engineering
            • Strong Python skills with PyTorch or TensorFlow
            • Experience with NLP (transformers, BERT, sentence embeddings)
            • Familiarity with MLOps tools (MLflow, Kubeflow, or SageMaker)
            • Experience deploying ML models as REST APIs
            • Solid understanding of data structures and algorithms
            • Experience with Docker and cloud platforms (AWS or GCP)

            PREFERRED SKILLS
            • Experience with Large Language Models (LLMs) and RAG pipelines
            • Knowledge of recommendation systems
            • Experience with distributed training
            • Familiarity with vector databases (FAISS, ChromaDB, Pinecone)
            • Published research papers in ML/NLP conferences

            MUST-HAVE REQUIREMENTS
            • Minimum 3 years of ML engineering experience
            • Production experience with PyTorch or TensorFlow
            • Hands-on NLP experience with transformer models
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 3. Full-Stack Developer (React + Node.js)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "jd_fullstack_developer.txt",
        "content": textwrap.dedent("""\
            JOB TITLE: Full-Stack Developer
            COMPANY: ShopEasy Commerce
            LOCATION: Pune, Maharashtra (On-site)
            EXPERIENCE: 4+ years

            ABOUT THE ROLE
            We are seeking a Full-Stack Developer to build and enhance our
            e-commerce platform. You will work across the entire stack from
            React frontends to Node.js backends, delivering features that
            serve millions of users.

            RESPONSIBILITIES
            • Build responsive, performant frontend interfaces using React/Next.js
            • Develop backend APIs using Node.js and Express/NestJS
            • Design and optimize database schemas (PostgreSQL, MongoDB)
            • Implement authentication, authorization, and security best practices
            • Build real-time features using WebSockets
            • Write unit and integration tests for frontend and backend
            • Participate in code reviews, architecture discussions, and sprint planning

            REQUIRED SKILLS
            • 4+ years of full-stack web development experience
            • Expert-level React/Next.js with TypeScript
            • Strong Node.js backend development (Express or NestJS)
            • Experience with PostgreSQL and MongoDB
            • Proficiency with Git and CI/CD workflows
            • Understanding of web performance optimization
            • Experience with RESTful APIs and/or GraphQL

            PREFERRED SKILLS
            • Experience with server-side rendering (SSR) and static site generation (SSG)
            • Knowledge of state management (Redux, Zustand)
            • Experience with Docker and Kubernetes
            • Familiarity with AWS or Vercel deployment
            • Experience with design systems and component libraries

            MUST-HAVE REQUIREMENTS
            • Minimum 4 years of full-stack development experience
            • Production experience with React and Node.js
            • TypeScript proficiency
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 4. DevOps / SRE Engineer
    # ────────────────────────────────────────────────────────────
    {
        "filename": "jd_devops_sre.txt",
        "content": textwrap.dedent("""\
            JOB TITLE: DevOps / SRE Engineer
            COMPANY: CloudScale Infrastructure
            LOCATION: Hyderabad, Telangana (Hybrid)
            EXPERIENCE: 4+ years

            ABOUT THE ROLE
            We need a DevOps/SRE Engineer to build and maintain our cloud
            infrastructure, CI/CD pipelines, and monitoring systems. You will
            ensure high availability, automate operations, and establish SRE
            best practices across the engineering organization.

            RESPONSIBILITIES
            • Design and manage Kubernetes clusters on AWS/GCP
            • Build and maintain CI/CD pipelines using GitHub Actions/Jenkins
            • Implement Infrastructure as Code using Terraform
            • Set up monitoring, alerting, and observability (Prometheus, Grafana)
            • Develop automation scripts and tools using Python and Bash
            • Manage incident response and establish SRE practices (SLOs, error budgets)
            • Ensure security best practices and compliance requirements

            REQUIRED SKILLS
            • 4+ years of DevOps/SRE experience
            • Strong Kubernetes expertise (deployment, scaling, troubleshooting)
            • Proficiency with Terraform or similar IaC tools
            • Experience with AWS or GCP cloud platforms
            • Strong Python and Bash scripting skills
            • Experience with monitoring tools (Prometheus, Grafana, Datadog)
            • Understanding of CI/CD principles and tools

            PREFERRED SKILLS
            • Certified Kubernetes Administrator (CKA)
            • Experience with service mesh (Istio, Linkerd)
            • Knowledge of GitOps and ArgoCD
            • Experience with HashiCorp tools (Vault, Consul)
            • Familiarity with chaos engineering principles

            MUST-HAVE REQUIREMENTS
            • Minimum 4 years of DevOps/infrastructure experience
            • Hands-on Kubernetes experience in production
            • Terraform proficiency
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 5. Data Engineer
    # ────────────────────────────────────────────────────────────
    {
        "filename": "jd_data_engineer.txt",
        "content": textwrap.dedent("""\
            JOB TITLE: Data Engineer
            COMPANY: InsightFlow Analytics
            LOCATION: Hyderabad, Telangana (Remote-Friendly)
            EXPERIENCE: 3+ years

            ABOUT THE ROLE
            Join our data platform team to build scalable data pipelines and
            analytics infrastructure. You will design ETL processes, manage
            data warehouses, and ensure data quality across the organization.

            RESPONSIBILITIES
            • Design and build ETL/ELT data pipelines using Python and Spark
            • Manage and optimize data warehouse (Snowflake/BigQuery/Redshift)
            • Implement data quality monitoring and validation frameworks
            • Orchestrate data workflows using Airflow
            • Build real-time streaming pipelines using Kafka
            • Develop dbt models for analytics and reporting
            • Collaborate with data scientists and analysts on data requirements

            REQUIRED SKILLS
            • 3+ years of data engineering experience
            • Strong Python and SQL skills
            • Experience with Apache Spark (PySpark or Scala)
            • Familiarity with data orchestration tools (Airflow, Prefect)
            • Experience with cloud data warehouses (Snowflake, BigQuery, or Redshift)
            • Understanding of data modeling concepts
            • Experience with AWS or GCP cloud services

            PREFERRED SKILLS
            • Experience with real-time streaming (Kafka, Flink)
            • Knowledge of dbt for data transformations
            • Familiarity with data lake architectures (Delta Lake, Iceberg)
            • Experience with data quality tools (Great Expectations)
            • Knowledge of Terraform for infrastructure provisioning

            MUST-HAVE REQUIREMENTS
            • Minimum 3 years of data engineering experience
            • Production experience with Spark
            • Strong SQL proficiency
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 6. Mobile Developer (Flutter / React Native)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "jd_mobile_developer.txt",
        "content": textwrap.dedent("""\
            JOB TITLE: Mobile Developer (Flutter / React Native)
            COMPANY: UrbanGo Mobility
            LOCATION: Bangalore, Karnataka (On-site)
            EXPERIENCE: 3+ years

            ABOUT THE ROLE
            We are looking for a Mobile Developer to build cross-platform
            mobile applications using Flutter or React Native. You will work
            on our consumer-facing mobility app used by millions of commuters.

            RESPONSIBILITIES
            • Build cross-platform mobile applications using Flutter or React Native
            • Implement complex UI designs with smooth animations
            • Integrate with REST APIs and real-time services (WebSockets, Firebase)
            • Optimize app performance, startup time, and memory usage
            • Write widget/component tests and integration tests
            • Manage app releases and deployment pipelines
            • Collaborate with designers and backend engineers

            REQUIRED SKILLS
            • 3+ years of mobile development experience
            • Strong Flutter (Dart) or React Native (JavaScript/TypeScript) skills
            • Experience with state management (BLoC, Provider, Redux)
            • Familiarity with RESTful APIs and Firebase
            • Understanding of mobile app architecture patterns (MVVM, Clean Architecture)
            • Experience with Git and mobile CI/CD tools
            • Published apps on Google Play Store and/or Apple App Store

            PREFERRED SKILLS
            • Experience with native Android (Kotlin) or iOS (Swift)
            • Knowledge of maps and location services integration
            • Experience with push notifications and deep linking
            • Familiarity with app performance profiling tools
            • Experience with offline-first architecture

            MUST-HAVE REQUIREMENTS
            • Minimum 3 years of mobile development experience
            • Production Flutter or React Native apps
            • Published apps on app stores
        """),
    },
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "job_descriptions")
    os.makedirs(out_dir, exist_ok=True)

    print(f"Generating {len(JOB_DESCRIPTIONS)} job descriptions in '{out_dir}/':\n")

    for jd in JOB_DESCRIPTIONS:
        filepath = os.path.join(out_dir, jd["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(jd["content"])
        print(f"  [OK] {filepath}")

    print(f"\nDone! {len(JOB_DESCRIPTIONS)} job descriptions generated.")


if __name__ == "__main__":
    main()
