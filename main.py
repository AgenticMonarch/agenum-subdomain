from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import dns.resolver
import asyncio
import aiohttp
from typing import List, Set
import re

app = FastAPI(
    title="Subdomain Discovery Service",
    description="A SaaS service to discover subdomains for a given domain",
    version="1.0.0"
)

class DomainRequest(BaseModel):
    domain: str
    
    @validator('domain')
    def validate_domain(cls, v):
        # Basic domain validation
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(domain_pattern, v):
            raise ValueError('Invalid domain format')
        return v.lower()

class SubdomainResponse(BaseModel):
    domain: str
    subdomains: List[str]
    total_found: int

class SubdomainDiscovery:
    def __init__(self):
        # Common subdomain wordlist
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mx', 'test', 'dev',
            'staging', 'api', 'admin', 'blog', 'shop', 'forum', 'support', 'help',
            'secure', 'ssl', 'vpn', 'remote', 'demo', 'beta', 'alpha', 'mobile',
            'app', 'cdn', 'static', 'media', 'images', 'img', 'assets', 'files'
        ]
    
    async def dns_lookup(self, subdomain: str, domain: str) -> bool:
        """Check if subdomain exists via DNS lookup"""
        try:
            full_domain = f"{subdomain}.{domain}"
            resolver = dns.resolver.Resolver()
            resolver.timeout = 2
            resolver.lifetime = 2
            
            # Try A record
            try:
                resolver.resolve(full_domain, 'A')
                return True
            except:
                pass
            
            # Try CNAME record
            try:
                resolver.resolve(full_domain, 'CNAME')
                return True
            except:
                pass
                
        except Exception:
            pass
        return False
    
    async def discover_subdomains(self, domain: str) -> Set[str]:
        """Discover subdomains using DNS enumeration"""
        found_subdomains = set()
        
        # Create tasks for concurrent DNS lookups
        tasks = []
        for subdomain in self.common_subdomains:
            task = asyncio.create_task(self.dns_lookup(subdomain, domain))
            tasks.append((subdomain, task))
        
        # Wait for all tasks to complete
        for subdomain, task in tasks:
            try:
                if await task:
                    found_subdomains.add(f"{subdomain}.{domain}")
            except Exception:
                continue
        
        return found_subdomains

# Initialize subdomain discovery service
subdomain_service = SubdomainDiscovery()

@app.get("/")
async def root():
    return {
        "message": "Subdomain Discovery Service",
        "endpoints": {
            "discover": "/discover",
            "health": "/health"
        }
    }

@app.post("/discover", response_model=SubdomainResponse)
async def discover_subdomains(request: DomainRequest):
    """
    Discover subdomains for a given domain
    """
    try:
        subdomains = await subdomain_service.discover_subdomains(request.domain)
        
        return SubdomainResponse(
            domain=request.domain,
            subdomains=sorted(list(subdomains)),
            total_found=len(subdomains)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error discovering subdomains: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "subdomain-discovery"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)