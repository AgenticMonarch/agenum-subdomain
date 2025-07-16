# 🔍 Advanced Subdomain Discovery SaaS Service

A comprehensive FastAPI-based service that discovers subdomains using multiple advanced methods including Certificate Transparency logs, threat intelligence APIs, and DNS enumeration.

## 🚀 Features

- **Multiple Discovery Methods:**
  - 🔍 DNS enumeration with 60+ common subdomains
  - 🔐 Certificate Transparency logs (crt.sh) - Most effective!
  - 🎯 HackerTarget API - Free threat intelligence
  - 🛡️ ThreatCrowd API - Security-focused data
  - 🦠 VirusTotal API - Malware/security insights
- **High Performance** with concurrent processing
- **Method Selection** - choose your discovery approach
- **Detailed Results** showing findings per method
- **Production Ready** with proper error handling

## 📦 Installation & Setup

### Step 1: Clone or Download
```bash
# If you have the files, navigate to the directory
cd your-subdomain-discovery-folder
```

### Step 2: Install Dependencies
```bash
# Install required Python packages
python -m pip install -r requirements.txt
```

### Step 3: Start the Service
```bash
# Run the FastAPI service
python main.py
```

You should see:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 🎯 Step-by-Step Usage Guide

### Method 1: Using curl (Command Line)

#### Basic Discovery (Recommended for beginners)
```bash
# Discover subdomains using the most reliable method (Certificate Transparency)
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "github.com", "methods": ["crt"]}'
```

#### Fast Discovery (DNS + Certificate Transparency)
```bash
# Quick discovery using 2 reliable methods
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "facebook.com", "methods": ["dns", "crt"]}'
```

#### Comprehensive Discovery (All Methods)
```bash
# Maximum coverage using all available methods
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "google.com", "methods": ["dns", "crt", "hackertarget", "threatcrowd", "virustotal"]}'
```

### Method 2: Using Web Browser (Interactive)

1. **Open your browser** and go to: `http://localhost:8000/docs`
2. **Click on "POST /discover"** to expand the endpoint
3. **Click "Try it out"** button
4. **Enter your request** in the JSON format:
   ```json
   {
     "domain": "example.com",
     "methods": ["dns", "crt"]
   }
   ```
5. **Click "Execute"** to run the discovery
6. **View results** in the response section

### Method 3: Using Python Code

```python
import requests
import json

# Basic request
def discover_subdomains(domain, methods=["dns", "crt"]):
    url = "http://localhost:8000/discover"
    data = {
        "domain": domain,
        "methods": methods
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Example usage
result = discover_subdomains("github.com", ["crt"])
print(f"Found {result['total_found']} subdomains:")
for subdomain in result['subdomains']:
    print(f"  - {subdomain}")
```

## � Understanding the Results

### Sample Response
```json
{
  "domain": "github.com",
  "subdomains": [
    "api.github.com",
    "www.github.com",
    "gist.github.com",
    "raw.githubusercontent.com"
  ],
  "total_found": 4,
  "methods_used": ["crt"],
  "results_by_method": {
    "crt": ["api.github.com", "www.github.com", "gist.github.com", "raw.githubusercontent.com"]
  }
}
```

### Response Fields Explained
- **domain**: The target domain you searched
- **subdomains**: List of all unique subdomains found
- **total_found**: Total count of unique subdomains
- **methods_used**: Which discovery methods you selected
- **results_by_method**: Breakdown showing what each method found

## 🎯 Method Selection Guide

### For Beginners - Start Here
```bash
# Use Certificate Transparency only (most reliable, fast)
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "your-target.com", "methods": ["crt"]}'
```

### For Speed (2-5 seconds)
```bash
# DNS + Certificate Transparency
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "your-target.com", "methods": ["dns", "crt"]}'
```

### For Maximum Coverage (10-30 seconds)
```bash
# All methods for comprehensive results
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "your-target.com", "methods": ["dns", "crt", "hackertarget", "threatcrowd"]}'
```

## 🔧 Available Methods Explained

| Method | Speed | Reliability | Coverage | Best For |
|--------|-------|-------------|----------|----------|
| `dns` | ⚡ Fast | 🟢 High | 🔵 Medium | Quick checks |
| `crt` | ⚡ Fast | 🟢 Very High | 🟢 High | **Recommended** |
| `hackertarget` | 🔵 Medium | 🟢 High | 🟢 High | Comprehensive |
| `threatcrowd` | 🔵 Medium | 🟡 Medium | 🔵 Medium | Security focus |
| `virustotal` | 🔴 Slow | 🟡 Medium | 🔵 Medium | Malware research |

## 🎯 Practical Examples

### Example 1: Security Assessment
```bash
# For security testing - use comprehensive methods
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "target-company.com", "methods": ["dns", "crt", "hackertarget"]}'
```

### Example 2: Quick Reconnaissance
```bash
# For quick recon - use fastest reliable method
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "example.com", "methods": ["crt"]}'
```

### Example 3: Research & Analysis
```bash
# For detailed analysis - use all methods
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "research-target.com", "methods": ["dns", "crt", "hackertarget", "threatcrowd", "virustotal"]}'
```

## 🔍 Additional Endpoints

### Check Service Health
```bash
curl http://localhost:8000/health
```

### Get Available Methods
```bash
curl http://localhost:8000/methods
```

### Service Information
```bash
curl http://localhost:8000/
```

## 📈 Expected Results by Domain Type

### Popular Websites (GitHub, Facebook, Google)
- **Certificate Transparency**: 50-200+ subdomains
- **Total with all methods**: 100-500+ subdomains

### Medium Companies
- **Certificate Transparency**: 10-50 subdomains  
- **Total with all methods**: 20-100 subdomains

### Small Websites
- **Certificate Transparency**: 2-10 subdomains
- **Total with all methods**: 5-20 subdomains

## 🚨 Important Notes

### Rate Limiting
- The service implements automatic rate limiting
- Certificate Transparency is unlimited
- Other APIs may have daily limits

### Legal & Ethical Use
- Only scan domains you own or have permission to test
- Respect rate limits and terms of service
- Use for legitimate security research only

### Performance Tips
- Start with `["crt"]` method for best results
- Use `["dns", "crt"]` for balanced speed/coverage
- Save comprehensive scans for important targets

## 🛠️ Troubleshooting

### Service Won't Start
```bash
# Check if dependencies are installed
python -m pip install -r requirements.txt

# Check if port 8000 is available
lsof -i :8000
```

### No Results from APIs
- Certificate Transparency (`crt`) should always work
- Other APIs may be temporarily unavailable
- Try with popular domains like `github.com` first

### Connection Errors
```bash
# Make sure service is running
curl http://localhost:8000/health

# Check if you're using the correct URL
# Should be: http://localhost:8000 (not https)
```

## 🎯 Quick Start Checklist

- [ ] Install dependencies: `python -m pip install -r requirements.txt`
- [ ] Start service: `python main.py`
- [ ] Test with: `curl http://localhost:8000/health`
- [ ] Try discovery: `curl -X POST "http://localhost:8000/discover" -H "Content-Type: application/json" -d '{"domain": "github.com", "methods": ["crt"]}'`
- [ ] Open browser docs: `http://localhost:8000/docs`

## 🚀 Production Deployment

For production use, consider:
- Adding authentication/API keys
- Implementing rate limiting per user
- Using a reverse proxy (nginx)
- Adding monitoring and logging
- Deploying with Docker or cloud services

---

**Ready to discover subdomains? Start with the Certificate Transparency method - it's the most reliable and will give you real results immediately!**