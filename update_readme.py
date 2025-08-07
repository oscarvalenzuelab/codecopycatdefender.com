#!/usr/bin/env python3
"""
Update README.md with GitHub project statistics
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
import urllib.request
import urllib.error

def fetch_github_stats(owner: str, repo: str) -> Optional[Dict]:
    """Fetch repository statistics from GitHub API"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'CopycatCodeDefender-Bot'
    }
    
    # Add GitHub token if available (for higher rate limits)
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return {
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'watchers': data.get('watchers_count', 0),
                'open_issues': data.get('open_issues_count', 0),
                'language': data.get('language', 'N/A'),
                'updated_at': data.get('updated_at', 'N/A'),
                'description': data.get('description', ''),
                'license': data.get('license', {}).get('name', 'N/A') if data.get('license') else 'N/A',
                'default_branch': data.get('default_branch', 'main')
            }
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
                'version': info.get('version', 'N/A'),
                'summary': info.get('summary', ''),
                'author': info.get('author', 'N/A'),
                'requires_python': info.get('requires_python', 'N/A'),
                'license': info.get('license', 'N/A')
            }
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

def update_readme():
    """Main function to update README with latest stats"""
    
    # Read current README
    with open('README.md', 'r') as f:
        readme_content = f.read()
    
    # Define projects to track
    projects = [
        {
            'name': 'semantic-copycat-purl2src',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2src',
            'pypi': 'semantic-copycat-purl2src'
        },
        {
            'name': 'semantic-copycat-miner',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-miner',
            'pypi': 'semantic-copycat-miner'
        }
    ]
    
    # Build statistics section
    stats_section = f"\n## 📊 Project Statistics\n\n"
    stats_section += f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n\n"
    
    for project in projects:
        stats_section += f"### {project['name']}\n\n"
        
        # GitHub stats
        if project.get('github'):
            parsed = parse_github_url(project['github'])
            if parsed:
                owner, repo = parsed
                github_stats = fetch_github_stats(owner, repo)
                if github_stats:
                    stats_section += f"**GitHub Repository:** [{owner}/{repo}]({project['github']})\n\n"
                    stats_section += "| Metric | Value |\n"
                    stats_section += "|--------|-------|\n"
                    stats_section += f"| ⭐ Stars | {github_stats['stars']} |\n"
                    stats_section += f"| 🍴 Forks | {github_stats['forks']} |\n"
                    stats_section += f"| 👀 Watchers | {github_stats['watchers']} |\n"
                    stats_section += f"| 🐛 Open Issues | {github_stats['open_issues']} |\n"
                    stats_section += f"| 💻 Language | {github_stats['language']} |\n"
                    stats_section += f"| 📜 License | {github_stats['license']} |\n"
                    stats_section += f"| 🔄 Last Updated | {github_stats['updated_at']} |\n\n"
                    
                    if github_stats['description']:
                        stats_section += f"**Description:** {github_stats['description']}\n\n"
        
        # PyPI stats
        if project.get('pypi'):
            pypi_stats = fetch_pypi_stats(project['pypi'])
            if pypi_stats:
                stats_section += f"**PyPI Package:** [{project['pypi']}](https://pypi.org/project/{project['pypi']}/)\n\n"
                stats_section += "| Metric | Value |\n"
                stats_section += "|--------|-------|\n"
                stats_section += f"| 📦 Latest Version | {pypi_stats['version']} |\n"
                stats_section += f"| 🐍 Python Requirement | {pypi_stats['requires_python']} |\n"
                stats_section += f"| 📜 License | {pypi_stats['license']} |\n\n"
        
        stats_section += "---\n\n"
    
    # Check if stats section already exists
    stats_pattern = r'## 📊 Project Statistics.*?(?=##|$)'
    if re.search(stats_pattern, readme_content, re.DOTALL):
        # Replace existing stats section
        updated_readme = re.sub(stats_pattern, stats_section.rstrip() + '\n\n', readme_content, flags=re.DOTALL)
    else:
        # Append stats section at the end
        updated_readme = readme_content.rstrip() + '\n\n' + stats_section
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(updated_readme)
    
    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    update_readme()