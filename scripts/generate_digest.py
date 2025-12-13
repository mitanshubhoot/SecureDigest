#!/usr/bin/env python3
"""
Generate a daily risk digest for today's date.
Uses deterministic seeding based on date to ensure stable output if rerun.
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Security/VRM themed digest items pool
DIGEST_POOL = [
    {
        "type": "tip",
        "title": "Enable DNSSEC for your domain",
        "why": "DNSSEC prevents DNS spoofing attacks by cryptographically signing DNS records",
        "fix": "Contact your DNS provider to enable DNSSEC and add DS records to your registrar"
    },
    {
        "type": "check",
        "title": "Verify SPF records are configured",
        "why": "SPF records prevent email spoofing by specifying which servers can send email for your domain",
        "fix": "Add a TXT record: 'v=spf1 include:_spf.google.com ~all' (adjust for your mail provider)"
    },
    {
        "type": "pattern",
        "title": "Implement DMARC policy",
        "why": "DMARC builds on SPF and DKIM to give domain owners control over email authentication",
        "fix": "Add TXT record: 'v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com'"
    },
    {
        "type": "tip",
        "title": "Use HSTS headers",
        "why": "HTTP Strict Transport Security forces browsers to only connect via HTTPS",
        "fix": "Add header: 'Strict-Transport-Security: max-age=31536000; includeSubDomains'"
    },
    {
        "type": "check",
        "title": "Scan for exposed .git directories",
        "why": "Exposed .git folders can leak source code and sensitive configuration",
        "fix": "Block access in web server config or use .htaccess: 'RedirectMatch 404 /\\.git'"
    },
    {
        "type": "pattern",
        "title": "Rotate API keys quarterly",
        "why": "Regular rotation limits the window of exposure if keys are compromised",
        "fix": "Set calendar reminders and use secret management tools like HashiCorp Vault"
    },
    {
        "type": "tip",
        "title": "Enable MFA for all admin accounts",
        "why": "Multi-factor authentication prevents account takeover even if passwords are stolen",
        "fix": "Use authenticator apps (Google Authenticator, Authy) or hardware keys (YubiKey)"
    },
    {
        "type": "check",
        "title": "Review third-party vendor access",
        "why": "Excessive vendor permissions increase attack surface and compliance risk",
        "fix": "Audit vendor access quarterly and apply principle of least privilege"
    },
    {
        "type": "pattern",
        "title": "Implement Content Security Policy",
        "why": "CSP headers prevent XSS attacks by controlling which resources can load",
        "fix": "Start with: 'Content-Security-Policy: default-src 'self'; script-src 'self''"
    },
    {
        "type": "tip",
        "title": "Use TLS 1.3 exclusively",
        "why": "Older TLS versions have known vulnerabilities and weaker cipher suites",
        "fix": "Update server config to disable TLS 1.0, 1.1, 1.2 and enable only TLS 1.3"
    },
    {
        "type": "check",
        "title": "Verify backup encryption",
        "why": "Unencrypted backups are a major data breach risk if storage is compromised",
        "fix": "Enable encryption at rest and in transit for all backup solutions"
    },
    {
        "type": "pattern",
        "title": "Implement rate limiting on APIs",
        "why": "Rate limits prevent brute force attacks and API abuse",
        "fix": "Use middleware like express-rate-limit or nginx limit_req module"
    },
    {
        "type": "tip",
        "title": "Scan dependencies for vulnerabilities",
        "why": "Vulnerable dependencies are a common attack vector in supply chain attacks",
        "fix": "Use tools like npm audit, pip-audit, or Snyk in your CI/CD pipeline"
    },
    {
        "type": "check",
        "title": "Remove default credentials",
        "why": "Default passwords are publicly known and exploited by automated scanners",
        "fix": "Change all default passwords immediately after deployment"
    },
    {
        "type": "pattern",
        "title": "Use parameterized queries",
        "why": "Parameterized queries prevent SQL injection attacks",
        "fix": "Never concatenate user input into SQL; use prepared statements instead"
    },
    {
        "type": "tip",
        "title": "Enable audit logging",
        "why": "Audit logs are essential for incident response and compliance",
        "fix": "Log authentication events, data access, and configuration changes"
    },
    {
        "type": "check",
        "title": "Verify CORS configuration",
        "why": "Misconfigured CORS can allow unauthorized cross-origin requests",
        "fix": "Explicitly whitelist allowed origins instead of using '*'"
    },
    {
        "type": "pattern",
        "title": "Implement session timeout",
        "why": "Long-lived sessions increase risk of session hijacking",
        "fix": "Set session timeout to 15-30 minutes for sensitive applications"
    },
    {
        "type": "tip",
        "title": "Use security headers scanner",
        "why": "Missing security headers leave applications vulnerable to common attacks",
        "fix": "Use securityheaders.com to scan and implement recommended headers"
    },
    {
        "type": "check",
        "title": "Disable directory listing",
        "why": "Directory listing exposes file structure and sensitive files",
        "fix": "Set 'Options -Indexes' in Apache or 'autoindex off' in nginx"
    },
    {
        "type": "pattern",
        "title": "Implement password complexity requirements",
        "why": "Weak passwords are easily cracked by brute force attacks",
        "fix": "Require minimum 12 characters with mix of uppercase, lowercase, numbers, symbols"
    },
    {
        "type": "tip",
        "title": "Use environment variables for secrets",
        "why": "Hardcoded secrets in code are exposed in version control",
        "fix": "Store secrets in .env files (gitignored) or secret management services"
    },
    {
        "type": "check",
        "title": "Verify SSL certificate validity",
        "why": "Expired certificates break HTTPS and expose users to MITM attacks",
        "fix": "Set up automated renewal with Let's Encrypt or monitor expiry dates"
    },
    {
        "type": "pattern",
        "title": "Implement input validation",
        "why": "Unvalidated input leads to injection attacks and data corruption",
        "fix": "Validate all user input on both client and server side"
    },
    {
        "type": "tip",
        "title": "Use secure cookie flags",
        "why": "Insecure cookies can be stolen via XSS or transmitted over HTTP",
        "fix": "Set HttpOnly, Secure, and SameSite flags on all cookies"
    },
    {
        "type": "check",
        "title": "Review firewall rules",
        "why": "Overly permissive firewall rules expose unnecessary services",
        "fix": "Apply principle of least privilege and close unused ports"
    },
    {
        "type": "pattern",
        "title": "Implement security incident response plan",
        "why": "Prepared response reduces damage and recovery time from breaches",
        "fix": "Document procedures, assign roles, and conduct regular drills"
    },
    {
        "type": "tip",
        "title": "Enable database encryption at rest",
        "why": "Unencrypted databases are vulnerable if storage media is compromised",
        "fix": "Enable Transparent Data Encryption (TDE) or equivalent for your database"
    },
    {
        "type": "check",
        "title": "Verify patch management process",
        "why": "Unpatched systems are vulnerable to known exploits",
        "fix": "Establish regular patching schedule and test updates before deployment"
    },
    {
        "type": "pattern",
        "title": "Use principle of least privilege",
        "why": "Excessive permissions increase blast radius of compromised accounts",
        "fix": "Grant only minimum necessary permissions for each role"
    },
    {
        "type": "tip",
        "title": "Implement API authentication",
        "why": "Unauthenticated APIs allow unauthorized access to data and functions",
        "fix": "Use OAuth 2.0, JWT tokens, or API keys with proper validation"
    },
    {
        "type": "check",
        "title": "Scan for exposed secrets in repos",
        "why": "Committed secrets can be found by attackers scanning public repositories",
        "fix": "Use tools like git-secrets or truffleHog to scan commit history"
    },
    {
        "type": "pattern",
        "title": "Implement network segmentation",
        "why": "Segmentation limits lateral movement in case of breach",
        "fix": "Separate production, staging, and development networks with firewalls"
    },
    {
        "type": "tip",
        "title": "Use Web Application Firewall (WAF)",
        "why": "WAF protects against common web attacks like SQL injection and XSS",
        "fix": "Deploy CloudFlare, AWS WAF, or ModSecurity"
    },
    {
        "type": "check",
        "title": "Review user access permissions",
        "why": "Stale permissions from former employees pose security risk",
        "fix": "Conduct quarterly access reviews and remove unnecessary permissions"
    },
    {
        "type": "pattern",
        "title": "Implement security awareness training",
        "why": "Human error is the leading cause of security incidents",
        "fix": "Conduct quarterly phishing simulations and security training"
    },
    {
        "type": "tip",
        "title": "Use secure file upload validation",
        "why": "Malicious file uploads can lead to remote code execution",
        "fix": "Validate file types, scan for malware, and store uploads outside webroot"
    },
    {
        "type": "check",
        "title": "Verify encryption in transit",
        "why": "Unencrypted data transmission exposes sensitive information",
        "fix": "Enforce HTTPS for all endpoints and use TLS for internal services"
    },
    {
        "type": "pattern",
        "title": "Implement zero trust architecture",
        "why": "Zero trust assumes breach and verifies every access request",
        "fix": "Require authentication for all resources regardless of network location"
    },
    {
        "type": "tip",
        "title": "Use security linters in CI/CD",
        "why": "Automated security checks catch vulnerabilities before deployment",
        "fix": "Integrate tools like Bandit (Python), ESLint security plugin (JS)"
    },
    {
        "type": "check",
        "title": "Verify container image security",
        "why": "Vulnerable base images introduce security risks to containerized apps",
        "fix": "Scan images with Trivy or Clair and use minimal base images"
    },
    {
        "type": "pattern",
        "title": "Implement data classification",
        "why": "Classification ensures appropriate security controls for sensitive data",
        "fix": "Label data as public, internal, confidential, or restricted"
    },
    {
        "type": "tip",
        "title": "Use secure random number generation",
        "why": "Weak randomness compromises cryptographic operations",
        "fix": "Use crypto.randomBytes() or secrets module, not Math.random()"
    },
    {
        "type": "check",
        "title": "Review cloud storage permissions",
        "why": "Misconfigured S3 buckets and storage accounts lead to data leaks",
        "fix": "Ensure buckets are private and use IAM policies for access control"
    },
    {
        "type": "pattern",
        "title": "Implement security monitoring",
        "why": "Real-time monitoring detects attacks and anomalies early",
        "fix": "Use SIEM tools and set up alerts for suspicious activities"
    },
    {
        "type": "tip",
        "title": "Use subresource integrity (SRI)",
        "why": "SRI prevents compromised CDN resources from executing malicious code",
        "fix": "Add integrity attribute to script and link tags loading external resources"
    },
    {
        "type": "check",
        "title": "Verify mobile app security",
        "why": "Mobile apps often have unique vulnerabilities like insecure storage",
        "fix": "Use OWASP Mobile Security Testing Guide for comprehensive testing"
    },
    {
        "type": "pattern",
        "title": "Implement disaster recovery plan",
        "why": "Disasters and ransomware require tested recovery procedures",
        "fix": "Document RTO/RPO, maintain offline backups, and test recovery quarterly"
    },
    {
        "type": "tip",
        "title": "Use security champions program",
        "why": "Embedded security advocates improve security culture across teams",
        "fix": "Designate security champions in each team and provide training"
    },
    {
        "type": "check",
        "title": "Verify API versioning strategy",
        "why": "Deprecated API versions may have unpatched vulnerabilities",
        "fix": "Maintain clear deprecation timeline and force upgrades for old versions"
    },
    {
        "type": "pattern",
        "title": "Implement secure software development lifecycle",
        "why": "Security integrated throughout SDLC is more effective than bolt-on security",
        "fix": "Include threat modeling, security reviews, and testing in each phase"
    }
]

HEADLINES = [
    "Strengthen Your Security Posture Today",
    "Essential Security Checks for Modern Apps",
    "Protect Your Infrastructure: Daily Reminders",
    "Security Best Practices You Should Know",
    "Harden Your Systems: Today's Focus Areas",
    "Critical Security Patterns to Implement",
    "Your Daily Security Improvement Guide",
    "Build Resilient Systems: Key Practices",
    "Security Fundamentals for Production Systems",
    "Reduce Risk: Today's Security Priorities"
]


def generate_digest(date_str: str) -> dict:
    """Generate a deterministic digest for the given date."""
    # Seed random with date for deterministic output
    seed = int(date_str.replace("-", ""))
    random.seed(seed)
    
    # Select 5-8 items randomly
    num_items = random.randint(5, 8)
    selected_items = random.sample(DIGEST_POOL, num_items)
    
    # Select headline
    headline = random.choice(HEADLINES)
    
    return {
        "date": date_str,
        "headline": headline,
        "digest_items": selected_items
    }


def main():
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Setup paths
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    digests_dir = base_dir / "digests"
    
    # Create digests directory if it doesn't exist
    digests_dir.mkdir(exist_ok=True)
    
    # Check if today's digest already exists
    digest_file = digests_dir / f"{today}.json"
    if digest_file.exists():
        print(f"Digest for {today} already exists. Skipping generation.")
        return 0
    
    # Generate digest
    digest = generate_digest(today)
    
    # Write digest file
    with open(digest_file, "w") as f:
        json.dump(digest, f, indent=2)
    print(f"Generated digest for {today}")
    
    # Update index
    index_file = digests_dir / "index.json"
    if index_file.exists():
        with open(index_file, "r") as f:
            index = json.load(f)
    else:
        index = []
    
    # Add today to index if not already present
    if today not in index:
        index.insert(0, today)  # Add to beginning
        with open(index_file, "w") as f:
            json.dump(index, f, indent=2)
        print(f"Updated index with {today}")
    
    return 0


if __name__ == "__main__":
    exit(main())
