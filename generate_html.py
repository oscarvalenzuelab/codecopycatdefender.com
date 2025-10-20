#!/usr/bin/env python3
"""
Generate index.html from component data
"""
import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error

# Import the components data from update_readme
from update_readme import fetch_github_stats, fetch_pypi_stats, parse_github_url, calculate_completion

def generate_html():
    """Generate index.html with updated component stats"""
    
    # Define all components (same as in update_readme.py)
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
            'license': 'MIT',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.1.2'
        },
        {
            'name': 'Code Miner',
            'component_id': 'semantic-copycat-miner',
            'github': None,
            'pypi': None,
            'description': 'Extracts code patterns and performs initial license detection',
            'category': 'Analysis Pipeline',
            'status_override': 'complete',
            'version_override': '1.7.0',
            'license': 'Private Beta'
        },
        {
            'name': 'Binary Sniffer',
            'component_id': 'semantic-copycat-binarysniffer',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-binarysniffer',
            'pypi': 'semantic-copycat-binarysniffer',
            'description': 'Identifies hidden OSS components embedded in binary files',
            'category': 'Analysis Pipeline',
            'license': 'MIT',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.10.5'
        },
        {
            'name': 'Open Agentic Framework',
            'component_id': 'open-agentic-framework',
            'github': 'https://github.com/oscarvalenzuelab/open_agentic_framework',
            'pypi': None,
            'description': 'Agentic analysis framework for intelligent code pattern detection',
            'category': 'Analysis Pipeline',
            'license': 'Apache-2.0',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.1.0'
        },
        {
            'name': 'OS License Identification Library',
            'component_id': 'semantic-copycat-oslili',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-oslili',
            'pypi': 'semantic-copycat-oslili',
            'description': 'High-performance license detection across 700+ SPDX identifiers with confidence scores',
            'category': 'License Analysis',
            'license': 'Apache-2.0',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.5.1'
        },
        {
            'name': 'PURL to Notice',
            'component_id': 'semantic-copycat-purl2notice',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2notices',
            'pypi': 'semantic-copycat-purl2notices',
            'description': 'Generates legal notices with licenses and copyright information',
            'category': 'License Analysis',
            'license': 'MIT',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.2.0'
        },
        {
            'name': 'CCDA',
            'component_id': 'semantic-copycat-ccda',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-ccda',
            'pypi': None,
            'description': 'Code Copycat Defender Advisory - Evolution of OSSA Scanner for semantic code copycat detection and advisory generation',
            'category': 'License Analysis',
            'license': 'MIT'
        },
        {
            'name': 'UPMEX',
            'component_id': 'semantic-copycat-upmex',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-upmex',
            'pypi': 'semantic-copycat-upmex',
            'description': 'Universal package metadata extractor supporting 13 package ecosystems',
            'category': 'Analysis Pipeline',
            'license': 'MIT',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.6.2'
        },
        {
            'name': 'Source To ID',
            'component_id': 'semantic-copycat-src2id',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-src2id',
            'pypi': 'semantic-copycat-src2id',
            'description': 'Identifies package coordinates from source code using SWHIDs and multiple strategies',
            'category': 'Analysis Pipeline',
            'license': 'AGPL-3.0',
            'status_override': 'complete',
            'completion_override': 100.0,
            'version_override': '1.3.1'
        },
        {
            'name': 'PURL2Risk',
            'component_id': 'semantic-copycat-purl2risk',
            'github': 'https://github.com/oscarvalenzuelab/semantic-copycat-purl2risk',
            'pypi': None,
            'description': 'Comprehensive risk intelligence including CVEs, business continuity, and OSS health metrics',
            'category': 'Risk Analysis',
            'license': 'MIT'
        }
    ]
    
    # Fetch stats for all components
    component_stats = []
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
                    
                    if component.get('completion_override') is None:
                        if stats['total_issues'] > 0:
                            stats['completion'] = calculate_completion(stats['closed_issues'], stats['total_issues'])
                        elif stats['github_exists'] and stats['version'] != '0.0.0':
                            stats['completion'] = 100.0
                        elif stats['github_exists']:
                            stats['completion'] = 10.0
        
        # Fetch PyPI stats if applicable
        if component.get('pypi'):
            pypi_stats = fetch_pypi_stats(component['pypi'])
            if pypi_stats:
                stats['pypi_exists'] = pypi_stats.get('exists', False)
                if pypi_stats.get('version', '0.0.0') != '0.0.0':
                    stats['version'] = pypi_stats['version']
                    if stats['completion'] == 0.0 and stats['pypi_exists']:
                        stats['completion'] = 100.0
        
        # Handle manual status overrides
        if stats['status_override'] == 'complete':
            stats['completion'] = component.get('completion_override', 100.0)
            stats['github_exists'] = True
            if component.get('version_override'):
                stats['version'] = component['version_override']
        elif stats['status_override'] == 'functional':
            stats['completion'] = component.get('completion_override', 80.0)
            stats['github_exists'] = True
            if component.get('version_override'):
                stats['version'] = component['version_override']
        
        # Count ready components
        if stats['version'] != '0.0.0' or stats['github_exists'] or stats['status_override'] in ['complete', 'functional']:
            total_components_ready += 1
        
        component_stats.append(stats)
    
    # Calculate overall completion
    overall_completion = (total_components_ready / len(components)) * 100
    
    # Read existing HTML as template
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # Update the overall progress - look for stat-number instead of stat-value
    html_content = re.sub(
        r'<div class="stat-number">\d+\.?\d*%</div>',
        f'<div class="stat-number">{overall_completion:.0f}%</div>',
        html_content,
        count=1
    )
    
    # Update ready count - find the 4th stat-number (the one after 8)
    stat_numbers = re.findall(r'<div class="stat-number">(\d+)</div>', html_content)
    if len(stat_numbers) >= 2:
        # Replace the 3rd occurrence (Ready count)
        pattern = r'(<div class="stat-number">8</div>.*?<div class="stat-number">)\d+(</div>)'
        html_content = re.sub(pattern, f'\\g<1>{total_components_ready}\\g<2>', html_content, flags=re.DOTALL)
        
        # Replace the 4th occurrence (In Development count)
        in_dev = len(components) - total_components_ready
        pattern = r'(<div class="stat-number">' + str(total_components_ready) + r'</div>.*?<div class="stat-number">)\d+(</div>)'
        html_content = re.sub(pattern, f'\\g<1>{in_dev}\\g<2>', html_content, flags=re.DOTALL)
    
    # Generate component cards HTML
    component_cards_html = ""
    for stats in component_stats:
        is_ready = (stats['version'] != '0.0.0' or 
                   stats.get('status_override') in ['complete', 'functional'] or 
                   stats['completion'] >= 80.0)
        
        status_class = "status-ready" if is_ready else "status-development"
        status_text = "Ready" if is_ready else "In Dev"
        
        links_html = ""
        if stats['github_url']:
            if stats['github_exists'] or stats.get('status_override') == 'complete':
                links_html += f'                        <a href="{stats["github_url"]}">🔗 GitHub</a>\n'
        if stats['pypi_url'] and stats['pypi_exists']:
            links_html += f'                        <a href="{stats["pypi_url"]}">📦 PyPI</a>\n'
        
        component_cards_html += f"""                <div class="component-card">
                    <div class="component-header">
                        <span class="component-name">{stats['name']}</span>
                        <span class="component-status {status_class}">{status_text}</span>
                    </div>
                    <p class="component-desc">{stats['description']}</p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {stats['completion']:.0f}%"></div>
                    </div>
                    <small>Version: {stats['version']} | License: {stats['license']}</small>
"""
        if links_html:
            component_cards_html += f"""                    <div class="component-links">
{links_html}                    </div>
"""
        component_cards_html += """                </div>
                
"""
    
    # Find and replace the components section
    pattern = r'(<div class="component-grid">)(.*?)(</div>\s*</section>)'
    replacement = f'\\1\n{component_cards_html}            \\3'
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Update the last updated timestamp
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    html_content = re.sub(
        r'Last updated: [^<]+',
        f'Last updated: {timestamp}',
        html_content
    )
    
    # Write updated HTML
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print(f"✅ index.html updated successfully!")
    print(f"📊 Overall completion: {overall_completion:.0f}%")
    print(f"🎯 Components ready: {total_components_ready}/{len(components)}")

if __name__ == "__main__":
    generate_html()