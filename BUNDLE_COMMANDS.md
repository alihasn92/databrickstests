# Databricks Bundle Commands - Quick Reference Guide

## 🚀 Essential Bundle Commands

### 1. Initialize a New Bundle
```bash
# Create a new bundle from template
databricks bundle init

# Create with specific template
databricks bundle init --template default-python
```

### 2. Validate Bundle Configuration
```bash
# Validate the bundle configuration
databricks bundle validate

# Validate specific target
databricks bundle validate -t dev
databricks bundle validate -t prod
```

### 3. Deploy Bundle
```bash
# Deploy to default target (dev)
databricks bundle deploy

# Deploy to specific target
databricks bundle deploy -t dev
databricks bundle deploy -t staging
databricks bundle deploy -t prod

# Force redeployment (useful for troubleshooting)
databricks bundle deploy -t dev --force

# Deploy with compute override
databricks bundle deploy -t dev --compute-id <cluster-id>
```

### 4. Run Bundle Resources
```bash
# Run a job from the bundle
databricks bundle run sales_processing_job

# Run with specific target
databricks bundle run sales_processing_job -t prod

# Run and wait for completion
databricks bundle run sales_processing_job --no-wait=false
```

### 5. Destroy Bundle
```bash
# Remove all deployed resources
databricks bundle destroy

# Destroy specific target
databricks bundle destroy -t dev
databricks bundle destroy -t staging

# Force destroy without confirmation
databricks bundle destroy -t dev --auto-approve
```

### 6. Generate Configuration from Workspace
```bash
# Generate bundle config from existing job
databricks bundle generate job <job-id>

# Generate from pipeline
databricks bundle generate pipeline <pipeline-id>

# Generate from model serving endpoint
databricks bundle generate model-serving-endpoint <endpoint-name>
```

### 7. Bind Bundle to Workspace Resources
```bash
# Bind bundle to existing workspace resource
databricks bundle deployment bind <resource-type> <resource-key> <resource-id>

# Example: Bind to existing job
databricks bundle deployment bind job sales_processing_job 123456
```

### 8. Get Bundle Summary
```bash
# Show bundle summary
databricks bundle summary

# Show summary for specific target
databricks bundle summary -t prod
```

## 🔍 Useful Debugging Commands

### Check Bundle Configuration
```bash
# Validate and show detailed errors
databricks bundle validate -t dev --debug

# Show computed configuration
databricks bundle schema
```

### View Deployed Resources
```bash
# List all deployed jobs
databricks jobs list

# Get specific job details
databricks jobs get --job-id <job-id>

# View job runs
databricks jobs runs list --job-id <job-id>
```

## 📋 Common Workflows

### Development Workflow
```bash
# 1. Make code changes
vim main.py

# 2. Run tests locally
pytest test_main.py

# 3. Validate bundle
databricks bundle validate -t dev

# 4. Deploy to dev
databricks bundle deploy -t dev

# 5. Run and test
databricks bundle run sales_processing_job -t dev
```

### Production Deployment Workflow
```bash
# 1. Validate production config
databricks bundle validate -t prod

# 2. Deploy to staging first
databricks bundle deploy -t staging

# 3. Test in staging
databricks bundle run sales_processing_job -t staging

# 4. Deploy to production
databricks bundle deploy -t prod

# 5. Monitor production job
databricks jobs runs list --job-id <prod-job-id>
```

### CI/CD Pipeline Commands
```bash
# In GitHub Actions / Azure DevOps pipeline:

# Validate
databricks bundle validate -t ${TARGET}

# Deploy
databricks bundle deploy -t ${TARGET} --auto-approve

# Run tests
databricks bundle run test_job -t ${TARGET}
```

## 🎯 Target-Specific Operations

### Switch Between Targets
```bash
# Deploy to different environments
databricks bundle deploy -t dev      # Your personal dev environment
databricks bundle deploy -t staging  # Shared staging environment
databricks bundle deploy -t prod     # Production environment
```

### Override Variables
```bash
# Override bundle variables at deploy time
databricks bundle deploy -t dev \
  --var="catalog=custom_catalog" \
  --var="schema=custom_schema"
```

## 🔧 Advanced Commands

### Using Custom Profiles
```bash
# Deploy using specific Databricks CLI profile
databricks bundle deploy -t prod --profile production-profile
```

### Parallel Deployments
```bash
# Deploy multiple bundles in parallel
databricks bundle deploy -t dev &
databricks bundle deploy -t staging &
wait
```

### Sync Local Changes
```bash
# Watch for file changes and auto-deploy (development mode)
# Note: This requires external tools like watchexec
watchexec -w . "databricks bundle deploy -t dev"
```

## 🐛 Troubleshooting Commands

### View Deployment Logs
```bash
# Enable verbose logging
databricks bundle deploy -t dev --debug

# View recent job runs
databricks jobs runs list --job-id <job-id> --limit 5
```

### Fix Common Issues
```bash
# Issue: Deployment lock conflict
# Solution: Disable lock in dev mode or wait for lock to release
databricks bundle deploy -t dev --force

# Issue: Permission denied
# Solution: Check workspace permissions and service principal config

# Issue: Resource already exists
# Solution: Use force deploy or destroy first
databricks bundle destroy -t dev --auto-approve
databricks bundle deploy -t dev
```

## 📚 Configuration File Locations

```
~/.databrickscfg          # Databricks CLI configuration
./databricks.yml          # Main bundle configuration
./resources/*.yml         # Resource definitions
./.databricks/            # Bundle state files (gitignored)
```

## 🔐 Authentication

```bash
# Configure authentication token
databricks configure --token

# Use service principal (recommended for CI/CD)
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-token"
export DATABRICKS_CLIENT_ID="your-client-id"
export DATABRICKS_CLIENT_SECRET="your-client-secret"
```

## 💡 Pro Tips

1. **Always validate before deploying**: `databricks bundle validate`
2. **Use dev mode for iteration**: Deployment lock is disabled in dev mode
3. **Test in staging first**: Never deploy directly to production
4. **Use service principals**: For production deployments
5. **Version your bundles**: Tag releases in Git
6. **Monitor deployments**: Check job runs after deployment

## 🆘 Getting Help

```bash
# General help
databricks bundle --help

# Command-specific help
databricks bundle deploy --help
databricks bundle run --help

# View bundle schema documentation
databricks bundle schema
```

---

**Quick Start**: `databricks bundle init → validate → deploy → run`
**Remember**: Dev for testing, Staging for validation, Prod for production!