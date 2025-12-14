"""
Threat Feed Service - Fetches and processes security threat intelligence
"""
import os
import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict


class ThreatFeedService:
    """Service for fetching and processing CVE threat intelligence"""
    
    def __init__(self):
        self.nvd_api_key = os.getenv("NVD_API_KEY", "")
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
    
    async def fetch_recent_cves(self, days: int = 7, limit: int = 50) -> List[Dict]:
        """
        Fetch recent CVEs from NVD API
        
        Args:
            days: Number of days to look back
            limit: Maximum number of CVEs to return
            
        Returns:
            List of CVE dictionaries with processed data
        """
        cache_key = f"recent_cves_{days}_{limit}"
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if (datetime.now() - cached_time).seconds < self.cache_duration:
                return cached_data
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for API (ISO 8601)
        pub_start = start_date.strftime("%Y-%m-%dT00:00:00.000")
        pub_end = end_date.strftime("%Y-%m-%dT23:59:59.999")
        
        headers = {}
        if self.nvd_api_key:
            headers["apiKey"] = self.nvd_api_key
        
        params = {
            "pubStartDate": pub_start,
            "pubEndDate": pub_end,
            "resultsPerPage": limit
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                # Process CVEs
                cves = []
                for item in data.get("vulnerabilities", [])[:limit]:
                    cve_data = item.get("cve", {})
                    cve_id = cve_data.get("id", "")
                    
                    # Extract description
                    descriptions = cve_data.get("descriptions", [])
                    description = ""
                    if descriptions:
                        description = descriptions[0].get("value", "")
                    
                    # Extract CVSS score and severity
                    metrics = cve_data.get("metrics", {})
                    cvss_score = 0.0
                    severity = "UNKNOWN"
                    
                    # Try CVSS v3.1 first, then v3.0, then v2.0
                    for version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                        if version in metrics and metrics[version]:
                            metric = metrics[version][0]
                            cvss_data = metric.get("cvssData", {})
                            cvss_score = cvss_data.get("baseScore", 0.0)
                            severity = cvss_data.get("baseSeverity", metric.get("baseSeverity", "UNKNOWN"))
                            break
                    
                    # Published date
                    published = cve_data.get("published", "")
                    
                    # References
                    references = []
                    for ref in cve_data.get("references", [])[:3]:
                        references.append({
                            "url": ref.get("url", ""),
                            "source": ref.get("source", "")
                        })
                    
                    cves.append({
                        "id": cve_id,
                        "description": description[:300] + "..." if len(description) > 300 else description,
                        "cvss_score": cvss_score,
                        "severity": severity.upper(),
                        "published": published,
                        "references": references
                    })
                
                # Cache results
                self.cache[cache_key] = (datetime.now(), cves)
                return cves
                
        except Exception as e:
            print(f"Error fetching CVEs: {e}")
            # Return mock data for development/demo
            return self._get_mock_cves(limit)
    
    async def get_severity_distribution(self, days: int = 30) -> Dict:
        """
        Get distribution of CVE severities for radar chart
        
        Returns:
            Dictionary with severity counts and percentages
        """
        cves = await self.fetch_recent_cves(days=days, limit=200)
        
        severity_counts = defaultdict(int)
        for cve in cves:
            severity_counts[cve["severity"]] += 1
        
        total = len(cves)
        
        return {
            "labels": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            "data": [
                severity_counts.get("CRITICAL", 0),
                severity_counts.get("HIGH", 0),
                severity_counts.get("MEDIUM", 0),
                severity_counts.get("LOW", 0)
            ],
            "percentages": [
                round(severity_counts.get("CRITICAL", 0) / total * 100, 1) if total > 0 else 0,
                round(severity_counts.get("HIGH", 0) / total * 100, 1) if total > 0 else 0,
                round(severity_counts.get("MEDIUM", 0) / total * 100, 1) if total > 0 else 0,
                round(severity_counts.get("LOW", 0) / total * 100, 1) if total > 0 else 0
            ],
            "total": total
        }
    
    async def get_category_distribution(self, days: int = 30) -> Dict:
        """
        Get threat distribution by category for radar chart
        Categorizes based on CVE description keywords
        
        Returns:
            Dictionary with category data for radar chart
        """
        cves = await self.fetch_recent_cves(days=days, limit=200)
        
        categories = {
            "Web Application": ["xss", "sql injection", "csrf", "web", "http"],
            "Network": ["network", "protocol", "tcp", "udp", "dns"],
            "Authentication": ["authentication", "password", "credential", "login"],
            "Privilege Escalation": ["privilege", "escalation", "root", "admin"],
            "Code Execution": ["remote code execution", "rce", "execute", "arbitrary code"],
            "Data Exposure": ["information disclosure", "data leak", "exposure", "sensitive"]
        }
        
        category_counts = defaultdict(int)
        
        for cve in cves:
            desc = cve["description"].lower()
            for category, keywords in categories.items():
                if any(keyword in desc for keyword in keywords):
                    category_counts[category] += 1
                    break
            else:
                category_counts["Other"] += 1
        
        return {
            "labels": list(categories.keys()),
            "data": [category_counts.get(cat, 0) for cat in categories.keys()]
        }
    
    def _get_mock_cves(self, limit: int = 50) -> List[Dict]:
        """Return mock CVE data for development/demo purposes"""
        mock_cves = [
            {
                "id": "CVE-2024-12345",
                "description": "Critical SQL injection vulnerability in web application framework allowing remote attackers to execute arbitrary SQL commands",
                "cvss_score": 9.8,
                "severity": "CRITICAL",
                "published": "2024-12-13T10:00:00.000",
                "references": [
                    {"url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12345", "source": "NVD"}
                ]
            },
            {
                "id": "CVE-2024-12346",
                "description": "Remote code execution vulnerability in popular CMS platform affecting versions 3.0 to 3.5",
                "cvss_score": 9.1,
                "severity": "CRITICAL",
                "published": "2024-12-12T15:30:00.000",
                "references": [
                    {"url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12346", "source": "NVD"}
                ]
            },
            {
                "id": "CVE-2024-12347",
                "description": "Cross-site scripting (XSS) vulnerability in authentication module",
                "cvss_score": 7.5,
                "severity": "HIGH",
                "published": "2024-12-11T09:15:00.000",
                "references": [
                    {"url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12347", "source": "NVD"}
                ]
            },
            {
                "id": "CVE-2024-12348",
                "description": "Privilege escalation vulnerability in Linux kernel affecting multiple distributions",
                "cvss_score": 8.4,
                "severity": "HIGH",
                "published": "2024-12-10T14:20:00.000",
                "references": [
                    {"url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12348", "source": "NVD"}
                ]
            },
            {
                "id": "CVE-2024-12349",
                "description": "Information disclosure vulnerability in API endpoint exposing sensitive user data",
                "cvss_score": 5.3,
                "severity": "MEDIUM",
                "published": "2024-12-09T11:45:00.000",
                "references": [
                    {"url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12349", "source": "NVD"}
                ]
            },
            {
                "id": "CVE-2024-12350",
                "description": "Denial of service vulnerability in network service allowing resource exhaustion",
                "cvss_score": 6.5,
                "severity": "MEDIUM",
                "published": "2024-12-08T16:00:00.000",
                "references": [
                    {"url": "https://nvd.nist.gov/vuln/detail/CVE-2024-12350", "source": "NVD"}
                ]
            }
        ]
        
        return mock_cves[:limit]
