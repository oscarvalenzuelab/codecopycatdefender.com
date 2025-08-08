#!/usr/bin/env python3
"""
Update README.md with Copycat Code Defender component status
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
        
        # Fetch open and closed issues
        open_issues = data.get('open_issues_count', 0)
        
        # Try to get total issues (open + closed)
        total_issues = open_issues
        try:
            issues_req = urllib.request.Request(f"{base_url}/issues?state=all&per_page=1", headers=headers)
            with urllib.request.urlopen(issues_req) as response:
                link_header = response.headers.get('Link', '')
                if link_header and 'last' in link_header:
                    # Parse the last page number from Link header
                    import re
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        total_issues = int(match.group(1))
        except:
            pass
        
        closed_issues = max(0, total_issues - open_issues)
        
        return {
            'exists': True,
            'open_issues': open_issues,
            'closed_issues': closed_issues,
            'total_issues': total_issues,
            'latest_version': latest_version,
            'updated_at': data.get('updated_at', 'N/A'),
            'created_at': data.get('created_at', 'N/A'),
            'default_branch': data.get('default_branch', 'main')
        }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'exists': False, 'open_issues': 0, 'closed_issues': 0, 'total_issues': 0, 'latest_version': '0.0.0'}
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
    """Calculate completion percentage"""
    if total_issues == 0:
        return 0.0
    return (closed_issues / total_issues) * 100

def get_status_badge(percentage: float) -> str:
    """Get status badge based on completion percentage"""
    if percentage >= 90:
        return "🟢"  # Green - Almost complete
    elif percentage >= 70:
        return "🟡"  # Yellow - Good progress
    elif percentage >= 40:
        return "🟠"  # Orange - In progress
    else:
        return "🔴"  # Red - Early stage

def get_progress_bar(percentage: float, width: int = 20) -> str:
    """Create a visual progress bar"""
    filled = int((percentage / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty

def update_readme():
    """Main function to update README with latest stats"""
    
    # Define all components of Copycat Code Defender
    components = [
        {
            'name': 'Frontend UI',
            'component_id': 'semantic-copycat-frontend',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-frontend',
            'pypi': None,
            'description': 'Web interface for scan submission and results visualization',
            'category': 'Web Platform',
            'license': 'MIT'
        },
        {
            'name': 'Backend API',
            'component_id': 'semantic-copycat-backend',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-backend',
            'pypi': None,
            'description': 'Core API services with scan queue management and orchestration',
            'category': 'Web Platform',
            'license': 'MIT'
        },
        {
            'name': 'PURL to Source',
            'component_id': 'semantic-copycat-purl2src',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2src',
            'pypi': 'semantic-copycat-purl2src',
            'description': 'Downloads source code from Package URLs (npm, PyPI, Maven, etc.)',
            'category': 'Analysis Pipeline',
            'license': 'MIT'
        },
        {
            'name': 'Code Miner',
            'component_id': 'semantic-copycat-miner',
            'github': None,  # Private repository
            'pypi': None,  # Not published to PyPI
            'description': 'Extracts code patterns and performs initial license detection',
            'category': 'Analysis Pipeline',
            'status_override': 'complete',  # Manually set as complete
            'version_override': '1.7.0',  # Manually set version
            'license': 'Proprietary'
        },
        {
            'name': 'Binary Sniffer',
            'component_id': 'semantic-copycat-binarysniffer',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-binarysniffer',
            'pypi': 'semantic-copycat-binarysniffer',
            'description': 'Identifies hidden OSS components embedded in binary files',
            'category': 'Analysis Pipeline',
            'license': 'MIT'
        },
        {
            'name': 'Open Agentic Framework',
            'component_id': 'open-agentic-framework',
            'github': 'https://github.com/oscarvalenzuelab/open_agentic_framework',
            'pypi': None,
            'description': 'Agentic analysis framework for intelligent code pattern detection',
            'category': 'Analysis Pipeline',
            'license': 'Apache-2.0'
        },
        {
            'name': 'LiLY Inspector',
            'component_id': 'semantic-copycat-lily',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-lily',
            'pypi': None,
            'description': 'Advanced license detection and classification engine',
            'category': 'License Analysis',
            'license': 'MIT'
        },
        {
            'name': 'PURL to Notice',
            'component_id': 'semantic-copycat-purl2notice',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2notice',
            'pypi': None,
            'description': 'Generates legal notices with licenses and copyright information',
            'category': 'License Analysis',
            'license': 'MIT'
        }
    ]
    
    # Fetch stats for all components
    component_stats = []
    total_open = 0
    total_closed = 0
    total_components_ready = 0
    
    for component in components:
        stats = {
            'name': component['name'],
            'component_id': component['component_id'],
            'description': component['description'],
            'category': component.get('category', 'Core'),
            'license': component.get('license', 'TBD'),
            'github_exists': False,
            'pypi_exists': False,
            'version': component.get('version_override', '0.0.0'),
            'open_issues': 0,
            'closed_issues': 0,
            'total_issues': 0,
            'completion': 0.0,
            'github_url': component.get('github', ''),
            'pypi_url': f"https://pypi.org/project/{component['pypi']}/" if component.get('pypi') else None,
            'status_override': component.get('status_override', None)
        }
        
        # Fetch GitHub stats
        if component.get('github'):
            parsed = parse_github_url(component['github'])
            if parsed:
                owner, repo = parsed
                github_stats = fetch_github_stats(owner, repo)
                if github_stats:
                    stats['github_exists'] = github_stats.get('exists', False)
                    stats['open_issues'] = github_stats.get('open_issues', 0)
                    stats['closed_issues'] = github_stats.get('closed_issues', 0)
                    stats['total_issues'] = github_stats.get('total_issues', 0)
                    stats['version'] = github_stats.get('latest_version', '0.0.0')
                    
                    # Calculate completion
                    if stats['total_issues'] > 0:
                        stats['completion'] = calculate_completion(stats['closed_issues'], stats['total_issues'])
                    elif stats['github_exists'] and stats['version'] != '0.0.0':
                        # If repo exists with a release version but no issues, it's likely complete
                        stats['completion'] = 100.0
                    elif stats['github_exists']:
                        # If repo exists but no version/issues yet, consider it as initial stage
                        stats['completion'] = 10.0
                    
                    total_open += stats['open_issues']
                    total_closed += stats['closed_issues']
        
        # Fetch PyPI stats if applicable
        if component.get('pypi'):
            pypi_stats = fetch_pypi_stats(component['pypi'])
            if pypi_stats:
                stats['pypi_exists'] = pypi_stats.get('exists', False)
                if pypi_stats.get('version', '0.0.0') != '0.0.0':
                    stats['version'] = pypi_stats['version']
                    # If package exists on PyPI with a version, consider it complete
                    if stats['completion'] == 0.0 and stats['pypi_exists']:
                        stats['completion'] = 100.0
        
        # Handle manual status overrides for private/complete components
        if stats['status_override'] == 'complete':
            stats['completion'] = 100.0
            stats['github_exists'] = True  # Mark as existing even if private
        
        # Count ready components (version > 0.0.0 or exists or marked complete)
        if stats['version'] != '0.0.0' or stats['github_exists'] or stats['status_override'] == 'complete':
            total_components_ready += 1
        
        component_stats.append(stats)
    
    # Calculate overall project completion
    overall_completion = (total_components_ready / len(components)) * 100
    
    # Build the new README content
    readme_content = """# 🛡️ Copycat Code Defender

> **Comprehensive code similarity detection and license compliance platform**

## 📊 Project Overview

<div align="center">

### Overall Project Completion

**{:.1f}%** Complete {} **{}/{}** Components Ready

{}

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
    C --> F[Agentic Framework<br/>Intelligent Analysis]
    D --> G[LiLY<br/>License Detection]
    E --> G
    F --> G
    G --> H[PURL2Notice<br/>Generate Legal Docs]
    H --> I[Results to Frontend]
```

1. **User Input**: Submit Package URL through web interface
2. **Source Retrieval**: Download complete source code
3. **Pattern Analysis**: Extract code patterns and signatures
4. **Binary Scanning**: Identify hidden OSS in compiled files
5. **Intelligent Analysis**: Apply agentic framework for advanced detection
6. **License Detection**: Classify and validate licenses
7. **Notice Generation**: Create comprehensive legal documentation

---

## 🎯 Component Status Dashboard

*Last updated: {} UTC*

| Component | Version | License | Status | Progress | Open Tickets | Links |
|-----------|---------|---------|--------|----------|--------------|-------|
""".format(
        overall_completion,
        get_status_badge(overall_completion),
        total_components_ready,
        len(components),
        get_progress_bar(overall_completion, 30),
        datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    )
    
    # Add each component to the table
    for stats in component_stats:
        status_icon = "✅" if stats['version'] != '0.0.0' else "🚧"
        progress_bar = get_progress_bar(stats['completion'], 10)
        
        links = []
        if stats.get('status_override') == 'complete' and not stats['github_url']:
            links.append("Private Repo")
        elif stats['github_url']:
            if stats['github_exists']:
                links.append(f"[GitHub]({stats['github_url']})")
            else:
                links.append("GitHub (planned)")
        if stats['pypi_url']:
            if stats['pypi_exists']:
                links.append(f"[PyPI]({stats['pypi_url']})")
            else:
                links.append("PyPI (planned)")
        
        readme_content += "| **{}**<br/>*{}* | {} | {} | {} | {} {:.0f}% | {} | {} |\n".format(
            stats['name'],
            stats['description'],
            stats['version'],
            stats['license'],
            status_icon,
            progress_bar,
            stats['completion'],
            stats['open_issues'] if stats['open_issues'] > 0 else '-',
            ' · '.join(links) if links else 'TBD'
        )
    
    # Add detailed component information
    readme_content += """

---

## 📋 Component Details

"""
    
    # Group components by category
    categories = {}
    for stats in component_stats:
        category = stats.get('category', 'Core')
        if category not in categories:
            categories[category] = []
        categories[category].append(stats)
    
    # Display components grouped by category
    for category in ['Web Platform', 'Analysis Pipeline', 'License Analysis']:
        if category in categories:
            readme_content += f"### 🏗️ {category}\n\n"
            for stats in categories[category]:
                status_emoji = get_status_badge(stats['completion'])
                readme_content += f"#### {status_emoji} {stats['name']} (`{stats['component_id']}`)\n\n"
                readme_content += f"> {stats['description']}\n\n"
                
                if stats['github_exists'] or stats['pypi_exists'] or stats.get('status_override') == 'complete':
                    readme_content += "| Metric | Value |\n"
                    readme_content += "|--------|-------|\n"
                    readme_content += f"| **Current Version** | {stats['version']} |\n"
                    readme_content += f"| **License** | {stats['license']} |\n"
                    readme_content += f"| **Completion** | {stats['completion']:.1f}% |\n"
                    readme_content += f"| **Open Issues** | {stats['open_issues']} |\n"
                    readme_content += f"| **Closed Issues** | {stats['closed_issues']} |\n"
                    readme_content += f"| **Total Issues** | {stats['total_issues']} |\n\n"
                else:
                    readme_content += "*Component not yet initialized*\n\n"
    
    # Add summary statistics
    total_issues = total_open + total_closed
    issues_completion = calculate_completion(total_closed, total_issues) if total_issues > 0 else 0
    
    readme_content += f"""---

## 📈 Summary Statistics

<div align="center">

| Total Components | Ready | In Development | Total Issues | Resolved | Open |
|-----------------|-------|----------------|--------------|----------|------|
| **{len(components)}** | **{total_components_ready}** | **{len(components) - total_components_ready}** | **{total_issues}** | **{total_closed}** | **{total_open}** |

**Issues Resolution Rate:** {issues_completion:.1f}%

</div>

---

## 🚀 Getting Started

Visit each component's repository for specific setup instructions and documentation.

## 📄 License

Copyright © 2025 Copycat Code Defender Project
"""
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md updated successfully!")
    print(f"📊 Overall completion: {overall_completion:.1f}%")
    print(f"🎯 Components ready: {total_components_ready}/{len(components)}")
    print(f"📝 Total issues: {total_open} open, {total_closed} closed")

if __name__ == "__main__":
    update_readme()