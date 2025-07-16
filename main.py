from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import asyncio
import aiohttp
import socket
import subprocess
import json
import re
from typing import List, Set, Optional, Tuple
from urllib.parse import quote
from bs4 import BeautifulSoup

app = FastAPI(
    title="Advanced Subdomain Discovery Service",
    description="A comprehensive SaaS service to discover subdomains using multiple methods",
    version="2.0.0"
)

class DomainRequest(BaseModel):
    domain: str
    methods: Optional[List[str]] = ["dns", "crt"]
    
    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v):
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(domain_pattern, v):
            raise ValueError('Invalid domain format')
        return v.lower()
    
    @field_validator('methods')
    @classmethod
    def validate_methods(cls, v):
        valid_methods = ["dns", "crt", "hackertarget", "threatcrowd", "virustotal"]
        if v:
            for method in v:
                if method not in valid_methods:
                    raise ValueError(f'Invalid method: {method}. Valid methods: {valid_methods}')
        return v or ["dns", "crt"]

class SubdomainResponse(BaseModel):
    domain: str
    subdomains: List[str]
    total_found: int
    methods_used: List[str]
    results_by_method: dict

class AdvancedSubdomainDiscovery:
    def __init__(self):
        # Expanded subdomain wordlist
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mx', 'test', 'dev',
            'staging', 'api', 'admin', 'blog', 'shop', 'forum', 'support', 'help',
            'secure', 'ssl', 'vpn', 'remote', 'demo', 'beta', 'alpha', 'mobile',
            'app', 'cdn', 'static', 'media', 'images', 'img', 'assets', 'files',
            'portal', 'server', 'ns', 'email', 'cloud', 'backup', 'mysql', 'sql',
            'database', 'db', 'ftp2', 'ns3', 'dns', 'search', 'login', 'panel',
            'control', 'secure2', 'admin2', 'test2', 'demo2', 'beta2', 'alpha2',
            'old', 'new', 'web', 'web1', 'web2', 'home', 'my', 'all', 'mobile2',
            'store', 'news', 'download', 'upload', 'video', 'music', 'game', 'chat'
        ]
    
    async def dns_lookup(self, subdomain: str, domain: str) -> bool:
        """Check if subdomain exists via DNS lookup"""
        try:
            full_domain = f"{subdomain}.{domain}"
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, socket.gethostbyname, full_domain)
            return True
        except (socket.gaierror, socket.herror, OSError):
            return False
        except Exception:
            return False
    
    async def dns_discovery(self, domain: str) -> Set[str]:
        """Discover subdomains using DNS enumeration"""
        found_subdomains = set()
        
        # Create semaphore to limit concurrent DNS requests
        semaphore = asyncio.Semaphore(50)
        
        async def check_subdomain(subdomain):
            async with semaphore:
                if await self.dns_lookup(subdomain, domain):
                    return f"{subdomain}.{domain}"
                return None
        
        tasks = [check_subdomain(sub) for sub in self.common_subdomains]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result and not isinstance(result, Exception):
                found_subdomains.add(result)
        
        return found_subdomains
    
    async def certificate_transparency_discovery(self, domain: str) -> Set[str]:
        """Discover subdomains using Certificate Transparency logs - Most reliable method"""
        found_subdomains = set()
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            # Try multiple CT log sources
            urls = [
                f"https://crt.sh/?q=%.{domain}&output=json",
                f"https://crt.sh/?q={domain}&output=json"
            ]
            
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                for url in urls:
                    try:
                        print(f"Querying Certificate Transparency: {url}")
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                print(f"Found {len(data)} certificates")
                                
                                for cert in data:
                                    name_value = cert.get('name_value', '')
                                    # Split by newlines as multiple domains can be in one certificate
                                    for name in name_value.split('\n'):
                                        name = name.strip().lower()
                                        # Filter valid subdomains
                                        if (name.endswith(f'.{domain}') and 
                                            '*' not in name and 
                                            name != domain and
                                            len(name.split('.')) >= 2):
                                            found_subdomains.add(name)
                            else:
                                print(f"CT API returned status: {response.status}")
                    except Exception as e:
                        print(f"Error querying {url}: {e}")
                        continue
        
        except Exception as e:
            print(f"Certificate transparency error: {e}")
        
        print(f"Certificate Transparency found {len(found_subdomains)} subdomains")
        return found_subdomains
    
    async def hackertarget_discovery(self, domain: str) -> Set[str]:
        """Discover subdomains using HackerTarget API"""
        found_subdomains = set()
        
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            timeout = aiohttp.ClientTimeout(total=15)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        lines = text.strip().split('\n')
                        
                        for line in lines:
                            if ',' in line:
                                subdomain = line.split(',')[0].strip()
                                if subdomain.endswith(f'.{domain}') and subdomain != domain:
                                    found_subdomains.add(subdomain)
        
        except Exception as e:
            print(f"HackerTarget error: {e}")
        
        return found_subdomains
    
    async def threatcrowd_discovery(self, domain: str) -> Set[str]:
        """Discover subdomains using ThreatCrowd API"""
        found_subdomains = set()
        
        try:
            url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
            timeout = aiohttp.ClientTimeout(total=15)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        subdomains = data.get('subdomains', [])
                        
                        for subdomain in subdomains:
                            if subdomain and subdomain != domain:
                                found_subdomains.add(subdomain)
        
        except Exception as e:
            print(f"ThreatCrowd error: {e}")
        
        return found_subdomains
    
    async def virustotal_discovery(self, domain: str) -> Set[str]:
        """Discover subdomains using VirusTotal API (public, no key needed)"""
        found_subdomains = set()
        
        try:
            # Note: This is a public endpoint that doesn't require API key
            url = f"https://www.virustotal.com/vtapi/v2/domain/report"
            params = {
                'apikey': 'public',  # Some endpoints work without real key
                'domain': domain
            }
            timeout = aiohttp.ClientTimeout(total=15)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        subdomains = data.get('subdomains', [])
                        
                        for subdomain in subdomains:
                            if subdomain and subdomain.endswith(f'.{domain}'):
                                found_subdomains.add(subdomain)
        
        except Exception as e:
            print(f"VirusTotal error: {e}")
        
        return found_subdomains
    
    async def discover_subdomains(self, domain: str, methods: List[str]) -> Tuple[Set[str], dict]:
        """Discover subdomains using multiple methods"""
        all_subdomains = set()
        results_by_method = {}
        
        # Create tasks for selected methods
        tasks = []
        
        if "dns" in methods:
            tasks.append(("dns", self.dns_discovery(domain)))
        
        if "crt" in methods:
            tasks.append(("crt", self.certificate_transparency_discovery(domain)))
        
        if "hackertarget" in methods:
            tasks.append(("hackertarget", self.hackertarget_discovery(domain)))
        
        if "threatcrowd" in methods:
            tasks.append(("threatcrowd", self.threatcrowd_discovery(domain)))
        
        if "virustotal" in methods:
            tasks.append(("virustotal", self.virustotal_discovery(domain)))
        
        # Execute all methods concurrently
        for method_name, task in tasks:
            try:
                print(f"Running {method_name} discovery...")
                method_results = await task
                results_by_method[method_name] = sorted(list(method_results))
                all_subdomains.update(method_results)
                print(f"{method_name} found {len(method_results)} subdomains")
            except Exception as e:
                print(f"Error in {method_name}: {e}")
                results_by_method[method_name] = []
        
        return all_subdomains, results_by_method

# Initialize subdomain discovery service
subdomain_service = AdvancedSubdomainDiscovery()

@app.get("/")
async def root():
    return {
        "message": "Advanced Subdomain Discovery Service",
        "version": "2.0.0",
        "available_methods": ["dns", "crt", "hackertarget", "threatcrowd", "virustotal"],
        "endpoints": {
            "discover": "/discover",
            "health": "/health",
            "methods": "/methods"
        }
    }

@app.get("/methods")
async def get_methods():
    return {
        "available_methods": {
            "dns": "DNS enumeration using common subdomain wordlist (fast, reliable)",
            "crt": "Certificate Transparency logs via crt.sh (most comprehensive)",
            "hackertarget": "HackerTarget API (good coverage, free)",
            "threatcrowd": "ThreatCrowd API (threat intelligence data)",
            "virustotal": "VirusTotal API (security-focused results)"
        },
        "recommendations": {
            "fast": ["dns", "crt"],
            "comprehensive": ["dns", "crt", "hackertarget", "threatcrowd"],
            "best_single": ["crt"]
        }
    }

@app.post("/discover", response_model=SubdomainResponse)
async def discover_subdomains(request: DomainRequest):
    """
    Discover subdomains using multiple advanced methods
    """
    try:
        print(f"Starting subdomain discovery for {request.domain} using methods: {request.methods}")
        
        subdomains, results_by_method = await subdomain_service.discover_subdomains(
            request.domain, 
            request.methods
        )
        
        print(f"Total unique subdomains found: {len(subdomains)}")
        
        return SubdomainResponse(
            domain=request.domain,
            subdomains=sorted(list(subdomains)),
            total_found=len(subdomains),
            methods_used=request.methods,
            results_by_method=results_by_method
        )
    
    except Exception as e:
        print(f"Error in discover_subdomains: {e}")
        raise HTTPException(status_code=500, detail=f"Error discovering subdomains: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "advanced-subdomain-discovery"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)