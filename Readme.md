# Knauf Sales Analytics - Data Platform 2.0 PoC

## 📋 Project Overview

This project demonstrates best practices for software development in Databricks as part of the Data Platform 2.0 migration from Azure ML to Databricks.

**Purpose**: PoC 1 - Establish good software development practices for Data Scientists

**Key Features**:
- ✅ Python `.py` files instead of notebooks for better version control
- ✅ Unit tests with pytest
- ✅ CI/CD with Databricks Asset Bundles
- ✅ Separation of dev/staging/prod environments
- ✅ Modular, testable code structure

## 🏗️ Project Structure

```
knauf-sales-analytics/
├── databricks.yml                 # Main bundle configuration
├── resources/
│   └── sales_processing_job.yml  # Job definitions
├── src/
│   ├── main.py                   # Main processing logic
│   └── test_main.py              # Unit tests
├── notebooks/                     # Optional notebooks for exploration
├── tests/                        # Integration tests
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD pipeline (GitHub Actions)
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

1. Databricks workspace access
2. Databricks CLI installed
3. Git repository configured

### Installation

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure Databricks authentication
databricks configure --token

# Clone this repository
git clone https://github.com/your-org/knauf-sales-analytics.git
cd knauf-sales-analytics
```

## 💻 Development Workflow

### 1. Local Development

```bash
# Create a feature branch
git checkout -b feature/new-kpi

# Make changes to main.py
# Run tests locally
pytest test_main.py -v

# Commit and push
git add .
git commit -m "Add new KPI calculation"
git push origin feature/new-kpi
```

### 2. Deploy to Dev Environment

```bash
# Validate bundle configuration
databricks bundle validate

# Deploy to dev workspace
databricks bundle deploy -t dev

# Run the job
databricks bundle run -t dev sales_processing_job
```

### 3. Code Review & Merge

1. Create Pull Request in GitHub/Azure DevOps
2. Team reviews the `.py` file changes (clean diffs!)
3. Automated tests run via CI/CD
4. Merge to main branch

### 4. Deploy to Production

```bash
# Deploy to staging first
databricks bundle deploy -t staging

# After validation, deploy to production
databricks bundle deploy -t prod
```

## 🧪 Running Tests

```bash
# Run all tests
pytest test_main.py -v

# Run specific test class
pytest test_main.py::TestSalesDataProcessor -v

# Run with coverage report
pytest test_main.py --cov=main --cov-report=html
```

## 📊 Key Components

### SalesDataProcessor Class

Main class that handles all sales data operations:

- `load_sales_data()` - Load data from Unity Catalog
- `calculate_monthly_kpis()` - Generate monthly metrics
- `add_revenue_trends()` - Calculate MoM and YoY growth
- `identify_top_performers()` - Find top customers/products
- `save_to_delta()` - Save results to Delta tables

### Example Usage

```python
from main import SalesDataProcessor

# Initialize processor
processor = SalesDataProcessor()

# Load sales data
df = processor.load_sales_data("main.sales_data.orders")

# Calculate KPIs
kpis = processor.calculate_monthly_kpis(df)

# Add trends
kpis_with_trends = processor.add_revenue_trends(kpis)

# Save results
processor.save_to_delta(
    kpis_with_trends, 
    "main.sales_analytics.monthly_kpis"
)
```

## 🎯 Bundle Deployment Targets

### Development (`dev`)
- Personal workspace folder
- Uses your personal catalog/schema
- Jobs are paused by default
- Fast iteration with deployment lock disabled

### Staging (`staging`)
- Shared workspace location
- Uses staging catalog
- Service principal execution
- Team testing environment

### Production (`prod`)
- Shared workspace location
- Uses production catalog
- Service principal execution
- Strict validation and deployment controls

## 🔧 Configuration

### databricks.yml

Main configuration file that defines:
- Bundle metadata
- Target environments
- Variables and permissions
- Artifact build settings

### resources/sales_processing_job.yml

Job definition that includes:
- Task definitions
- Cluster configuration
- Schedule and notifications
- Dependencies and retry logic

## 📦 Building Artifacts

To build Python wheel for deployment:

```bash
# Build wheel
pip wheel -w dist .

# Deploy bundle (will automatically build artifacts)
databricks bundle deploy -t prod
```

## 🔐 Security Best Practices

1. **Service Principals**: Use service principals for staging/prod deployments
2. **Secrets Management**: Store credentials in Databricks Secrets
3. **Access Control**: Define proper permissions in bundle configuration
4. **Git Integration**: Use Git source for job runs

## 🐛 Troubleshooting

### Bundle validation fails
```bash
# Check bundle configuration syntax
databricks bundle validate -t dev
```

### Job fails to run
```bash
# Check job run logs in Databricks UI
# Or use CLI:
databricks jobs runs list --job-id <job-id>
```

### Deployment issues
```bash
# Force redeployment
databricks bundle deploy -t dev --force
```

## 📚 Additional Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/)
- [CI/CD Best Practices](https://docs.databricks.com/dev-tools/ci-cd/best-practices.html)
- [Unity Catalog Guide](https://docs.databricks.com/data-governance/unity-catalog/)

## 👥 Team

**Project Lead**: Hassan Ali (hassan.ali@knauf.com)
**Data Platform Team**: Knauf IT - Data & Cross Enablement

## 📝 License

Internal Knauf Project - All Rights Reserved

---

**Status**: PoC Phase
**Last Updated**: October 2025