# src/publichost/utils.py
import string
import random
import re

RESERVED_WORDS = {
    # System and admin paths
    'admin', 'administrator', 'root', 'system', 'dashboard', 'console',
    'api', 'auth', 'login', 'dev', 'test', 'staging', 'prod', 'production',
    'internal', 'app', 'host', 'server', 'database', 'db', 'mail', 'smtp',
    'ftp', 'ssh', 'dns', 'mx', 'ns', 'ns1', 'ns2', 'web', 'www', 'control',
    
    # Common service names
    'grafana', 'prometheus', 'kibana', 'jenkins', 'gitlab', 'github', 
    'bitbucket', 'jira', 'confluence', 'wiki', 'docs', 'registry',
    
    # Security related
    'security', 'secure', 'ssl', 'tls', 'vpn', 'firewall', 'proxy',
    'sysadmin', 'webmaster', 'postmaster', 'hostmaster',
    
    # Common subdomains
    'blog', 'shop', 'store', 'support', 'help', 'status', 'metrics',
    'monitor', 'stats', 'analytics', 'cdn', 'assets', 'static', 'media',
    
    # Special terms
    'localhost', 'example', 'test', 'invalid', 'undefined', 'null'
}

def generate_subdomain() -> str:
    """
    Generate a random subdomain that meets all requirements:
    - At least 6 characters long
    - Contains only lowercase letters, numbers, and hyphens
    - Starts and ends with alphanumeric characters
    - Not in reserved words list
    
    Returns:
        str: A safe random subdomain like 'app-x8k2p9'
    """
    # Ensure we start with a letter for better readability
    prefix = 'app-'
    
    # Generate random string for uniqueness (6 chars)
    chars = string.ascii_lowercase + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(6))
    
    # Combine to ensure minimum length and pattern requirements
    subdomain = f"{prefix}{random_part}"
    
    return subdomain