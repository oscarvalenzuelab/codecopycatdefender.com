#!/usr/bin/env python3
"""
Update README.md with Code Copycat Defender component status
"""
import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error

def fetch_github_stats(owner: str, repo: str) -> Optional[Dict]:
    """Fetch repository statistics from GitHub API"""
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'CopycatCodeDefender-Bot'
    }
    
    # Add GitHub token if available (for higher rate limits)
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        # Fetch repo info
        req = urllib.request.Request(base_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        # Fetch latest release info
        latest_version = "0.0.0"
        try:
            release_req = urllib.request.Request(f"{base_url}/releases/latest", headers=headers)
            with urllib.request.urlopen(release_req) as response:
                release_data = json.loads(response.read().decode())
                latest_version = release_data.get('tag_name', '0.0.0').lstrip('v')
        except:
            # No releases yet
            pass
        
        # Fetch issues info
        open_issues = 0
        closed_issues = 0
        total_issues = 0
        try:
            # Fetch open issues count
            open_req = urllib.request.Request(f"{base_url}/issues?state=open&per_page=1", headers=headers)
            with urllib.request.urlopen(open_req) as response:
                # Get the total count from the Link header if available
                link_header = response.headers.get('Link', '')
                if 'last' in link_header:
                    # Parse the last page number to get total count
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        open_issues = int(match.group(1))
                else:
                    # If no pagination, count the actual issues
                    open_data = json.loads(response.read().decode())
                    open_issues = len(open_data)
            
            # Fetch closed issues count
            closed_req = urllib.request.Request(f"{base_url}/issues?state=closed&per_page=1", headers=headers)
            with urllib.request.urlopen(closed_req) as response:
                link_header = response.headers.get('Link', '')
                if 'last' in link_header:
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        closed_issues = int(match.group(1))
                else:
                    closed_data = json.loads(response.read().decode())
                    closed_issues = len(closed_data)
            
            total_issues = open_issues + closed_issues
        except:
            # Issues API might not be available or accessible
            pass
        
        return {
            'exists': True,
            'latest_version': latest_version,
            'updated_at': data.get('updated_at', 'N/A'),
            'created_at': data.get('created_at', 'N/A'),
            'default_branch': data.get('default_branch', 'main'),
            'open_issues': open_issues,
            'closed_issues': closed_issues,
            'total_issues': total_issues
        }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'exists': False, 'latest_version': '0.0.0'}
        print(f"Error fetching stats for {owner}/{repo}: {e}")
        return None
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"Error fetching stats for {owner}/{repo}: {e}")
        return None

def fetch_pypi_stats(package_name: str) -> Optional[Dict]:
    """Fetch package statistics from PyPI"""
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            info = data.get('info', {})
            return {
                'version': info.get('version', '0.0.0'),
                'exists': True
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'version': '0.0.0', 'exists': False}
        return None
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"Error fetching PyPI stats for {package_name}: {e}")
        return None

def parse_github_url(url: str) -> Optional[tuple]:
    """Extract owner and repo from GitHub URL"""
    pattern = r'github\.com/([^/]+)/([^/\s,]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    return None

def calculate_completion(closed_issues: int, total_issues: int) -> float:
    """Calculate completion percentage based on closed vs total issues"""
    if total_issues == 0:
        return 0.0
    return (closed_issues / total_issues) * 100

def get_progress_bar(percentage: float, width: int = 50) -> str:
    """Create a visual progress bar"""
    filled = int((percentage / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty

def update_readme():
    """Main function to update README with latest stats"""
    
    # Define all components of Code Copycat Defender - Updated list
    components = [
        {
            'name': 'Frontend UI',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-frontend',
            'pypi': None,
            'description': 'Web interface for scan submission and results visualization with enterprise authentication',
            'license': 'MIT',
            'status': 'development'
        },
        {
            'name': 'Backend API',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-backend',
            'pypi': None,
            'description': 'Core API services with scan queue management, orchestration, and webhook notifications',
            'license': 'MIT',
            'status': 'development'
        },
        {
            'name': 'PURL to Source',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2src',
            'pypi': 'semantic-copycat-purl2src',
            'description': 'Downloads source code from Package URLs supporting npm, PyPI, Maven, Go, and more',
            'license': 'MIT',
            'status': 'ready',
            'version_override': '0.1.1'
        },
        {
            'name': 'Code Miner',
            'github': None,  # Private repository
            'pypi': None,
            'description': 'Extracts code patterns and performs initial license detection using semantic analysis',
            'license': 'Private Beta',
            'status': 'ready',
            'version_override': '1.7.0'
        },
        {
            'name': 'Binary Sniffer',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-binarysniffer',
            'pypi': 'semantic-copycat-binarysniffer',
            'description': 'Identifies hidden OSS components embedded in binary files through signature matching',
            'license': 'MIT',
            'status': 'ready',
            'version_override': '1.10.0'
        },
        {
            'name': 'Open Agentic Framework',
            'github': 'https://github.com/oscarvalenzuelab/open_agentic_framework',
            'pypi': None,
            'description': 'AI-powered analysis framework for intelligent code pattern detection and classification',
            'license': 'Apache-2.0',
            'status': 'ready',
            'version_override': '1.1.0'
        },
        {
            'name': 'OS License Identification Library',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-oslili',
            'pypi': 'semantic-copycat-oslili',
            'description': 'High-performance license detection across 700+ SPDX identifiers with confidence scores',
            'license': 'Apache-2.0',
            'status': 'ready',
            'version_override': '1.2.6'
        },
        {
            'name': 'PURL to Notice',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2notices',
            'pypi': 'semantic-copycat-purl2notices',
            'description': 'Generates legal notices with licenses and copyright information for compliance',
            'license': 'MIT',
            'status': 'ready',
            'version_override': '1.1.3'
        },
        {
            'name': 'CCDA',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-ccda',
            'pypi': None,
            'description': 'Code Copycat Defender Advisory - Evolution of OSSA Scanner for semantic code copycat detection',
            'license': 'MIT',
            'status': 'development'
        },
        {
            'name': 'UPMEX',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-upmex',
            'pypi': 'semantic-copycat-upmex',
            'description': 'Universal package metadata extractor supporting 13 package ecosystems',
            'license': 'MIT',
            'status': 'ready',
            'version_override': '1.5.0'
        },
        {
            'name': 'Source To ID',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-src2id',
            'pypi': 'semantic-copycat-src2id',
            'description': 'Identifies package coordinates from source code using SWHIDs and multiple strategies',
            'license': 'AGPL-3.0',
            'status': 'ready',
            'version_override': '1.1.2'
        },
        {
            'name': 'PURL2Risk',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2risk',
            'pypi': None,
            'description': 'Comprehensive risk intelligence including CVEs, business continuity, and OSS health metrics',
            'license': 'MIT',
            'status': 'development'
        }
    ]
    
    # Fetch stats for all components
    component_stats = []
    total_ready = 0
    total_dev = 0
    
    for component in components:
        stats = {
            'name': component['name'],
            'description': component['description'],
            'license': component.get('license', 'MIT'),
            'version': component.get('version_override', '0.0.0'),
            'status': component.get('status', 'development'),
            'github_url': component.get('github', ''),
            'pypi_url': f"https://pypi.org/project/{component['pypi']}/" if component.get('pypi') else None,
            'github_exists': False,
            'pypi_exists': False
        }
        
        # Fetch GitHub stats if URL provided
        if component.get('github'):
            parsed = parse_github_url(component['github'])
            if parsed:
                owner, repo = parsed
                github_stats = fetch_github_stats(owner, repo)
                if github_stats:
                    stats['github_exists'] = github_stats.get('exists', False)
                    if not component.get('version_override'):
                        stats['version'] = github_stats.get('latest_version', '0.0.0')
        
        # Fetch PyPI stats if applicable
        if component.get('pypi'):
            pypi_stats = fetch_pypi_stats(component['pypi'])
            if pypi_stats:
                stats['pypi_exists'] = pypi_stats.get('exists', False)
                if pypi_stats.get('version', '0.0.0') != '0.0.0' and not component.get('version_override'):
                    stats['version'] = pypi_stats['version']
        
        # Count ready vs development
        if stats['status'] == 'ready':
            total_ready += 1
        else:
            total_dev += 1
        
        component_stats.append(stats)
    
    # Calculate overall project completion
    overall_completion = (total_ready / len(components)) * 100
    
    # Build the new README content - Simplified format
    readme_content = """# Code Copycat Defender

> **Enterprise OSS Compliance Platform - Comprehensive code similarity detection and license compliance for modern software development**

## Project Overview

<div align="center">

### Overall Project Completion

**{:.0f}%** Complete | **{}/{}** Components Ready

{}

</div>

---

## Component Status Dashboard

*Last updated: {}*

| Component | Version | License | Status | Links |
|-----------|---------|---------|--------|-------|
""".format(
        overall_completion,
        total_ready,
        len(components),
        get_progress_bar(overall_completion),
        datetime.now(timezone.utc).strftime('%Y-%m-%d')
    )
    
    # Add each component to the table
    for stats in component_stats:
        status_icon = "✅ Ready" if stats['status'] == 'ready' else "🚧 Development"
        
        links = []
        if stats['name'] == 'Code Miner':
            links.append("Private Repo")
        else:
            if stats['github_url']:
                if stats['github_exists']:
                    links.append(f"[GitHub]({stats['github_url']})")
                else:
                    links.append("GitHub (planned)")
            if stats['pypi_url']:
                if stats['pypi_exists']:
                    links.append(f"[PyPI]({stats['pypi_url']})")
        
        readme_content += "| **{}**<br/>*{}* | {} | {} | {} | {} |\n".format(
            stats['name'],
            stats['description'],
            stats['version'],
            stats['license'],
            status_icon,
            ' · '.join(links) if links else 'GitHub (planned)'
        )
    
    # Add platform capabilities section
    readme_content += """
---

## Platform Capabilities

### ✅ Available Features

- **Package Download Engine** - Automated source retrieval from PURL (npm, PyPI, Maven, Go, Cargo)
- **Code Pattern Mining** - Advanced signature extraction and semantic analysis algorithms
- **Binary Component Scanner** - Detection of embedded OSS components in compiled binaries
- **License Detection System** - Identification of 700+ SPDX licenses with confidence scoring
- **AI-Powered Analysis** - Intelligent pattern recognition using agentic framework
- **Metadata Extraction** - Universal parser supporting 13 package ecosystems
- **Source Identification** - Package coordinate mapping using SWHIDs and fingerprinting

### 🚧 In Development

- **Web Management Interface** - Enterprise dashboard for scan submission and monitoring
- **RESTful API** - Programmatic access with authentication and rate limiting
- **Automated Notice Generation** - Legal document creation with attribution requirements
- **Batch Processing Pipeline** - Concurrent analysis of multiple packages with queue management
- **Compliance Dashboard** - Real-time metrics, trends, and risk assessment reports
- **CI/CD Integration** - Native plugins for Jenkins, GitLab, GitHub Actions

---

## Summary Statistics

<div align="center">

| Total Components | Production Ready | In Development | SPDX Licenses Supported |
|-----------------|------------------|----------------|-------------------------|
| **{}** | **{}** | **{}** | **700+** |

</div>

---

## Getting Started

Visit the [project website](https://copycatcodedefender.com) for more information, or explore individual component repositories for specific setup instructions and documentation.

## License

Copyright © 2025 Code Copycat Defender | Enterprise OSS Compliance Platform""".format(
        len(components),
        total_ready,
        total_dev
    )
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md updated successfully!")
    print(f"📊 Overall completion: {overall_completion:.0f}%")
    print(f"🎯 Components ready: {total_ready}/{len(components)}")
    print(f"   - Production Ready: {total_ready}")
    print(f"   - In Development: {total_dev}")

if __name__ == "__main__":
    update_readme()