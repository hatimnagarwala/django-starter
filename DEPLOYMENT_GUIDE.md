# Django App Deployment and Update Guide

This document outlines the complete process of updating and deploying changes to a Django application running on Azure Container Apps.

## Table of Contents
- [Initial Setup](#initial-setup)
- [Update and Deployment Workflow](#update-and-deployment-workflow)
- [Step-by-Step Process](#step-by-step-process)
- [Verification Steps](#verification-steps)
- [Troubleshooting](#troubleshooting)

---

## Initial Setup

### Prerequisites
Before starting the update process, ensure you have:

1. **Docker** installed and running
2. **Azure CLI** installed and configured
3. **Git** for version control
4. **Azure Container Registry (ACR)** created
5. **Azure Container Apps Environment** set up

### Project Structure
```
anjuman/
├── myapp/                  # Django application
│   ├── views.py           # Application views (updated)
│   ├── urls.py            # URL routing
│   └── ...
├── myproject/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── requirements.txt       # Python dependencies
├── .dockerignore         # Docker ignore rules
├── .gitignore            # Git ignore rules
└── manage.py             # Django management script
```

---

## Update and Deployment Workflow

### Overview
The deployment pipeline follows these stages:

```
Code Change → Build → Tag → Push to ACR → Update Container App → Verify
```

### Configuration Details

**Azure Resources Used:**
- **Container Registry**: `anjumanmobilereg.azurecr.io`
- **Container App**: `django-app`
- **Resource Group**: `hatimmanagedenv`
- **Environment**: `hatimmanagedenv`
- **Location**: UAE North

**Docker Image:**
- **Local Tag**: `django-app`
- **ACR Tag**: `anjumanmobilereg.azurecr.io/django-app:latest`

**Live Application:**
- **URL**: https://django-app.calmrock-3bce75ae.uaenorth.azurecontainerapps.io/

---

## Step-by-Step Process

### Step 1: Make Code Changes

**Example: Updated the landing page view**

Location: `myapp/views.py`

Changes made:
- Added HTML template with modern styling
- Implemented gradient background
- Added technology badges (Django, Docker, Azure)
- Included CSS animations and glass-morphism effects

```python
def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django Starter</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: white;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            /* ... more styles ... */
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Django Starter App</h1>
            <p>Successfully deployed on Azure Container Apps! ☁️</p>
            <div>
                <span class="badge">✅ Django 5.2.9</span>
                <span class="badge">🐳 Docker</span>
                <span class="badge">☁️ Azure</span>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
```

---

### Step 2: Rebuild Docker Image

After making code changes, rebuild the Docker image locally.

**Command:**
```powershell
docker build -t django-app .
```

**What happens:**
- Docker reads the `Dockerfile`
- Installs Python dependencies from `requirements.txt`
- Copies application code into the image
- Creates a new image with your changes

**Expected Output:**
```
[+] Building 2.8s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [1/5] FROM docker.io/library/python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt /app/
 => [4/5] RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . /app/
 => exporting to image
 => => naming to docker.io/library/django-app:latest
```

**Time taken**: ~2-3 seconds (faster on subsequent builds due to layer caching)

---

### Step 3: Tag Image for Azure Container Registry

Tag the local image with the ACR repository name.

**Command:**
```powershell
docker tag django-app anjumanmobilereg.azurecr.io/django-app:latest
```

**What happens:**
- Creates an alias for your local image
- Prepares it for pushing to Azure Container Registry
- The tag includes: `<registry-name>.azurecr.io/<repository>:<version>`

**Verification:**
```powershell
docker images | grep django-app
```

You should see both tags:
- `django-app:latest`
- `anjumanmobilereg.azurecr.io/django-app:latest`

---

### Step 4: Push Image to Azure Container Registry

Push the tagged image to ACR.

**Command:**
```powershell
docker push anjumanmobilereg.azurecr.io/django-app:latest
```

**What happens:**
- Docker uploads image layers to ACR
- Layers that haven't changed are skipped (efficient)
- New/modified layers are uploaded
- ACR generates a digest for the image

**Expected Output:**
```
The push refers to repository [anjumanmobilereg.azurecr.io/django-app]
a86cabe533f4: Pushed
1733a4cd5954: Layer already exists
f9c2a4bb0cfe: Layer already exists
4dc968c110bc: Pushed
latest: digest: sha256:cd973ef2d5f842d40475e70812db139b5ad5859a2babc18b7b868e2ceaf6f238 size: 856
```

**Time taken**: ~10-30 seconds (depending on changes and network speed)

**Note**: Layers marked "Layer already exists" are not re-uploaded, saving time and bandwidth.

---

### Step 5: Update Azure Container App

Update the Container App to use the new image from ACR.

**Command:**
```powershell
az containerapp update --name django-app --resource-group hatimmanagedenv --image anjumanmobilereg.azurecr.io/django-app:latest
```

**What happens:**
- Azure Container Apps pulls the new image from ACR
- Creates a new revision (or updates existing in Single mode)
- Performs a rolling deployment
- Routes traffic to the new revision once healthy
- Maintains zero downtime during update

**Expected Output:**
```json
{
  "id": "/subscriptions/.../containerapps/django-app",
  "location": "UAE North",
  "name": "django-app",
  "properties": {
    "configuration": {
      "ingress": {
        "fqdn": "django-app.calmrock-3bce75ae.uaenorth.azurecontainerapps.io",
        "targetPort": 8000
      }
    },
    "latestRevisionName": "django-app--0000001",
    "provisioningState": "Succeeded",
    "runningStatus": "Running"
  }
}
```

**Time taken**: ~30-60 seconds for the update to complete

---

### Step 6: Restart Container App Revision (Optional)

Restart the revision to ensure the new image is loaded immediately.

**Command:**
```powershell
az containerapp revision restart --name django-app --resource-group hatimmanagedenv --revision django-app--0000001
```

**What happens:**
- Forces a restart of all replicas
- Ensures latest image is pulled and running
- Helpful if image digest is the same but content changed

**Expected Output:**
```
"Restart succeeded"
```

---

### Step 7: Verify Deployment

Check that the changes are live and the app is healthy.

#### 7.1 Check Revision Status

**Command:**
```powershell
az containerapp revision list --name django-app --resource-group hatimmanagedenv --output table
```

**Expected Output:**
```
CreatedTime                Active    Replicas    TrafficWeight    HealthState    ProvisioningState    Name
-------------------------  --------  ----------  ---------------  -------------  -------------------  -------------------
2025-12-09T13:11:24+00:00  True      1           100              Healthy        Provisioned          django-app--0000001
```

**Verify:**
- ✅ Active: `True`
- ✅ HealthState: `Healthy`
- ✅ TrafficWeight: `100` (all traffic to this revision)
- ✅ ProvisioningState: `Provisioned`

#### 7.2 Check Container App Status

**Command:**
```powershell
az containerapp show --name django-app --resource-group hatimmanagedenv --output table
```

**Expected Output:**
```
Name        Location    ResourceGroup    Fqdn
----------  ----------  ---------------  -----------------------------------------------------------
django-app  UAE North   hatimmanagedenv  django-app.calmrock-3bce75ae.uaenorth.azurecontainerapps.io
```

#### 7.3 View Application Logs (Optional)

**Command:**
```powershell
az containerapp logs show --name django-app --resource-group hatimmanagedenv --follow
```

**What to look for:**
- Django server starting successfully
- No error messages
- Requests being served

#### 7.4 Test the Live Application

**URL**: https://django-app.calmrock-3bce75ae.uaenorth.azurecontainerapps.io/

**Manual Verification:**
- Open the URL in a browser
- Verify the new UI is displayed
- Check that all styling is correct
- Test functionality

**Expected Result:**
- Beautiful gradient background
- Styled container with glass effect
- Technology badges visible
- Animations working

---

### Step 8: Commit Changes to Git

Push your code changes to GitHub for version control.

**Commands:**
```powershell
git add myapp/views.py
git commit -m "Update landing page with styled UI"
git push
```

**Expected Output:**
```
[main c0f8bde] Update landing page with styled UI
 1 file changed, 61 insertions(+), 1 deletion(-)
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 1.11 KiB | 1.11 MiB/s, done.
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/hatimnagarwala/django-starter.git
   b410af0..c0f8bde  main -> main
```

---

## Verification Steps

### Complete Verification Checklist

- [ ] **Code Changes Applied**: Verify changes in source files
- [ ] **Docker Image Built**: Local image created successfully
- [ ] **Image Tagged**: ACR tag applied correctly
- [ ] **Image Pushed**: Image available in ACR
- [ ] **Container App Updated**: Azure shows successful update
- [ ] **Revision Healthy**: Health check passes
- [ ] **Application Accessible**: URL responds
- [ ] **Changes Visible**: New UI/functionality working
- [ ] **No Errors**: Logs show no errors
- [ ] **Git Updated**: Changes pushed to repository

### Quick Verification Commands

```powershell
# Check local Docker images
docker images | grep django-app

# Verify image in ACR
az acr repository show-tags --name anjumanmobilereg --repository django-app --output table

# Check Container App status
az containerapp show --name django-app --resource-group hatimmanagedenv --query "properties.runningStatus"

# View recent logs
az containerapp logs show --name django-app --resource-group hatimmanagedenv --tail 50

# Test HTTP response
curl https://django-app.calmrock-3bce75ae.uaenorth.azurecontainerapps.io/
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Docker Build Fails

**Symptoms:**
- Error during `docker build`
- Missing dependencies

**Solutions:**
```powershell
# Clear Docker cache and rebuild
docker build --no-cache -t django-app .

# Check Dockerfile syntax
# Ensure requirements.txt is up to date
```

#### Issue 2: Push to ACR Fails

**Symptoms:**
- Authentication errors
- Permission denied

**Solutions:**
```powershell
# Re-login to Azure
az login --use-device-code

# Login to ACR
az acr login --name anjumanmobilereg

# Verify ACR access
az acr show --name anjumanmobilereg --query "loginServer"
```

#### Issue 3: Container App Not Updating

**Symptoms:**
- Old version still showing
- Changes not visible

**Solutions:**
```powershell
# Force restart the revision
az containerapp revision restart --name django-app --resource-group hatimmanagedenv --revision <revision-name>

# Check if image digest changed
az acr repository show --name anjumanmobilereg --image django-app:latest --query "digest"

# Verify Container App is pulling latest image
az containerapp show --name django-app --resource-group hatimmanagedenv --query "properties.template.containers[0].image"
```

#### Issue 4: Application Unhealthy

**Symptoms:**
- HealthState shows "Unhealthy"
- App not accessible

**Solutions:**
```powershell
# Check logs for errors
az containerapp logs show --name django-app --resource-group hatimmanagedenv --follow

# Verify port configuration
az containerapp show --name django-app --resource-group hatimmanagedenv --query "properties.configuration.ingress.targetPort"

# Check if Django is binding to 0.0.0.0:8000 (not 127.0.0.1)
```

#### Issue 5: Changes Not Visible in Browser

**Symptoms:**
- Old UI still showing
- Browser cache issue

**Solutions:**
- Hard refresh browser: `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
- Clear browser cache
- Test in incognito/private window
- Verify changes actually deployed:
  ```powershell
  az containerapp logs show --name django-app --resource-group hatimmanagedenv --tail 20
  ```

---

## Complete Workflow Summary

### Quick Reference Commands

```powershell
# 1. Make code changes in your editor
# Edit files as needed

# 2. Rebuild Docker image
docker build -t django-app .

# 3. Tag for ACR
docker tag django-app anjumanmobilereg.azurecr.io/django-app:latest

# 4. Push to ACR
docker push anjumanmobilereg.azurecr.io/django-app:latest

# 5. Update Container App
az containerapp update --name django-app --resource-group hatimmanagedenv --image anjumanmobilereg.azurecr.io/django-app:latest

# 6. Restart (optional but recommended)
az containerapp revision restart --name django-app --resource-group hatimmanagedenv --revision django-app--0000001

# 7. Verify
az containerapp revision list --name django-app --resource-group hatimmanagedenv --output table

# 8. Commit to Git
git add .
git commit -m "Your commit message"
git push
```

### Automation Script (Optional)

Create a PowerShell script `deploy.ps1`:

```powershell
# deploy.ps1 - Automated deployment script

Write-Host "Starting deployment process..." -ForegroundColor Green

# Build Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t django-app .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Tag image
Write-Host "Tagging image for ACR..." -ForegroundColor Yellow
docker tag django-app anjumanmobilereg.azurecr.io/django-app:latest

# Push to ACR
Write-Host "Pushing to Azure Container Registry..." -ForegroundColor Yellow
docker push anjumanmobilereg.azurecr.io/django-app:latest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Update Container App
Write-Host "Updating Azure Container App..." -ForegroundColor Yellow
az containerapp update --name django-app --resource-group hatimmanagedenv --image anjumanmobilereg.azurecr.io/django-app:latest

# Restart revision
Write-Host "Restarting revision..." -ForegroundColor Yellow
az containerapp revision restart --name django-app --resource-group hatimmanagedenv --revision django-app--0000001

Write-Host "Deployment complete! ✅" -ForegroundColor Green
Write-Host "Live at: https://django-app.calmrock-3bce75ae.uaenorth.azurecontainerapps.io/" -ForegroundColor Cyan
```

**Usage:**
```powershell
.\deploy.ps1
```

---

## Best Practices

### 1. Version Tagging
Instead of always using `latest`, consider semantic versioning:
```powershell
docker tag django-app anjumanmobilereg.azurecr.io/django-app:v1.0.0
docker tag django-app anjumanmobilereg.azurecr.io/django-app:latest
```

### 2. Testing Locally First
Always test locally before deploying:
```powershell
docker run -p 8000:8000 django-app
# Visit http://localhost:8000
```

### 3. Use Environment Variables
Store sensitive data in Azure Key Vault or Container App secrets:
```powershell
az containerapp secret set --name django-app --resource-group hatimmanagedenv --secrets "db-password=<value>"
```

### 4. Monitor Application
Set up monitoring and alerts:
```powershell
az monitor metrics list --resource <container-app-id> --metric-names Requests
```

### 5. Implement CI/CD
Consider using GitHub Actions or Azure DevOps for automated deployments.

---

## Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Docker Documentation**: https://docs.docker.com/
- **Azure Container Apps**: https://learn.microsoft.com/en-us/azure/container-apps/
- **Azure Container Registry**: https://learn.microsoft.com/en-us/azure/container-registry/

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-09 | Updated landing page with styled UI | Deployment Team |
| 2025-12-09 | Initial deployment to Azure Container Apps | Deployment Team |
| 2025-12-09 | Created Django starter project | Development Team |

---

**Document Version**: 1.0  
**Last Updated**: December 9, 2025  
**Maintained By**: Development Team
