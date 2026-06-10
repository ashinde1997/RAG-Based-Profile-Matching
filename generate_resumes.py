"""
generate_resumes.py - Creates 32 diverse sample resumes for the RAG system.

Run once to populate the resumes/ folder:
    python generate_resumes.py

Generates a mix of:
- 20 .txt, 6 .pdf, 6 .docx files
- Roles: Backend, Frontend, ML, DevOps, Data, Mobile, QA, Security, etc.
- Experience levels: 1-15 years
- Indian names, cities, companies, and colleges
"""

import os
import textwrap


RESUMES = [
    # ────────────────────────────────────────────────────────────
    # 1. Arjun Sharma — Senior Python Backend (5 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_arjun_sharma.txt",
        "content": textwrap.dedent("""\
            ARJUN SHARMA
            Email: arjun.sharma@email.com | Phone: +91 98765 43210
            LinkedIn: linkedin.com/in/arjunsharma | GitHub: github.com/arjunsharma
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Senior Software Engineer with 5 years of experience specializing in
            Python, Django, and cloud infrastructure. Passionate about building
            scalable backend systems and automating deployment pipelines.

            SKILLS
            Languages: Python, SQL, Bash, JavaScript
            Frameworks: Django, Flask, FastAPI, Celery
            Cloud & DevOps: AWS (EC2, S3, Lambda, RDS), Docker, Terraform
            Databases: PostgreSQL, Redis, MongoDB
            Tools: Git, Jenkins, Jira, Confluence

            WORK EXPERIENCE

            Senior Software Engineer — Flipkart, Bangalore, Karnataka
            June 2021 – Present
            • Led migration of monolithic Django application to microservices architecture
            • Designed and implemented RESTful APIs serving 10M+ requests/day
            • Reduced AWS infrastructure costs by 30% through resource optimization
            • Mentored 3 junior developers in Python best practices and code review

            Software Engineer — Zoho Corporation, Chennai, Tamil Nadu
            Jan 2019 – May 2021
            • Built data ingestion pipelines processing 500GB of daily logs using Python
            • Developed automated testing suite achieving 92% code coverage
            • Implemented CI/CD pipeline using Jenkins and Docker
            • Collaborated with data science team on ML model deployment

            EDUCATION
            B.Tech Computer Science — IIT Bombay (2018)

            CERTIFICATIONS
            • AWS Certified Solutions Architect – Associate
            • Python Institute PCPP – Certified Professional in Python Programming
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 2. Priya Nair — Staff Java/Kubernetes (8 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_priya_nair.txt",
        "content": textwrap.dedent("""\
            PRIYA NAIR
            Email: priya.nair@email.com | Phone: +91 87654 32109
            LinkedIn: linkedin.com/in/priyanair
            Location: Hyderabad, Telangana

            PROFESSIONAL SUMMARY
            Staff Software Engineer with 8 years of experience in enterprise Java
            development, distributed systems, and container orchestration.
            Proven track record of delivering high-availability services at scale.

            SKILLS
            Languages: Java, Kotlin, Go, Python
            Frameworks: Spring Boot, Spring Cloud, Hibernate, gRPC
            Cloud & DevOps: Kubernetes, Docker, AWS, GCP, Helm, ArgoCD
            Databases: MySQL, PostgreSQL, Cassandra, Elasticsearch
            Tools: Git, Gradle, Maven, Prometheus, Grafana

            WORK EXPERIENCE

            Staff Software Engineer — Google India, Hyderabad, Telangana
            Mar 2020 – Present
            • Architected event-driven microservices platform handling 50K events/sec
            • Led Kubernetes migration for 40+ services with zero downtime
            • Designed circuit-breaker patterns reducing cascading failures by 90%
            • Established SRE practices including SLOs, error budgets, and on-call

            Senior Software Engineer — Paytm, Noida, Uttar Pradesh
            Jul 2017 – Feb 2020
            • Built real-time payment processing system using Spring Boot and Kafka
            • Implemented OAuth2/OIDC authentication for 2M+ users
            • Optimized database queries reducing p99 latency from 800ms to 120ms

            Software Engineer — Wipro Technologies, Bangalore, Karnataka
            Jun 2015 – Jun 2017
            • Developed e-commerce backend using Java and Spring MVC
            • Integrated third-party payment gateways (Razorpay, PayU)
            • Automated deployment workflows using Jenkins and Ansible

            EDUCATION
            M.Tech Computer Science — IIT Madras (2015)
            B.Tech Computer Science — NIT Trichy (2013)

            CERTIFICATIONS
            • Certified Kubernetes Administrator (CKA)
            • Oracle Certified Professional Java SE 17 Developer
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 3. Rahul Verma — ML Engineer (3 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_rahul_verma.pdf",
        "content": textwrap.dedent("""\
            RAHUL VERMA
            Email: rahul.verma@email.com | Phone: +91 76543 21098
            LinkedIn: linkedin.com/in/rahulverma | GitHub: github.com/rahulverma
            Location: Mumbai, Maharashtra

            PROFESSIONAL SUMMARY
            Machine Learning Engineer with 3 years of experience building and
            deploying production ML systems. Strong foundation in Python,
            deep learning frameworks, and MLOps best practices.

            SKILLS
            Languages: Python, R, SQL, C++
            ML/AI: TensorFlow, PyTorch, scikit-learn, Hugging Face Transformers
            Data: Pandas, NumPy, Spark, Airflow, dbt
            Cloud & MLOps: AWS SageMaker, MLflow, Kubeflow, Docker
            Tools: Git, Jupyter, Weights & Biases, DVC

            WORK EXPERIENCE

            Machine Learning Engineer — Jio AI Labs, Mumbai, Maharashtra
            Aug 2022 – Present
            • Developed NLP pipeline for resume parsing using BERT-based models
            • Built real-time recommendation engine serving 5M+ users with <50ms latency
            • Designed A/B testing framework for model evaluation in production
            • Reduced model training time by 60% through distributed training on GPUs

            Data Scientist — Fractal Analytics, Pune, Maharashtra
            May 2021 – Jul 2022
            • Built customer churn prediction model achieving 94% accuracy using Python
            • Created automated feature engineering pipeline using Pandas and scikit-learn
            • Deployed models as REST APIs using FastAPI and Docker

            ML Research Intern — IISc Bangalore, Bangalore, Karnataka
            Jun 2020 – Apr 2021
            • Researched transformer architectures for text classification
            • Published paper on efficient fine-tuning of large language models
            • Contributed to open-source TensorFlow model garden

            EDUCATION
            M.Tech Data Science — IIT Delhi (2021)
            B.Tech Computer Science — BITS Pilani (2019)

            PUBLICATIONS
            • "Efficient Fine-Tuning Strategies for LLMs" — NeurIPS Workshop 2021
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 4. Sneha Iyer — Full-Stack JS (6 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_sneha_iyer.docx",
        "content": textwrap.dedent("""\
            SNEHA IYER
            Email: sneha.iyer@email.com | Phone: +91 65432 10987
            LinkedIn: linkedin.com/in/snehaiyer | Portfolio: snehaiyer.dev
            Location: Pune, Maharashtra

            PROFESSIONAL SUMMARY
            Full-Stack Developer with 6 years of experience building modern web
            applications. Expert in JavaScript ecosystem with deep knowledge of
            React, Node.js, and cloud-native architectures.

            SKILLS
            Languages: JavaScript, TypeScript, HTML, CSS, Python
            Frontend: React, Next.js, Redux, Tailwind CSS, Storybook
            Backend: Node.js, Express, NestJS, GraphQL, REST
            Databases: PostgreSQL, MongoDB, Redis, DynamoDB
            Cloud & DevOps: AWS, Vercel, Docker, GitHub Actions, Terraform
            Tools: Git, Figma, Webpack, Vite, Jest, Cypress

            WORK EXPERIENCE

            Senior Full-Stack Developer — Razorpay, Bangalore, Karnataka
            Apr 2021 – Present
            • Led development of SaaS platform used by 200K+ businesses
            • Built server-side rendered app using Next.js improving SEO scores by 45%
            • Implemented real-time collaboration features using WebSockets
            • Reduced page load time by 50% through code splitting and lazy loading

            Full-Stack Developer — Freshworks, Chennai, Tamil Nadu
            Sep 2018 – Mar 2021
            • Developed React-based dashboard for analytics platform
            • Built Node.js microservices for user management and notifications
            • Designed and implemented GraphQL API layer for mobile and web clients

            Junior Developer — TCS Digital, Mumbai, Maharashtra
            Jun 2017 – Aug 2018
            • Built responsive websites using React and CSS Grid
            • Developed REST APIs using Express.js and MongoDB

            EDUCATION
            B.Tech Computer Science — COEP Pune (2017)

            CERTIFICATIONS
            • AWS Certified Developer – Associate
            • Meta Front-End Developer Professional Certificate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 5. Vikram Reddy — Data Engineer (4 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_vikram_reddy.txt",
        "content": textwrap.dedent("""\
            VIKRAM REDDY
            Email: vikram.reddy@email.com | Phone: +91 54321 09876
            LinkedIn: linkedin.com/in/vikramreddy | GitHub: github.com/vikramreddy
            Location: Hyderabad, Telangana

            PROFESSIONAL SUMMARY
            Data Engineer with 4 years of experience designing and maintaining
            large-scale data platforms. Skilled in Python, Apache Spark, and
            modern data stack technologies.

            SKILLS
            Languages: Python, Scala, SQL, Java
            Big Data: Apache Spark, Kafka, Flink, Hadoop
            Data Tools: Airflow, dbt, Snowflake, BigQuery, Redshift
            Cloud: AWS (EMR, Glue, S3, Kinesis), GCP (Dataflow, Pub/Sub)
            Databases: PostgreSQL, Cassandra, HBase, Delta Lake
            Tools: Git, Docker, Kubernetes, Terraform, Great Expectations

            WORK EXPERIENCE

            Senior Data Engineer — Amazon India, Hyderabad, Telangana
            Jan 2022 – Present
            • Architected real-time streaming pipeline processing 2B events/day using Kafka and Spark
            • Led migration from Hadoop to Snowflake reducing query times by 75%
            • Built data quality monitoring framework using Great Expectations and Python
            • Designed dimensional data models serving analytics for 500+ internal users

            Data Engineer — Mu Sigma, Bangalore, Karnataka
            Jun 2020 – Dec 2021
            • Built ETL pipelines processing 5TB of daily sales data using Python and Spark
            • Implemented data lake architecture on AWS S3 with Delta Lake format
            • Created dbt models for business-critical KPI dashboards
            • Automated data pipeline orchestration using Apache Airflow

            EDUCATION
            M.Tech Computer Science — IIIT Hyderabad (2020)
            B.Tech Information Technology — NIT Warangal (2018)

            CERTIFICATIONS
            • Databricks Certified Data Engineer Professional
            • AWS Certified Data Analytics – Specialty
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 6. Meera Krishnan — Embedded Systems (7 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_meera_krishnan.txt",
        "content": textwrap.dedent("""\
            MEERA KRISHNAN
            Email: meera.krishnan@email.com | Phone: +91 43210 98765
            LinkedIn: linkedin.com/in/meerakrishnan
            Location: Chennai, Tamil Nadu

            PROFESSIONAL SUMMARY
            Embedded Systems Engineer with 7 years of experience in firmware
            development, real-time operating systems, and hardware-software
            integration. Strong background in C++ and safety-critical systems.

            SKILLS
            Languages: C++, C, Python, Assembly (ARM, x86)
            RTOS: FreeRTOS, Zephyr, VxWorks, QNX
            Protocols: CAN, SPI, I2C, UART, Ethernet, MQTT
            Tools: JTAG, Oscilloscope, Logic Analyzer, Valgrind
            Hardware: ARM Cortex-M/A, STM32, ESP32, Raspberry Pi
            Development: Git, CMake, GDB, CI/CD (GitLab CI)

            WORK EXPERIENCE

            Senior Embedded Engineer — Tata Elxsi, Bangalore, Karnataka
            May 2020 – Present
            • Designed ADAS sensor fusion module for autonomous vehicle platform
            • Developed real-time control software on FreeRTOS meeting <1ms deadlines
            • Implemented CAN bus communication stack for vehicle ECU network
            • Led team of 4 engineers in MISRA C++ compliant firmware development

            Embedded Software Engineer — Robert Bosch India, Coimbatore, Tamil Nadu
            Jul 2017 – Apr 2020
            • Built firmware for fleet of 10K+ IoT sensor devices using C++ and Zephyr
            • Developed OTA firmware update system with rollback capability
            • Optimized power management achieving 2-year battery life on coin cell

            Junior Firmware Developer — HCL Technologies, Noida, Uttar Pradesh
            Jun 2016 – Jun 2017
            • Developed firmware for medical monitoring devices
            • Implemented IEC 62304 compliant software development lifecycle

            EDUCATION
            M.Tech VLSI Design — IIT Kharagpur (2016)
            B.Tech Electronics & Communication — Anna University, Chennai (2014)

            CERTIFICATIONS
            • ISTQB Certified Tester – Foundation Level
            • ARM Accredited Engineer
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 7. Ankit Patel — Junior Python Backend (2 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_ankit_patel.docx",
        "content": textwrap.dedent("""\
            ANKIT PATEL
            Email: ankit.patel@email.com | Phone: +91 32109 87654
            LinkedIn: linkedin.com/in/ankitpatel | GitHub: github.com/ankitpatel
            Location: Ahmedabad, Gujarat

            PROFESSIONAL SUMMARY
            Backend Developer with 2 years of experience building RESTful APIs
            and microservices using Python and FastAPI. Eager learner with strong
            fundamentals in database design and clean code practices.

            SKILLS
            Languages: Python, SQL, TypeScript, Go
            Frameworks: FastAPI, SQLAlchemy, Pydantic, Alembic
            Databases: PostgreSQL, Redis, SQLite, MongoDB
            Cloud & DevOps: AWS (ECS, RDS, SQS), Docker, GitHub Actions
            Tools: Git, Postman, pgAdmin, VS Code, Pytest

            WORK EXPERIENCE

            Backend Developer — CRED, Bangalore, Karnataka
            Aug 2023 – Present
            • Built RESTful API platform using Python and FastAPI serving 100K daily users
            • Designed PostgreSQL schema for multi-tenant SaaS application
            • Implemented async task processing using Celery and Redis
            • Wrote comprehensive test suite with 95% coverage using Pytest

            Software Engineering Intern — Infosys, Mysore, Karnataka
            Jan 2023 – Jul 2023
            • Developed CRUD APIs for internal tools using FastAPI and SQLAlchemy
            • Built automated database migration pipeline using Alembic
            • Created Python scripts for data migration from legacy MySQL to PostgreSQL

            EDUCATION
            B.Tech Computer Science — DA-IICT Gandhinagar (2023)

            PROJECTS
            • Open-source Python CLI for API load testing (500+ GitHub stars)
            • Personal blog platform built with FastAPI and HTMX
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 8. Kavita Singh — Ruby/Rails Full-Stack (5 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_kavita_singh.txt",
        "content": textwrap.dedent("""\
            KAVITA SINGH
            Email: kavita.singh@email.com | Phone: +91 21098 76543
            LinkedIn: linkedin.com/in/kavitasingh
            Location: Jaipur, Rajasthan

            PROFESSIONAL SUMMARY
            Full-Stack Developer with 5 years of experience specializing in
            Ruby on Rails, GraphQL, and modern frontend technologies.
            Passionate about developer experience and API design.

            SKILLS
            Languages: Ruby, JavaScript, TypeScript, SQL, Python
            Backend: Ruby on Rails, Sinatra, Sidekiq, GraphQL (graphql-ruby)
            Frontend: React, Stimulus, Hotwire (Turbo + Stimulus), Tailwind CSS
            Databases: PostgreSQL, Redis, Elasticsearch
            Cloud & DevOps: Heroku, AWS, Docker, CircleCI, Datadog
            Tools: Git, RSpec, Minitest, Rubocop, Webpack

            WORK EXPERIENCE

            Senior Developer — Zerodha, Bangalore, Karnataka
            Feb 2022 – Present
            • Lead developer on Rails 7 application serving 50K+ subscribers
            • Migrated REST API to GraphQL reducing frontend data fetching by 60%
            • Implemented real-time notifications using Hotwire and ActionCable
            • Improved deployment pipeline reducing release cycle from 1 week to daily

            Full-Stack Developer — Hasura, Bangalore, Karnataka
            Jun 2019 – Jan 2022
            • Built multi-tenant e-commerce platform using Ruby on Rails
            • Developed custom payment integration with Razorpay and PayU
            • Created admin dashboard using React and GraphQL

            Junior Developer — Mindtree, Pune, Maharashtra
            May 2018 – May 2019
            • Developed features for content management system in Rails
            • Wrote RSpec tests maintaining 90% code coverage

            EDUCATION
            B.Tech Computer Science — MNIT Jaipur (2018)

            CERTIFICATIONS
            • AWS Certified Cloud Practitioner
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 9. Deepak Gupta — DevOps Engineer (6 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_deepak_gupta.txt",
        "content": textwrap.dedent("""\
            DEEPAK GUPTA
            Email: deepak.gupta@email.com | Phone: +91 10987 65432
            LinkedIn: linkedin.com/in/deepakgupta | GitHub: github.com/deepakgupta
            Location: Delhi NCR

            PROFESSIONAL SUMMARY
            DevOps Engineer with 6 years of experience in CI/CD, infrastructure
            automation, and cloud architecture. Expert in Python scripting,
            Docker containerization, and Infrastructure as Code.

            SKILLS
            Languages: Python, Bash, Go, YAML, HCL
            CI/CD: Jenkins, GitHub Actions, GitLab CI, ArgoCD, Tekton
            Containers: Docker, Kubernetes, Helm, Istio, Podman
            Cloud: AWS (EKS, ECS, Lambda, CloudFormation), Azure, GCP
            IaC: Terraform, Ansible, Pulumi, CloudFormation
            Monitoring: Prometheus, Grafana, ELK Stack, Datadog, PagerDuty
            Tools: Git, Vault, Consul, Nexus, SonarQube

            WORK EXPERIENCE

            Senior DevOps Engineer — PhonePe, Bangalore, Karnataka
            Oct 2021 – Present
            • Architected Kubernetes platform hosting 100+ microservices on AWS EKS
            • Built zero-downtime deployment pipeline using ArgoCD and Helm
            • Developed Python-based infrastructure automation reducing provisioning time
            • Implemented secrets management using HashiCorp Vault
            • Established SRE practices achieving 99.95% uptime SLA

            DevOps Engineer — Ola Cabs, Bangalore, Karnataka
            Mar 2019 – Sep 2021
            • Migrated legacy applications to Docker containers and Kubernetes
            • Automated infrastructure provisioning using Terraform and Ansible
            • Built CI/CD pipelines for 30+ repositories using Jenkins

            Systems Administrator — Tech Mahindra, Noida, Uttar Pradesh
            Jul 2017 – Feb 2019
            • Managed Linux server fleet of 200+ servers
            • Automated routine tasks using Python and Bash scripts
            • Implemented centralized logging with ELK Stack

            EDUCATION
            B.Tech Information Technology — DTU Delhi (2017)

            CERTIFICATIONS
            • AWS Certified DevOps Engineer – Professional
            • Certified Kubernetes Administrator (CKA)
            • HashiCorp Certified Terraform Associate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 10. Pooja Deshmukh — Go Backend (4 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_pooja_deshmukh.pdf",
        "content": textwrap.dedent("""\
            POOJA DESHMUKH
            Email: pooja.deshmukh@email.com | Phone: +91 99887 76655
            LinkedIn: linkedin.com/in/poojadeshmukh | GitHub: github.com/poojadeshmukh
            Location: Pune, Maharashtra

            PROFESSIONAL SUMMARY
            Backend Engineer with 4 years of experience building high-performance
            distributed systems using Go. Passionate about microservices
            architecture, gRPC, and system design.

            SKILLS
            Languages: Go, Python, Rust, SQL, Protobuf
            Frameworks: Gin, Echo, gRPC-Go, NATS, Temporal
            Infrastructure: Kubernetes, Docker, Istio, Envoy, Consul
            Databases: PostgreSQL, CockroachDB, Redis, etcd, ScyllaDB
            Cloud: GCP (GKE, Cloud Run, Pub/Sub, Spanner), AWS
            Tools: Git, Buf, Wire, GoReleaser, Prometheus, Jaeger

            WORK EXPERIENCE

            Backend Engineer — Swiggy, Bangalore, Karnataka
            May 2022 – Present
            • Built high-throughput order processing system in Go handling 100K req/s
            • Designed gRPC service mesh with Istio for inter-service communication
            • Implemented distributed tracing using OpenTelemetry and Jaeger
            • Created Go SDK for internal platform adopted by 15 engineering teams

            Software Engineer — Directi (Media.net), Mumbai, Maharashtra
            Mar 2021 – Apr 2022
            • Developed event-driven microservices using Go and NATS messaging
            • Implemented rate limiting and circuit breaking with custom Go middleware
            • Optimized garbage collection reducing p99 latency spikes by 40%

            Junior Developer — ThoughtWorks India, Pune, Maharashtra
            Jun 2020 – Feb 2021
            • Built REST APIs in Go using the Gin framework
            • Wrote integration tests and set up CI/CD with GitHub Actions

            EDUCATION
            B.Tech Computer Science — VJTI Mumbai (2020)

            CERTIFICATIONS
            • Google Cloud Professional Cloud Developer
            • Go Developer Certification (by Ardan Labs)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 11. Rohan Mehta — Android/Mobile Developer (4 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_rohan_mehta.pdf",
        "content": textwrap.dedent("""\
            ROHAN MEHTA
            Email: rohan.mehta@email.com | Phone: +91 99001 12233
            LinkedIn: linkedin.com/in/rohanmehta | GitHub: github.com/rohanmehta
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Android Developer with 4 years of experience building native mobile
            applications using Kotlin and Jetpack Compose. Strong focus on
            performance optimization, clean architecture, and CI/CD for mobile.

            SKILLS
            Languages: Kotlin, Java, Dart, SQL
            Android: Jetpack Compose, MVVM, Hilt/Dagger, Room, Retrofit, Coroutines
            Cross-Platform: Flutter, React Native (basic)
            Backend: Firebase, REST APIs, GraphQL
            Tools: Android Studio, Git, Gradle, Fastlane, Bitrise, Figma
            Testing: JUnit, Espresso, Mockito, UI Automator

            WORK EXPERIENCE

            Senior Android Developer — Meesho, Bangalore, Karnataka
            Aug 2022 – Present
            • Led Jetpack Compose migration for flagship app with 50M+ downloads
            • Reduced app startup time by 40% through baseline profiles and lazy init
            • Implemented offline-first architecture using Room and WorkManager
            • Built modular multi-module Gradle project improving build times by 55%

            Android Developer — Swiggy, Bangalore, Karnataka
            Jul 2020 – Jul 2022
            • Developed order tracking features in Kotlin with real-time map integration
            • Implemented in-app payment flows using Razorpay SDK
            • Wrote UI tests with Espresso achieving 80% coverage on critical flows
            • Participated in app size reduction initiative (APK size reduced by 25%)

            EDUCATION
            B.Tech Computer Science — RVCE Bangalore (2020)

            CERTIFICATIONS
            • Google Associate Android Developer Certification
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 12. Nisha Banerjee — iOS Developer (3 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_nisha_banerjee.txt",
        "content": textwrap.dedent("""\
            NISHA BANERJEE
            Email: nisha.banerjee@email.com | Phone: +91 88990 11223
            LinkedIn: linkedin.com/in/nishabanerjee
            Location: Kolkata, West Bengal

            PROFESSIONAL SUMMARY
            iOS Developer with 3 years of experience building polished, performant
            iOS applications using Swift and SwiftUI. Passionate about great UX
            and Apple platform best practices.

            SKILLS
            Languages: Swift, Objective-C, Python
            iOS: SwiftUI, UIKit, Combine, Core Data, Core Animation, ARKit
            Architecture: MVVM, Clean Architecture, Coordinator Pattern
            Backend: Firebase, REST APIs, CloudKit
            Tools: Xcode, Git, CocoaPods, SPM, Fastlane, TestFlight
            Testing: XCTest, Quick/Nimble, Snapshot Testing

            WORK EXPERIENCE

            iOS Developer — PhonePe, Bangalore, Karnataka
            Mar 2023 – Present
            • Developed SwiftUI-based investment module used by 10M+ users
            • Implemented biometric authentication and secure keychain storage
            • Built custom chart components with Core Animation for portfolio view
            • Reduced crash rate from 2.1% to 0.3% through systematic debugging

            iOS Developer — Practo, Bangalore, Karnataka
            Jun 2021 – Feb 2023
            • Built appointment booking flow using UIKit and MVVM architecture
            • Integrated HealthKit for patient vitals tracking
            • Implemented push notification system with rich media support
            • Collaborated with design team on accessibility improvements (WCAG 2.1)

            EDUCATION
            B.Tech Computer Science — Jadavpur University, Kolkata (2021)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 13. Siddharth Joshi — Cloud Architect (10 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_siddharth_joshi.txt",
        "content": textwrap.dedent("""\
            SIDDHARTH JOSHI
            Email: siddharth.joshi@email.com | Phone: +91 77889 90011
            LinkedIn: linkedin.com/in/siddharthjoshi
            Location: Pune, Maharashtra

            PROFESSIONAL SUMMARY
            Cloud Solutions Architect with 10 years of experience designing
            enterprise-grade cloud infrastructure on AWS and GCP. Led cloud
            transformation programs for Fortune 500 clients. Expert in
            cost optimization, security, and multi-cloud strategy.

            SKILLS
            Languages: Python, Go, Bash, HCL, CloudFormation YAML
            AWS: VPC, EC2, EKS, Lambda, RDS, DynamoDB, S3, CloudFront, IAM
            GCP: GKE, Cloud Run, BigQuery, Pub/Sub, Cloud Functions
            Architecture: Microservices, Event-Driven, Serverless, Multi-Cloud
            IaC: Terraform, Pulumi, AWS CDK, CloudFormation
            Security: IAM, KMS, WAF, GuardDuty, Security Hub, SOC2 compliance
            Tools: Docker, Kubernetes, Istio, Consul, Vault

            WORK EXPERIENCE

            Principal Cloud Architect — Accenture India, Pune, Maharashtra
            Jan 2021 – Present
            • Led cloud migration for banking client moving 200+ applications to AWS
            • Designed multi-region disaster recovery achieving RPO <15min, RTO <1hr
            • Established FinOps practice reducing cloud spend by $2M annually
            • Built reusable Terraform modules adopted across 50+ projects

            Senior Cloud Engineer — Microsoft India, Hyderabad, Telangana
            Jun 2017 – Dec 2020
            • Architected hybrid cloud solutions combining Azure and on-premises
            • Designed zero-trust security architecture for enterprise clients
            • Built internal developer platform using Kubernetes and Backstage

            Cloud Engineer — Infosys, Mysore, Karnataka
            Jul 2014 – May 2017
            • Migrated legacy data centers to AWS for retail client
            • Implemented auto-scaling strategies reducing infrastructure costs by 40%
            • Managed multi-account AWS organization with 100+ accounts

            EDUCATION
            M.Tech Computer Science — IIT Kanpur (2014)
            B.Tech Computer Science — COEP Pune (2012)

            CERTIFICATIONS
            • AWS Certified Solutions Architect – Professional
            • Google Cloud Professional Cloud Architect
            • HashiCorp Certified Terraform Associate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 14. Tanvi Agarwal — QA/SDET (5 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_tanvi_agarwal.docx",
        "content": textwrap.dedent("""\
            TANVI AGARWAL
            Email: tanvi.agarwal@email.com | Phone: +91 66778 89900
            LinkedIn: linkedin.com/in/tanviagarwal
            Location: Noida, Uttar Pradesh

            PROFESSIONAL SUMMARY
            Senior QA Engineer / SDET with 5 years of experience in test
            automation, performance testing, and quality engineering. Proficient
            in Python, Selenium, and API testing frameworks.

            SKILLS
            Languages: Python, Java, JavaScript, SQL
            Automation: Selenium, Playwright, Cypress, Appium, Robot Framework
            API Testing: Postman, REST Assured, pytest, requests
            Performance: JMeter, k6, Locust, Gatling
            CI/CD: Jenkins, GitHub Actions, GitLab CI
            Tools: Git, Jira, TestRail, Allure Reports, Docker
            Concepts: BDD (Cucumber), TDD, Shift-Left Testing

            WORK EXPERIENCE

            Senior SDET — Myntra (Flipkart Group), Bangalore, Karnataka
            Apr 2022 – Present
            • Built end-to-end test automation framework using Python and Playwright
            • Designed API contract testing suite validating 100+ microservice endpoints
            • Implemented performance testing pipeline using k6 and GitHub Actions
            • Reduced regression test execution time from 4 hours to 45 minutes
            • Mentored 3 junior QA engineers in automation best practices

            QA Engineer — Wipro Technologies, Pune, Maharashtra
            Jun 2019 – Mar 2022
            • Automated 500+ test cases using Selenium and Python
            • Built BDD test framework with Cucumber and pytest-bdd
            • Conducted API testing for REST services using Postman and requests
            • Created dashboards for test metrics using Allure and Grafana

            EDUCATION
            B.Tech Computer Science — Amity University, Noida (2019)

            CERTIFICATIONS
            • ISTQB Certified Tester – Advanced Level Test Automation
            • AWS Certified Cloud Practitioner
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 15. Arun Kumar — Cybersecurity Engineer (6 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_arun_kumar.txt",
        "content": textwrap.dedent("""\
            ARUN KUMAR
            Email: arun.kumar@email.com | Phone: +91 55667 78899
            LinkedIn: linkedin.com/in/arunkumar
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Cybersecurity Engineer with 6 years of experience in application
            security, penetration testing, and cloud security. Skilled in
            Python scripting, SAST/DAST tools, and incident response.

            SKILLS
            Languages: Python, Bash, Go, PowerShell
            Security: OWASP Top 10, SAST (SonarQube, Checkmarx), DAST (Burp Suite, ZAP)
            Cloud Security: AWS Security Hub, GuardDuty, IAM, CloudTrail, Azure Sentinel
            Network: Wireshark, Nmap, Metasploit, Snort
            Compliance: SOC2, ISO 27001, PCI-DSS, GDPR
            Tools: Git, Splunk, SIEM, Vault, CrowdStrike

            WORK EXPERIENCE

            Senior Security Engineer — Flipkart, Bangalore, Karnataka
            May 2021 – Present
            • Led application security program for 80+ microservices
            • Built automated vulnerability scanning pipeline using Python and Trivy
            • Conducted threat modeling for critical payment and checkout flows
            • Reduced mean time to remediation (MTTR) from 30 days to 5 days
            • Implemented secrets management using HashiCorp Vault

            Security Analyst — Deloitte India, Hyderabad, Telangana
            Mar 2019 – Apr 2021
            • Performed penetration testing for banking and fintech clients
            • Built Python-based security automation tools for compliance auditing
            • Conducted incident response for security breaches
            • Delivered security awareness training to 500+ employees

            Junior Security Engineer — Quick Heal Technologies, Pune, Maharashtra
            Jun 2017 – Feb 2019
            • Analyzed malware samples and developed detection signatures
            • Monitored SIEM alerts and investigated security incidents
            • Assisted in ISO 27001 certification audit

            EDUCATION
            M.Tech Information Security — IIIT Bangalore (2017)
            B.Tech Computer Science — VIT Vellore (2015)

            CERTIFICATIONS
            • Certified Ethical Hacker (CEH)
            • OSCP – Offensive Security Certified Professional
            • AWS Certified Security – Specialty
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 16. Divya Prakash — UI/UX Designer + Frontend (4 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_divya_prakash.pdf",
        "content": textwrap.dedent("""\
            DIVYA PRAKASH
            Email: divya.prakash@email.com | Phone: +91 44556 67788
            LinkedIn: linkedin.com/in/divyaprakash | Portfolio: divyaprakash.design
            Location: Mumbai, Maharashtra

            PROFESSIONAL SUMMARY
            UI/UX Designer and Frontend Developer with 4 years of experience
            creating user-centered digital products. Strong skills in design
            systems, prototyping, and implementing pixel-perfect React interfaces.

            SKILLS
            Design: Figma, Sketch, Adobe XD, Principle, Framer
            Frontend: React, TypeScript, HTML5, CSS3, Tailwind CSS, Framer Motion
            Design Systems: Storybook, Design Tokens, Component Libraries
            Research: User Interviews, Usability Testing, A/B Testing, Hotjar
            Tools: Git, Jira, Notion, Miro, Zeplin
            Concepts: Design Thinking, Accessibility (WCAG 2.1), Responsive Design

            WORK EXPERIENCE

            Senior UI/UX Developer — Zomato, Gurugram, Haryana
            Jun 2022 – Present
            • Led design system serving 3 product teams with 200+ components
            • Built interactive prototypes in Figma reducing design-dev handoff time by 40%
            • Implemented micro-animations using Framer Motion improving engagement by 25%
            • Conducted usability studies with 50+ users for restaurant listing redesign

            UI Developer — BookMyShow, Mumbai, Maharashtra
            Aug 2020 – May 2022
            • Developed responsive event booking interface using React and TypeScript
            • Built component library with Storybook adopted by 4 frontend teams
            • Improved Lighthouse accessibility score from 62 to 95
            • Designed and implemented dark mode theme system

            EDUCATION
            B.Des Interaction Design — NID Ahmedabad (2020)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 17. Amit Saxena — NLP/AI Researcher (5 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_amit_saxena.docx",
        "content": textwrap.dedent("""\
            AMIT SAXENA
            Email: amit.saxena@email.com | Phone: +91 33445 56677
            LinkedIn: linkedin.com/in/amitsaxena | Scholar: scholar.google.com/amitsaxena
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            NLP Research Scientist with 5 years of experience in natural language
            processing, large language models, and conversational AI. Published
            researcher with expertise in Python, PyTorch, and transformer architectures.

            SKILLS
            Languages: Python, C++, Julia
            ML/NLP: PyTorch, Hugging Face Transformers, spaCy, NLTK, LangChain
            LLMs: GPT, BERT, T5, LLaMA, RLHF, Prompt Engineering, RAG
            Data: Pandas, NumPy, Spark, Weights & Biases
            Cloud & MLOps: AWS SageMaker, GCP Vertex AI, MLflow, Docker
            Tools: Git, Jupyter, LaTeX, Wandb, DVC

            WORK EXPERIENCE

            Senior NLP Engineer — Microsoft Research India, Bangalore, Karnataka
            Jan 2022 – Present
            • Developed multilingual question-answering system for 10 Indian languages
            • Fine-tuned LLaMA models for domain-specific text generation
            • Built RAG pipeline using LangChain and vector databases for enterprise search
            • Published 3 papers at ACL and EMNLP on low-resource NLP

            NLP Engineer — Haptik (Reliance Jio), Mumbai, Maharashtra
            Jun 2020 – Dec 2021
            • Built intent classification and entity extraction pipeline using BERT
            • Developed conversational AI chatbot serving 2M monthly users
            • Implemented semantic search using sentence transformers and FAISS
            • Created data annotation pipeline and quality assurance framework

            Research Assistant — IIT Bombay, Mumbai, Maharashtra
            Aug 2019 – May 2020
            • Researched cross-lingual transfer learning for Indian languages
            • Developed Hindi-English code-switching NLP models
            • Published paper at LREC 2020 on multilingual embeddings

            EDUCATION
            M.Tech Computer Science (NLP specialization) — IIT Bombay (2020)
            B.Tech Computer Science — BHU Varanasi (2018)

            PUBLICATIONS
            • "Cross-Lingual Transfer for Low-Resource Indian Languages" — ACL 2023
            • "Efficient RAG for Enterprise Knowledge Bases" — EMNLP 2022
            • "Hindi-English Code-Switching in NLP Models" — LREC 2020
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 18. Lakshmi Sundaram — SRE (5 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_lakshmi_sundaram.pdf",
        "content": textwrap.dedent("""\
            LAKSHMI SUNDARAM
            Email: lakshmi.sundaram@email.com | Phone: +91 22334 45566
            LinkedIn: linkedin.com/in/lakshmisundaram
            Location: Chennai, Tamil Nadu

            PROFESSIONAL SUMMARY
            Site Reliability Engineer with 5 years of experience building
            reliable, observable, and scalable infrastructure. Expert in
            Kubernetes, monitoring systems, and incident management.

            SKILLS
            Languages: Python, Go, Bash, SQL
            Infrastructure: Kubernetes, Docker, Terraform, Ansible, Helm
            Monitoring: Prometheus, Grafana, Datadog, ELK Stack, PagerDuty
            Cloud: AWS (EKS, EC2, RDS, CloudWatch), GCP
            SRE Practices: SLOs/SLIs, Error Budgets, Chaos Engineering, Runbooks
            Tools: Git, Vault, Consul, Istio, ArgoCD

            WORK EXPERIENCE

            Senior SRE — Atlassian India, Bangalore, Karnataka
            Apr 2022 – Present
            • Managed Kubernetes clusters serving 10M+ daily active users
            • Built SLO monitoring platform using Prometheus and custom Go exporter
            • Led chaos engineering program using Litmus and Chaos Monkey
            • Reduced MTTR from 45 min to 12 min through improved runbooks and automation
            • Designed multi-region failover architecture for critical services

            SRE — Shopify India, Bangalore, Karnataka
            Jan 2020 – Mar 2022
            • Implemented observability stack (logs, metrics, traces) using ELK and Jaeger
            • Built auto-scaling policies reducing infrastructure costs by 25%
            • Developed incident response automation using PagerDuty and Python
            • Maintained 99.99% uptime for payment processing services

            Junior DevOps Engineer — Cognizant, Chennai, Tamil Nadu
            Jun 2018 – Dec 2019
            • Managed CI/CD pipelines for Java microservices using Jenkins
            • Automated infrastructure provisioning using Ansible and Terraform
            • Monitored application health using Nagios and Grafana

            EDUCATION
            B.Tech Computer Science — CEG, Anna University, Chennai (2018)

            CERTIFICATIONS
            • Certified Kubernetes Administrator (CKA)
            • AWS Certified SysOps Administrator – Associate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 19. Karan Malhotra — Flutter/Cross-Platform (3 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_karan_malhotra.txt",
        "content": textwrap.dedent("""\
            KARAN MALHOTRA
            Email: karan.malhotra@email.com | Phone: +91 11223 34455
            LinkedIn: linkedin.com/in/karanmalhotra | GitHub: github.com/karanmalhotra
            Location: Chandigarh, Punjab

            PROFESSIONAL SUMMARY
            Cross-Platform Mobile Developer with 3 years of experience building
            production Flutter applications. Strong in Dart, state management,
            and building beautiful, responsive mobile UIs.

            SKILLS
            Languages: Dart, Kotlin, JavaScript, Python
            Mobile: Flutter, BLoC, Riverpod, Provider, GetX
            Backend: Firebase, Supabase, REST APIs, GraphQL
            Tools: Android Studio, VS Code, Git, Figma, Codemagic, Fastlane
            Testing: Widget Testing, Integration Testing, Mockito
            Concepts: Material Design 3, Responsive UI, Offline-First, CI/CD

            WORK EXPERIENCE

            Senior Flutter Developer — Paytm, Noida, Uttar Pradesh
            Feb 2023 – Present
            • Built Paytm Mini Apps platform using Flutter serving 5M+ users
            • Implemented BLoC state management with clean architecture principles
            • Developed custom widget library with 40+ reusable components
            • Integrated native Android/iOS SDKs using platform channels
            • Reduced app crash rate by 60% through systematic error handling

            Flutter Developer — Dunzo, Bangalore, Karnataka
            Aug 2021 – Jan 2023
            • Developed delivery tracking UI with real-time map integration
            • Built chat feature using Firebase Firestore and Cloud Messaging
            • Implemented deep linking and dynamic links for marketing campaigns
            • Created automated screenshot testing pipeline using Codemagic

            EDUCATION
            B.Tech Computer Science — PEC Chandigarh (2021)

            PROJECTS
            • Open-source Flutter UI kit (2K+ GitHub stars)
            • Personal expense tracker app (10K+ Play Store downloads)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 20. Ritu Sharma — Technical Writer (4 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_ritu_sharma.docx",
        "content": textwrap.dedent("""\
            RITU SHARMA
            Email: ritu.sharma@email.com | Phone: +91 99001 22334
            LinkedIn: linkedin.com/in/ritusharma
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Technical Writer with 4 years of experience creating developer
            documentation, API references, and technical guides. Proficient
            in docs-as-code workflows, Markdown, and developer experience.

            SKILLS
            Writing: API Documentation, SDK Guides, Tutorials, Release Notes
            Tools: Markdown, Docusaurus, Swagger/OpenAPI, Postman, Confluence
            Tech: Python, JavaScript, REST APIs, GraphQL, Git
            Design: Figma, Diagrams.net, Mermaid, PlantUML
            Process: Docs-as-Code, CI/CD for Docs, Information Architecture
            Concepts: Developer Experience (DX), Style Guides, Localization

            WORK EXPERIENCE

            Senior Technical Writer — Razorpay, Bangalore, Karnataka
            Mar 2022 – Present
            • Led documentation for payment APIs used by 200K+ businesses
            • Built Docusaurus-based developer portal reducing support tickets by 35%
            • Created interactive API playground using Swagger/OpenAPI
            • Developed style guide and writing standards for engineering org
            • Collaborated with product and engineering on developer experience

            Technical Writer — Postman, Bangalore, Karnataka
            Jun 2020 – Feb 2022
            • Authored API testing guides and tutorials for Postman Learning Center
            • Created video tutorials and walkthroughs for new features
            • Managed documentation for Postman CLI and Newman

            EDUCATION
            M.A. English Literature — Delhi University (2020)
            B.Tech Computer Science — SRM University, Chennai (2018)

            CERTIFICATIONS
            • Google Technical Writing Certificate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 21. Suresh Raman — Blockchain Developer (3 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_suresh_raman.txt",
        "content": textwrap.dedent("""\
            SURESH RAMAN
            Email: suresh.raman@email.com | Phone: +91 88776 65544
            LinkedIn: linkedin.com/in/sureshraman | GitHub: github.com/sureshraman
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Blockchain Developer with 3 years of experience building smart
            contracts, DeFi protocols, and Web3 applications. Expert in
            Solidity, Ethereum, and Rust-based blockchain development.

            SKILLS
            Languages: Solidity, Rust, TypeScript, Python
            Blockchain: Ethereum, Polygon, Solana, Hyperledger Fabric
            Smart Contracts: Hardhat, Foundry, OpenZeppelin, Chainlink
            Frontend: React, Next.js, ethers.js, wagmi, RainbowKit
            Tools: Git, Remix IDE, IPFS, The Graph, Alchemy
            Concepts: DeFi, NFTs, DAOs, ZK-Proofs, Layer-2 Scaling

            WORK EXPERIENCE

            Blockchain Developer — Polygon Labs, Bangalore, Karnataka
            May 2023 – Present
            • Developed smart contracts for cross-chain bridge handling $100M+ TVL
            • Built Solidity libraries for gas-optimized ERC-20 and ERC-721 tokens
            • Implemented ZK-proof verification contracts for Layer-2 scaling
            • Created developer tooling and SDKs for Polygon ecosystem

            Web3 Developer — CoinDCX, Mumbai, Maharashtra
            Jan 2022 – Apr 2023
            • Built DeFi yield aggregator protocol on Ethereum using Solidity
            • Developed React-based dApp frontend with MetaMask integration
            • Conducted smart contract audits for internal and partner projects
            • Implemented automated testing suite using Hardhat and Foundry

            EDUCATION
            B.Tech Computer Science — IIIT Bangalore (2021)

            CERTIFICATIONS
            • Ethereum Developer Certification (ConsenSys)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 22. Geeta Rao — Product Manager (7 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_geeta_rao.txt",
        "content": textwrap.dedent("""\
            GEETA RAO
            Email: geeta.rao@email.com | Phone: +91 77665 54433
            LinkedIn: linkedin.com/in/geetarao
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Senior Product Manager with 7 years of experience leading B2B SaaS
            products from ideation to scale. Strong technical background with
            expertise in data-driven product development and platform strategy.

            SKILLS
            Product: Roadmap Planning, PRDs, User Stories, A/B Testing, OKRs
            Analytics: SQL, Amplitude, Mixpanel, Google Analytics, Tableau
            Technical: Python, REST APIs, System Design (basic), Git
            Design: Figma, Miro, User Research, Design Sprints
            Process: Agile/Scrum, Kanban, RICE Framework, Jobs-to-be-Done
            Tools: Jira, Notion, Confluence, Linear, ProductBoard

            WORK EXPERIENCE

            Senior Product Manager — Freshworks, Chennai, Tamil Nadu
            Jan 2022 – Present
            • Led product strategy for CRM platform serving 60K+ businesses
            • Launched AI-powered ticket classification feature increasing resolution by 30%
            • Drove 45% increase in enterprise revenue through platform API improvements
            • Managed cross-functional team of 12 engineers, 3 designers, and 2 analysts
            • Conducted 100+ customer interviews for product discovery

            Product Manager — Zoho Corporation, Chennai, Tamil Nadu
            Jul 2019 – Dec 2021
            • Owned product roadmap for Zoho Analytics with 5M+ users
            • Launched self-service dashboard builder increasing user engagement by 40%
            • Implemented data pipeline monitoring features using SQL and Python
            • Worked with engineering to define API contracts and technical requirements

            Associate Product Manager — Ola Cabs, Bangalore, Karnataka
            Jun 2017 – Jun 2019
            • Managed driver incentive optimization product reducing costs by 20%
            • Designed and launched new ride categories based on market research
            • Ran A/B tests for pricing algorithms using internal analytics platform

            EDUCATION
            MBA — IIM Bangalore (2017)
            B.Tech Computer Science — NIT Surathkal (2015)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 23. Harish Menon — Python + Django Backend (6 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_harish_menon.pdf",
        "content": textwrap.dedent("""\
            HARISH MENON
            Email: harish.menon@email.com | Phone: +91 66554 43322
            LinkedIn: linkedin.com/in/harishmenon | GitHub: github.com/harishmenon
            Location: Kochi, Kerala

            PROFESSIONAL SUMMARY
            Senior Python Developer with 6 years of experience building scalable
            web applications using Django and Django REST Framework. Strong in
            database optimization, caching strategies, and API design.

            SKILLS
            Languages: Python, SQL, JavaScript, Bash
            Frameworks: Django, Django REST Framework, Celery, FastAPI
            Databases: PostgreSQL, MySQL, Redis, Elasticsearch
            Cloud & DevOps: AWS (EC2, RDS, S3, Lambda), Docker, Nginx, Gunicorn
            Tools: Git, Sentry, New Relic, Swagger, Pytest
            Concepts: REST API Design, Caching, Message Queues, Microservices

            WORK EXPERIENCE

            Senior Python Developer — Razorpay, Bangalore, Karnataka
            Aug 2021 – Present
            • Architected Django-based merchant onboarding platform serving 500K+ merchants
            • Designed and built RESTful APIs with Django REST Framework for payment integrations
            • Implemented Redis caching layer reducing database load by 60%
            • Built async task processing with Celery for bulk payment operations
            • Led Python 3.11 migration and Django 4.2 upgrade across services

            Python Developer — UST Global, Thiruvananthapuram, Kerala
            May 2019 – Jul 2021
            • Developed healthcare data management system using Django and PostgreSQL
            • Built data export APIs processing 10M+ records with streaming responses
            • Implemented full-text search using Elasticsearch and Django Haystack
            • Created automated deployment scripts using Docker and GitHub Actions

            Junior Developer — Infosys, Mysore, Karnataka
            Jun 2017 – Apr 2019
            • Built internal tools using Django for project management
            • Developed Python scripts for data ETL and report generation
            • Wrote unit tests with Pytest achieving 85% code coverage

            EDUCATION
            B.Tech Computer Science — NIT Calicut (2017)

            CERTIFICATIONS
            • AWS Certified Developer – Associate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 24. Swati Patil — Data Scientist + ML (4 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_swati_patil.txt",
        "content": textwrap.dedent("""\
            SWATI PATIL
            Email: swati.patil@email.com | Phone: +91 55443 32211
            LinkedIn: linkedin.com/in/swatipatil | GitHub: github.com/swatipatil
            Location: Pune, Maharashtra

            PROFESSIONAL SUMMARY
            Data Scientist with 4 years of experience in machine learning,
            statistical modeling, and data analysis. Skilled in Python,
            scikit-learn, and building end-to-end ML pipelines.

            SKILLS
            Languages: Python, R, SQL
            ML/AI: scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch
            Data: Pandas, NumPy, Matplotlib, Seaborn, Plotly
            Big Data: PySpark, Hive, Hadoop
            Cloud: AWS (SageMaker, S3, Redshift), GCP (BigQuery, Vertex AI)
            Tools: Git, Jupyter, MLflow, Airflow, Streamlit

            WORK EXPERIENCE

            Senior Data Scientist — Flipkart, Bangalore, Karnataka
            Mar 2022 – Present
            • Built product recommendation engine increasing click-through rate by 18%
            • Developed demand forecasting model using LightGBM for inventory planning
            • Created ML pipeline using Airflow and MLflow for model retraining
            • Conducted A/B testing framework for pricing optimization experiments
            • Presented insights to VP-level stakeholders with actionable recommendations

            Data Scientist — TCS Innovation Lab, Pune, Maharashtra
            Jul 2020 – Feb 2022
            • Built credit risk scoring model for banking client using XGBoost
            • Developed customer segmentation using K-Means and DBSCAN clustering
            • Created interactive dashboards using Streamlit and Plotly
            • Automated data quality checks reducing manual review time by 70%

            EDUCATION
            M.Sc. Statistics — Indian Statistical Institute, Kolkata (2020)
            B.Sc. Statistics — Fergusson College, Pune (2018)

            PUBLICATIONS
            • "Demand Forecasting in E-commerce Using Ensemble Methods" — KDD Workshop 2023
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 25. Varun Tiwari — React + Node Full-Stack (3 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_varun_tiwari.docx",
        "content": textwrap.dedent("""\
            VARUN TIWARI
            Email: varun.tiwari@email.com | Phone: +91 44332 21100
            LinkedIn: linkedin.com/in/varuntiwari | GitHub: github.com/varuntiwari
            Location: Indore, Madhya Pradesh

            PROFESSIONAL SUMMARY
            Full-Stack Developer with 3 years of experience building web
            applications using React, Node.js, and TypeScript. Passionate about
            clean code, testing, and modern development practices.

            SKILLS
            Languages: JavaScript, TypeScript, Python, SQL
            Frontend: React, Next.js, Redux Toolkit, Zustand, Tailwind CSS
            Backend: Node.js, Express, NestJS, Prisma, GraphQL
            Databases: PostgreSQL, MongoDB, Redis
            Cloud: AWS (Amplify, Lambda, DynamoDB), Vercel
            Tools: Git, Docker, Jest, React Testing Library, Cypress

            WORK EXPERIENCE

            Full-Stack Developer — Lenskart, Bangalore, Karnataka
            Jan 2023 – Present
            • Built e-commerce virtual try-on feature using React and WebGL
            • Developed Node.js microservices for order management system
            • Implemented server-side rendering with Next.js improving page speed by 35%
            • Built admin dashboard using React and Chart.js for business analytics
            • Set up CI/CD pipeline with GitHub Actions and Docker

            Junior Developer — Tata Digital, Mumbai, Maharashtra
            Jul 2021 – Dec 2022
            • Developed React components for Tata Neu super app
            • Built REST APIs using Express.js and MongoDB
            • Wrote unit and integration tests using Jest and React Testing Library
            • Participated in agile sprints and code reviews

            EDUCATION
            B.Tech Computer Science — IET DAVV Indore (2021)

            PROJECTS
            • Real-time collaborative whiteboard (React, Socket.io, Node.js)
            • E-commerce platform with Stripe integration (Next.js, Prisma)
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 26. Neha Kapoor — Data Analyst + BI (3 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_neha_kapoor.txt",
        "content": textwrap.dedent("""\
            NEHA KAPOOR
            Email: neha.kapoor@email.com | Phone: +91 33221 10099
            LinkedIn: linkedin.com/in/nehakapoor
            Location: Gurugram, Haryana

            PROFESSIONAL SUMMARY
            Data Analyst with 3 years of experience in business intelligence,
            SQL analytics, and dashboard development. Skilled in translating
            complex data into actionable business insights.

            SKILLS
            Languages: SQL, Python, R
            BI Tools: Tableau, Power BI, Looker, Google Data Studio
            Data: Excel (Advanced), Pandas, NumPy, Matplotlib
            Databases: PostgreSQL, MySQL, BigQuery, Redshift
            Tools: Git, Jupyter, Airflow, dbt
            Concepts: Statistical Analysis, KPI Design, ETL, Data Modeling

            WORK EXPERIENCE

            Data Analyst — Zomato, Gurugram, Haryana
            Apr 2022 – Present
            • Built executive dashboard in Tableau tracking 15+ KPIs for leadership
            • Developed SQL-based analytics pipeline for restaurant performance metrics
            • Created customer cohort analysis driving 20% improvement in retention strategy
            • Automated weekly reports using Python and Airflow reducing manual effort by 80%
            • Collaborated with product team on A/B test analysis for app features

            Junior Data Analyst — EY India, Gurugram, Haryana
            Jun 2021 – Mar 2022
            • Analyzed financial data for audit clients using SQL and Excel
            • Built Power BI dashboards for client engagement metrics
            • Created data validation scripts using Python and Pandas
            • Supported due diligence analysis for M&A transactions

            EDUCATION
            B.Com (Honours) — SRCC, Delhi University (2021)

            CERTIFICATIONS
            • Google Data Analytics Professional Certificate
            • Tableau Desktop Specialist
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 27. Rajesh Nambiar — Python + FastAPI Backend (3 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_rajesh_nambiar.txt",
        "content": textwrap.dedent("""\
            RAJESH NAMBIAR
            Email: rajesh.nambiar@email.com | Phone: +91 22110 09988
            LinkedIn: linkedin.com/in/rajeshnambiar | GitHub: github.com/rajeshnambiar
            Location: Thiruvananthapuram, Kerala

            PROFESSIONAL SUMMARY
            Backend Developer with 3 years of experience building high-performance
            APIs using Python, FastAPI, and PostgreSQL. Focused on async programming,
            database optimization, and clean architecture.

            SKILLS
            Languages: Python, SQL, TypeScript, Rust
            Frameworks: FastAPI, SQLAlchemy, Pydantic, asyncio, aiohttp
            Databases: PostgreSQL, Redis, MongoDB, TimescaleDB
            Cloud: AWS (ECS, RDS, SQS, Lambda), Docker
            Tools: Git, Pytest, Alembic, Celery, RabbitMQ
            Concepts: Async Programming, Event-Driven Architecture, TDD, SOLID

            WORK EXPERIENCE

            Backend Developer — Chargebee, Chennai, Tamil Nadu
            May 2023 – Present
            • Built subscription billing APIs using FastAPI serving 50K+ businesses
            • Implemented async webhook delivery system processing 1M events/day
            • Designed PostgreSQL partitioning strategy for billing tables (500M+ rows)
            • Created comprehensive API documentation using OpenAPI/Swagger
            • Led adoption of async SQLAlchemy for improved database performance

            Python Developer — QBurst, Thiruvananthapuram, Kerala
            Jul 2021 – Apr 2023
            • Developed REST APIs for healthcare platform using FastAPI and PostgreSQL
            • Built real-time notification system using WebSockets and Redis pub/sub
            • Implemented rate limiting and API key authentication middleware
            • Wrote integration tests with Pytest achieving 90% coverage

            EDUCATION
            B.Tech Computer Science — CET Thiruvananthapuram (2021)

            PROJECTS
            • FastAPI starter template with auth, rate limiting (1K+ GitHub stars)
            • Python async job queue library using Redis
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 28. Pallavi Hegde — ML + Computer Vision (4 yrs) [PDF]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_pallavi_hegde.pdf",
        "content": textwrap.dedent("""\
            PALLAVI HEGDE
            Email: pallavi.hegde@email.com | Phone: +91 11009 98877
            LinkedIn: linkedin.com/in/pallavihegde | GitHub: github.com/pallavihegde
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Computer Vision Engineer with 4 years of experience building
            production vision systems using deep learning. Expert in Python,
            PyTorch, and deploying models on edge devices.

            SKILLS
            Languages: Python, C++, CUDA
            ML/CV: PyTorch, OpenCV, TensorFlow, YOLO, SAM, Detectron2
            Deep Learning: CNNs, Transformers (ViT), GANs, Object Detection, Segmentation
            Edge: TensorRT, ONNX, OpenVINO, NVIDIA Jetson, Coral TPU
            Cloud: AWS (SageMaker, EC2 GPU), GCP (Vertex AI)
            Tools: Git, Docker, MLflow, Label Studio, DVC

            WORK EXPERIENCE

            Senior CV Engineer — Ather Energy, Bangalore, Karnataka
            Aug 2022 – Present
            • Built real-time object detection system for autonomous scooter using YOLO v8
            • Deployed PyTorch models on NVIDIA Jetson achieving 30 FPS inference
            • Developed data labeling pipeline processing 100K+ images using Label Studio
            • Implemented model compression (pruning + quantization) reducing size by 70%
            • Created synthetic data generation pipeline using GANs for rare scenarios

            Computer Vision Engineer — Qualcomm India, Hyderabad, Telangana
            Jun 2020 – Jul 2022
            • Developed face recognition system for mobile SoC using TensorRT
            • Built image segmentation pipeline for medical imaging applications
            • Optimized CNN inference on Snapdragon neural processing engine
            • Published internal paper on efficient vision transformer architectures

            EDUCATION
            M.Tech Computer Vision — IIIT Hyderabad (2020)
            B.Tech Computer Science — RV College of Engineering, Bangalore (2018)

            PUBLICATIONS
            • "Edge-Optimized Vision Transformers for Real-Time Detection" — CVPR Workshop 2023
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 29. Manish Dubey — Fresher / Junior (1 yr)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_manish_dubey.txt",
        "content": textwrap.dedent("""\
            MANISH DUBEY
            Email: manish.dubey@email.com | Phone: +91 99887 77665
            LinkedIn: linkedin.com/in/manishdubey | GitHub: github.com/manishdubey
            Location: Lucknow, Uttar Pradesh

            PROFESSIONAL SUMMARY
            Recent Computer Science graduate with 1 year of internship experience
            in web development. Eager to learn and grow as a software developer.
            Familiar with Python, JavaScript, and basic cloud services.

            SKILLS
            Languages: Python, JavaScript, HTML, CSS, SQL
            Frameworks: Flask, Express.js, Bootstrap
            Databases: MySQL, SQLite, MongoDB
            Tools: Git, VS Code, Postman
            Concepts: Data Structures, Algorithms, OOP, REST APIs

            WORK EXPERIENCE

            Software Development Intern — Cognizant, Pune, Maharashtra
            Jan 2024 – Jun 2024
            • Developed web pages using HTML, CSS, and JavaScript
            • Built simple REST APIs using Flask and MySQL
            • Participated in daily standups and code reviews
            • Completed training in Python, SQL, and cloud fundamentals

            EDUCATION
            B.Tech Computer Science — AKTU Lucknow (2024)

            PROJECTS
            • To-do list web app using Flask and SQLite
            • Weather dashboard using JavaScript and OpenWeather API
            • Student management system using Python and MySQL

            CERTIFICATIONS
            • Python for Everybody – Coursera
            • AWS Cloud Practitioner Essentials
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 30. Anjali Choudhary — Platform Engineer (8 yrs) [DOCX]
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_anjali_choudhary.docx",
        "content": textwrap.dedent("""\
            ANJALI CHOUDHARY
            Email: anjali.choudhary@email.com | Phone: +91 88665 54432
            LinkedIn: linkedin.com/in/anjalichoudhary
            Location: Bangalore, Karnataka

            PROFESSIONAL SUMMARY
            Platform Engineer with 8 years of experience building internal
            developer platforms, CI/CD systems, and infrastructure automation.
            Expert in Python, Kubernetes, and developer experience tooling.

            SKILLS
            Languages: Python, Go, TypeScript, Bash, HCL
            Platform: Kubernetes, Docker, Backstage, Crossplane, ArgoCD
            CI/CD: GitHub Actions, Tekton, Jenkins, Spinnaker
            Cloud: AWS (EKS, Lambda, CDK), GCP (GKE, Cloud Build)
            IaC: Terraform, Pulumi, AWS CDK, Crossplane
            Monitoring: Prometheus, Grafana, Datadog, OpenTelemetry
            Tools: Git, Vault, Consul, Harbor, SonarQube

            WORK EXPERIENCE

            Principal Platform Engineer — Razorpay, Bangalore, Karnataka
            Jun 2021 – Present
            • Built internal developer platform (IDP) using Backstage serving 300+ engineers
            • Designed self-service infrastructure provisioning using Crossplane and Terraform
            • Implemented golden path templates reducing new service onboarding from 2 weeks to 2 hours
            • Created centralized observability platform using OpenTelemetry and Grafana
            • Led platform team of 6 engineers setting technical direction

            Senior DevOps Engineer — Walmart Global Tech India, Bangalore, Karnataka
            Mar 2018 – May 2021
            • Managed Kubernetes clusters hosting 500+ microservices
            • Built automated canary deployment system using Spinnaker and Istio
            • Developed Python-based platform CLI tools used by 200+ developers
            • Implemented GitOps workflow using ArgoCD and Helm charts

            DevOps Engineer — Mindtree, Pune, Maharashtra
            Jul 2015 – Feb 2018
            • Automated CI/CD pipelines using Jenkins and Docker
            • Managed AWS infrastructure using CloudFormation and Ansible
            • Built monitoring dashboards using Grafana and Prometheus

            EDUCATION
            B.Tech Computer Science — BITS Pilani (2015)

            CERTIFICATIONS
            • Certified Kubernetes Administrator (CKA)
            • AWS Certified DevOps Engineer – Professional
            • HashiCorp Certified Terraform Associate
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 31. Vivek Shankar — Scala/Big Data Engineer (5 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_vivek_shankar.txt",
        "content": textwrap.dedent("""\
            VIVEK SHANKAR
            Email: vivek.shankar@email.com | Phone: +91 77554 43321
            LinkedIn: linkedin.com/in/vivekshankar | GitHub: github.com/vivekshankar
            Location: Hyderabad, Telangana

            PROFESSIONAL SUMMARY
            Big Data Engineer with 5 years of experience building large-scale
            data processing systems using Scala, Apache Spark, and cloud-native
            data platforms. Strong background in streaming and batch processing.

            SKILLS
            Languages: Scala, Python, Java, SQL
            Big Data: Apache Spark, Kafka, Flink, Hive, Presto
            Data Platforms: Databricks, Snowflake, Delta Lake, Apache Iceberg
            Cloud: AWS (EMR, Glue, Kinesis, Redshift), GCP (Dataproc, BigQuery)
            Tools: Git, Airflow, dbt, Terraform, Docker, Kubernetes
            Databases: PostgreSQL, Cassandra, DynamoDB, Redis

            WORK EXPERIENCE

            Senior Data Engineer — Microsoft India, Hyderabad, Telangana
            Apr 2022 – Present
            • Architected Lakehouse platform using Databricks and Delta Lake for 50+ teams
            • Built real-time streaming pipelines using Spark Structured Streaming and Kafka
            • Designed data governance framework with Unity Catalog and data lineage tracking
            • Optimized Spark jobs reducing compute costs by $500K annually
            • Led migration from on-premises Hadoop to cloud-native Databricks

            Data Engineer — Deloitte India, Hyderabad, Telangana
            Jun 2019 – Mar 2022
            • Built batch ETL pipelines processing 20TB daily using Scala and Spark
            • Implemented real-time fraud detection pipeline using Kafka and Flink
            • Developed dbt models for enterprise data warehouse on Snowflake
            • Created data quality validation framework using Great Expectations

            EDUCATION
            M.Tech Computer Science — IIT Hyderabad (2019)
            B.Tech Computer Science — JNTU Hyderabad (2017)

            CERTIFICATIONS
            • Databricks Certified Data Engineer Professional
            • AWS Certified Big Data – Specialty
        """),
    },
    # ────────────────────────────────────────────────────────────
    # 32. Fatima Sheikh — Python + ML + AWS (5 yrs)
    # ────────────────────────────────────────────────────────────
    {
        "filename": "resume_fatima_sheikh.txt",
        "content": textwrap.dedent("""\
            FATIMA SHEIKH
            Email: fatima.sheikh@email.com | Phone: +91 66443 32210
            LinkedIn: linkedin.com/in/fatimasheikh | GitHub: github.com/fatimasheikh
            Location: Mumbai, Maharashtra

            PROFESSIONAL SUMMARY
            ML Engineer with 5 years of experience building production machine
            learning systems using Python, PyTorch, and AWS. Specializes in NLP,
            recommendation systems, and ML infrastructure.

            SKILLS
            Languages: Python, SQL, Scala, Bash
            ML/AI: PyTorch, scikit-learn, Hugging Face, LangChain, XGBoost
            NLP: Transformers, BERT, GPT, Sentence Embeddings, RAG, spaCy
            MLOps: AWS SageMaker, MLflow, Kubeflow, Airflow, Docker
            Cloud: AWS (EC2, S3, Lambda, ECS, Bedrock), GCP
            Tools: Git, Jupyter, Weights & Biases, DVC, FastAPI

            WORK EXPERIENCE

            Senior ML Engineer — Amazon India, Mumbai, Maharashtra
            Jan 2022 – Present
            • Built multi-modal product search using CLIP embeddings and FAISS
            • Developed text classification pipeline using fine-tuned BERT models
            • Designed RAG system for internal knowledge base using LangChain and OpenSearch
            • Implemented feature store using AWS SageMaker Feature Store
            • Reduced ML model deployment time from 2 weeks to 2 hours with CI/CD

            ML Engineer — Myntra (Flipkart Group), Bangalore, Karnataka
            May 2020 – Dec 2021
            • Built fashion recommendation engine using collaborative filtering and deep learning
            • Developed size prediction model reducing returns by 15%
            • Created NLP pipeline for review sentiment analysis using transformers
            • Deployed models as REST APIs using FastAPI and Docker on AWS ECS

            Data Science Intern — IISC Bangalore, Bangalore, Karnataka
            Jun 2019 – Apr 2020
            • Researched attention mechanisms for text summarization
            • Developed sequence-to-sequence models for abstractive summarization
            • Published paper at NAACL 2020 student workshop

            EDUCATION
            M.Tech AI & ML — IISc Bangalore (2020)
            B.Tech Computer Science — COEP Pune (2018)

            PUBLICATIONS
            • "Attention-Guided Abstractive Summarization" — NAACL Student Workshop 2020
            • "Multi-Modal Search for E-Commerce" — RecSys 2023

            CERTIFICATIONS
            • AWS Certified Machine Learning – Specialty
            • Deep Learning Specialization (Coursera – Andrew Ng)
        """),
    },
]


# --- file creators for each format ---

def create_txt(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")


def create_pdf(path, content):
    """Generate a basic PDF with the resume text."""
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER
    margin = 1 * inch
    y = height - margin

    for line in content.splitlines():
        if y < margin:
            c.showPage()
            y = height - margin
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, line[:90])
        y -= 14

    c.save()
    print(f"  [OK] {path}")


def create_docx(path, content):
    """Generate a DOCX file with the resume text."""
    from docx import Document
    doc = Document()
    for line in content.splitlines():
        doc.add_paragraph(line)
    doc.save(path)
    print(f"  [OK] {path}")


CREATORS = {
    ".txt": create_txt,
    ".pdf": create_pdf,
    ".docx": create_docx,
}


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resumes")
    os.makedirs(out_dir, exist_ok=True)

    print(f"Generating {len(RESUMES)} sample resumes in '{out_dir}/':\n")

    for resume in RESUMES:
        filename = resume["filename"]
        ext = os.path.splitext(filename)[1].lower()
        filepath = os.path.join(out_dir, filename)

        creator = CREATORS.get(ext)
        if creator is None:
            print(f"  [SKIP] Unsupported format: {filename}")
            continue
        creator(filepath, resume["content"])

    # make sure the output directory exists too
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nCreated output directory: {output_dir}/")
    print(f"\nDone! {len(RESUMES)} sample resumes generated.")


if __name__ == "__main__":
    main()
