# Code Copycat Defender - Capability Map

## System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        WEB[Frontend UI<br/>React Web App]
        API[REST API<br/>Backend Services]
    end

    subgraph "Input Processing"
        PURL[PURL to Source<br/>Package Downloader]
        UPMEX[UPMEX<br/>Metadata Extractor]
    end

    subgraph "Core Analysis Engine"
        MINER[Code Miner<br/>Pattern Extraction]
        BINARY[Binary Sniffer<br/>Binary Analysis]
        SRC2ID[Source To ID<br/>Source Identification]
        AGENT[Open Agentic Framework<br/>AI Analysis]
    end

    subgraph "License & Compliance"
        OSLILI[OS License Identification Library<br/>License Detection]
        NOTICE[PURL to Notice<br/>Legal Docs Generator]
    end

    subgraph "Data Storage"
        DB[(Database<br/>Results & Metadata)]
        CACHE[(Cache<br/>Package Data)]
    end

    WEB --> API
    API --> PURL
    API --> DB
    
    PURL --> CACHE
    PURL --> UPMEX
    PURL --> MINER
    PURL --> BINARY
    PURL --> SRC2ID
    
    UPMEX --> DB
    
    MINER --> AGENT
    BINARY --> AGENT
    SRC2ID --> AGENT
    
    AGENT --> OSLILI
    OSLILI --> NOTICE
    
    NOTICE --> DB
    DB --> API
    CACHE --> PURL

    style WEB fill:#fef3c7
    style API fill:#fef3c7
    style PURL fill:#d1fae5
    style UPMEX fill:#d1fae5
    style MINER fill:#d1fae5
    style BINARY fill:#d1fae5
    style SRC2ID fill:#d1fae5
    style AGENT fill:#d1fae5
    style OSLILI fill:#d1fae5
    style NOTICE fill:#fef3c7
    style DB fill:#e5e7eb
    style CACHE fill:#e5e7eb
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant PURL2Src
    participant Analyzers
    participant License
    participant Storage

    User->>Frontend: Submit Package URL
    Frontend->>API: POST /scan
    API->>Storage: Create scan job
    API->>Frontend: Return job ID
    
    API->>PURL2Src: Download package
    PURL2Src->>PURL2Src: Fetch from registry
    PURL2Src->>Storage: Cache package
    
    par Parallel Analysis
        PURL2Src->>Analyzers: Code Miner
        and
        PURL2Src->>Analyzers: Binary Sniffer
        and
        PURL2Src->>Analyzers: UPMEX
        and
        PURL2Src->>Analyzers: Source To ID
    end
    
    Analyzers->>Analyzers: Agentic Framework
    Analyzers->>License: OS License Identification Library
    License->>License: PURL to Notice
    License->>Storage: Save results
    
    Frontend->>API: GET /scan/{id}
    API->>Storage: Fetch results
    API->>Frontend: Return analysis
    Frontend->>User: Display results
```

## Capability Matrix

```mermaid
graph LR
    subgraph "Input Capabilities"
        I1[npm packages]
        I2[PyPI packages]
        I3[Maven/Java]
        I4[Go modules]
        I5[Cargo/Rust]
        I6[RubyGems]
        I7[NuGet/.NET]
        I8[Packagist/PHP]
        I9[CocoaPods]
        I10[Swift packages]
        I11[Pub/Dart]
        I12[Hex/Elixir]
        I13[CPAN/Perl]
    end

    subgraph "Detection Capabilities"
        D1[Code Patterns]
        D2[Binary Signatures]
        D3[License Text]
        D4[Copyright Notices]
        D5[Package Metadata]
        D6[Dependency Trees]
        D7[SWHID Matching]
        D8[Fingerprinting]
        D9[Semantic Analysis]
        D10[AI Classification]
    end

    subgraph "Output Capabilities"
        O1[License Report]
        O2[SBOM Generation]
        O3[Legal Notices]
        O4[Risk Assessment]
        O5[Compliance Status]
        O6[Attribution Files]
        O7[JSON/XML Export]
        O8[PDF Reports]
        O9[CI/CD Integration]
        O10[Webhook Alerts]
    end

    I1 --> D1
    I2 --> D1
    I3 --> D1
    I4 --> D1
    I5 --> D1
    I6 --> D1
    I7 --> D1
    I8 --> D1
    I9 --> D1
    I10 --> D1
    I11 --> D1
    I12 --> D1
    I13 --> D1

    D1 --> O1
    D2 --> O1
    D3 --> O1
    D4 --> O3
    D5 --> O2
    D6 --> O2
    D7 --> O4
    D8 --> O4
    D9 --> O5
    D10 --> O5

    O1 --> O6
    O2 --> O7
    O3 --> O8
    O4 --> O9
    O5 --> O10
```

## Component Status & Capabilities

| Component | Status | Key Capabilities |
|-----------|--------|------------------|
| **Frontend UI** | 🚧 Development | • Web-based submission interface<br/>• Results visualization<br/>• Report generation<br/>• User authentication |
| **Backend API** | 🚧 Development | • RESTful endpoints<br/>• Job queue management<br/>• Webhook notifications<br/>• Rate limiting |
| **PURL to Source** | ✅ Ready | • 13+ package registries<br/>• Automatic unpacking<br/>• Version resolution<br/>• Cache management |
| **Code Miner** | ✅ Ready | • Pattern extraction<br/>• Code fingerprinting<br/>• Initial license detection<br/>• Semantic analysis |
| **Binary Sniffer** | ✅ Ready | • ELF/PE analysis<br/>• String extraction<br/>• Symbol detection<br/>• Embedded OSS finding |
| **Agentic Framework** | ✅ Ready | • AI-powered analysis<br/>• Pattern learning<br/>• Risk scoring<br/>• Intelligent classification |
| **OS License Identification Library** | ✅ Ready | • 700+ SPDX licenses<br/>• Confidence scoring<br/>• Multi-method detection<br/>• Evidence collection |
| **PURL to Notice** | 🚧 Development | • Legal notice generation<br/>• Attribution formatting<br/>• License text inclusion<br/>• Compliance documentation |
| **UPMEX** | ✅ Ready | • Universal metadata parsing<br/>• 13 ecosystems support<br/>• Dependency extraction<br/>• SBOM data collection |
| **Source To ID** | ✅ Ready | • SWHID generation<br/>• Package identification<br/>• Web search integration<br/>• SCANOSS fingerprinting |

## Technology Stack

### Languages & Frameworks
- **Python 3.9+**: Core analysis engine
- **TypeScript/React**: Frontend UI
- **FastAPI**: Backend API
- **PostgreSQL**: Data storage
- **Redis**: Caching & queues

### Key Technologies
- **Software Heritage IDs (SWHID)**: Content-based identification
- **SPDX**: License standardization
- **CycloneDX/SPDX**: SBOM formats
- **Docker**: Containerization
- **Kubernetes**: Orchestration (planned)

### Integrations
- **GitHub Actions**: CI/CD automation
- **GitLab CI**: Pipeline integration
- **Jenkins**: Enterprise CI support
- **Webhooks**: Real-time notifications
- **REST API**: Programmatic access

## Deployment Architecture

```mermaid
graph TB
    subgraph "Cloud Infrastructure"
        LB[Load Balancer]
        
        subgraph "Application Tier"
            WEB1[Frontend Node 1]
            WEB2[Frontend Node 2]
            API1[API Server 1]
            API2[API Server 2]
        end
        
        subgraph "Processing Tier"
            WORKER1[Analysis Worker 1]
            WORKER2[Analysis Worker 2]
            WORKER3[Analysis Worker 3]
        end
        
        subgraph "Data Tier"
            DB[(PostgreSQL<br/>Primary)]
            DBREP[(PostgreSQL<br/>Replica)]
            REDIS[(Redis Cache)]
            S3[(Object Storage)]
        end
    end
    
    LB --> WEB1
    LB --> WEB2
    WEB1 --> API1
    WEB2 --> API2
    
    API1 --> REDIS
    API2 --> REDIS
    
    REDIS --> WORKER1
    REDIS --> WORKER2
    REDIS --> WORKER3
    
    WORKER1 --> DB
    WORKER2 --> DB
    WORKER3 --> DB
    
    WORKER1 --> S3
    WORKER2 --> S3
    WORKER3 --> S3
    
    DB --> DBREP
```

## Use Cases

### 1. Enterprise Compliance Scanning
- Submit internal packages for analysis
- Generate SBOM for all dependencies
- Identify license conflicts
- Create attribution documents

### 2. Supply Chain Security
- Detect embedded OSS in binaries
- Identify unknown components
- Track package provenance
- Risk assessment scoring

### 3. Legal & Compliance Teams
- Automated notice generation
- License compatibility checking
- Copyright attribution
- Audit trail maintenance

### 4. CI/CD Integration
- Pre-commit scanning
- Pull request checks
- Release validation
- Continuous monitoring

### 5. Open Source Projects
- License verification
- Dependency analysis
- Attribution management
- Compliance documentation

## Roadmap

### Phase 1: Core Engine (70% Complete)
- ✅ Package download & extraction
- ✅ Pattern analysis & mining
- ✅ Binary scanning
- ✅ License detection
- ✅ AI-powered analysis
- ✅ Metadata extraction
- ✅ Source identification
- 🚧 Notice generation

### Phase 2: Platform (In Progress)
- 🚧 Web interface
- 🚧 REST API
- 🚧 Authentication & authorization
- ⬜ Batch processing
- ⬜ Report generation

### Phase 3: Enterprise Features (Planned)
- ⬜ Multi-tenant support
- ⬜ LDAP/SSO integration
- ⬜ Custom policy engine
- ⬜ Compliance dashboards
- ⬜ Advanced analytics

### Phase 4: Ecosystem Integration (Future)
- ⬜ IDE plugins
- ⬜ Container scanning
- ⬜ Cloud marketplace
- ⬜ SaaS offering
- ⬜ API marketplace