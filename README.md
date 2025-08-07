# 🛡️ Copycat Code Defender

> **Comprehensive code similarity detection and license compliance platform**

## 📊 Project Overview

<div align="center">

### Overall Project Completion

**28.6%** Complete 🔴 **2/7** Components Ready

████████░░░░░░░░░░░░░░░░░░░░░░

</div>

---

## 🔄 Analysis Workflow

The platform orchestrates a comprehensive analysis pipeline:

```mermaid
graph LR
    A[User submits PURL] --> B[Backend Queue]
    B --> C[PURL2Src<br/>Download Source]
    C --> D[Code Miner<br/>Extract Patterns]
    C --> E[Binary Sniffer<br/>Scan Binaries]
    D --> F[LiLY<br/>License Detection]
    E --> F
    F --> G[PURL2Notice<br/>Generate Legal Docs]
    G --> H[Results to Frontend]
```

1. **User Input**: Submit Package URL through web interface
2. **Source Retrieval**: Download complete source code
3. **Pattern Analysis**: Extract code patterns and signatures
4. **Binary Scanning**: Identify hidden OSS in compiled files
5. **License Detection**: Classify and validate licenses
6. **Notice Generation**: Create comprehensive legal documentation

---

## 🎯 Component Status Dashboard

*Last updated: 2025-08-07 06:20:03 UTC*

| Component | Version | Status | Progress | Open Tickets | Links |
|-----------|---------|--------|----------|--------------|-------|
| **Frontend UI**<br/>*Web interface for scan submission and results visualization* | 0.0.0 | 🚧 | ░░░░░░░░░░ 0% | - | GitHub (planned) |
| **Backend API**<br/>*Core API services with scan queue management and orchestration* | 0.0.0 | 🚧 | ░░░░░░░░░░ 0% | - | GitHub (planned) |
| **PURL to Source**<br/>*Downloads source code from Package URLs (npm, PyPI, Maven, etc.)* | 0.1.1 | ✅ | █░░░░░░░░░ 10% | - | [GitHub](https://github.com/oscarvalenzuelab/semantic-copycat-purl2src) · [PyPI](https://pypi.org/project/semantic-copycat-purl2src/) |
| **Code Miner**<br/>*Extracts code patterns and performs initial license detection* | 0.0.0 | 🚧 | ░░░░░░░░░░ 0% | - | GitHub (planned) · PyPI (planned) |
| **Binary Sniffer**<br/>*Identifies hidden OSS components embedded in binary files* | 1.8.4 | ✅ | ░░░░░░░░░░ 0% | - | GitHub (planned) · [PyPI](https://pypi.org/project/semantic-copycat-binarysniffer/) |
| **LiLY Inspector**<br/>*Advanced license detection and classification engine* | 0.0.0 | 🚧 | ░░░░░░░░░░ 0% | - | GitHub (planned) |
| **PURL to Notice**<br/>*Generates legal notices with licenses and copyright information* | 0.0.0 | 🚧 | ░░░░░░░░░░ 0% | - | GitHub (planned) |


---

## 📋 Component Details

### 🏗️ Web Platform

#### 🔴 Frontend UI (`semantic-copycat-frontend`)

> Web interface for scan submission and results visualization

*Component not yet initialized*

#### 🔴 Backend API (`semantic-copycat-backend`)

> Core API services with scan queue management and orchestration

*Component not yet initialized*

### 🏗️ Analysis Pipeline

#### 🔴 PURL to Source (`semantic-copycat-purl2src`)

> Downloads source code from Package URLs (npm, PyPI, Maven, etc.)

| Metric | Value |
|--------|-------|
| **Current Version** | 0.1.1 |
| **Completion** | 10.0% |
| **Open Issues** | 0 |
| **Closed Issues** | 0 |
| **Total Issues** | 0 |

#### 🔴 Code Miner (`semantic-copycat-miner`)

> Extracts code patterns and performs initial license detection

*Component not yet initialized*

#### 🔴 Binary Sniffer (`semantic-copycat-binarysniffer`)

> Identifies hidden OSS components embedded in binary files

| Metric | Value |
|--------|-------|
| **Current Version** | 1.8.4 |
| **Completion** | 0.0% |
| **Open Issues** | 0 |
| **Closed Issues** | 0 |
| **Total Issues** | 0 |

### 🏗️ License Analysis

#### 🔴 LiLY Inspector (`semantic-copycat-lily`)

> Advanced license detection and classification engine

*Component not yet initialized*

#### 🔴 PURL to Notice (`semantic-copycat-purl2notice`)

> Generates legal notices with licenses and copyright information

*Component not yet initialized*

---

## 📈 Summary Statistics

<div align="center">

| Total Components | Ready | In Development | Total Issues | Resolved | Open |
|-----------------|-------|----------------|--------------|----------|------|
| **7** | **2** | **5** | **0** | **0** | **0** |

**Issues Resolution Rate:** 0.0%

</div>

---

## 🚀 Getting Started

Visit each component's repository for specific setup instructions and documentation.

## 📄 License

Copyright © 2025 Copycat Code Defender Project
