"""
Unit Tests for Sales Data Processing Module
============================================
This module contains unit tests for the SalesDataProcessor class.

Author: Hassan Ali
Date: October 2025
Purpose: PoC 1 - Demonstrate testing best practices
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType, DoubleType, IntegerType
from datetime import datetime, timedelta
from main import SalesDataProcessor, create_sample_data


@pytest.fixture(scope="session")
def spark():
    """
    Create a SparkSession for testing.
    This fixture is created once per test session.
    """
    spark = SparkSession.builder \
        .appName("TestSalesDataProcessor") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()


@pytest.fixture
def sample_sales_data(spark):
    """
    Create sample sales data for testing.
    """
    schema = StructType([
        StructField("order_id", StringType(), True),
        StructField("order_date", DateType(), True),
        StructField("customer_id", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("revenue", DoubleType(), True),
        StructField("quantity", IntegerType(), True)
    ])
    
    data = [
        ("ORD_001", datetime(2024, 1, 15), "CUST_001", "PROD_001", 1000.0, 2),
        ("ORD_002", datetime(2024, 1, 20), "CUST_002", "PROD_002", 1500.0, 3),
        ("ORD_003", datetime(2024, 2, 10), "CUST_001", "PROD_001", 2000.0, 4),
        ("ORD_004", datetime(2024, 2, 15), "CUST_003", "PROD_003", 500.0, 1),
        ("ORD_005", datetime(2024, 3, 5), "CUST_002", "PROD_002", 3000.0, 5),
    ]
    
    return spark.createDataFrame(data, schema)


@pytest.fixture
def processor(spark):
    """
    Create a SalesDataProcessor instance for testing.
    """
    return SalesDataProcessor(spark)


class TestSalesDataProcessor:
    """
    Test suite for SalesDataProcessor class.
    """
    
    def test_initialization(self, spark):
        """Test that processor initializes correctly."""
        processor = SalesDataProcessor(spark)
        assert processor.spark is not None
        assert isinstance(processor, SalesDataProcessor)
    
    def test_calculate_monthly_kpis(self, processor, sample_sales_data):
        """Test monthly KPI calculations."""
        result = processor.calculate_monthly_kpis(sample_sales_data)
        
        # Check that result has expected columns
        expected_columns = [
            "month", "total_revenue", "order_count", 
            "unique_customers", "avg_order_value",
            "max_order_value", "min_order_value"
        ]
        for col in expected_columns:
            assert col in result.columns, f"Missing column: {col}"
        
        # Check row count (should have 3 months)
        assert result.count() == 3
        
        # Check January totals
        jan_data = result.filter("month = '2024-01-01'").collect()[0]
        assert jan_data["total_revenue"] == 2500.0
        assert jan_data["order_count"] == 2
        assert jan_data["unique_customers"] == 2
    
    def test_add_revenue_trends(self, processor, spark):
        """Test revenue trend calculations."""
        # Create simple monthly data
        schema = StructType([
            StructField("month", DateType(), True),
            StructField("total_revenue", DoubleType(), True)
        ])
        
        data = [
            (datetime(2024, 1, 1), 1000.0),
            (datetime(2024, 2, 1), 1200.0),
            (datetime(2024, 3, 1), 1500.0),
        ]
        
        monthly_df = spark.createDataFrame(data, schema)
        result = processor.add_revenue_trends(monthly_df)
        
        # Check that trend columns exist
        assert "mom_growth_pct" in result.columns
        assert "yoy_growth_pct" in result.columns
        
        # Check February MoM growth: (1200-1000)/1000 * 100 = 20%
        feb_data = result.filter("month = '2024-02-01'").collect()[0]
        assert abs(feb_data["mom_growth_pct"] - 20.0) < 0.01
    
    def test_identify_top_performers(self, processor, sample_sales_data):
        """Test top performer identification."""
        result = processor.identify_top_performers(
            sample_sales_data,
            group_by_col="customer_id",
            top_n=2
        )
        
        # Should return top 2 customers
        assert result.count() == 2
        
        # Check columns
        assert "customer_id" in result.columns
        assert "total_revenue" in result.columns
        assert "order_count" in result.columns
        
        # Top customer should be CUST_002 with 4500.0 total revenue
        top_customer = result.collect()[0]
        assert top_customer["customer_id"] == "CUST_002"
        assert top_customer["total_revenue"] == 4500.0
    
    def test_create_sample_data(self, spark):
        """Test sample data creation function."""
        df = create_sample_data(spark)
        
        # Check that data was created
        assert df.count() == 1000
        
        # Check schema
        expected_columns = [
            "order_id", "order_date", "customer_id", 
            "product_id", "revenue", "quantity"
        ]
        for col in expected_columns:
            assert col in df.columns
    
    def test_empty_dataframe_handling(self, processor, spark):
        """Test handling of empty DataFrames."""
        schema = StructType([
            StructField("order_id", StringType(), True),
            StructField("order_date", DateType(), True),
            StructField("customer_id", StringType(), True),
            StructField("revenue", DoubleType(), True)
        ])
        
        empty_df = spark.createDataFrame([], schema)
        result = processor.calculate_monthly_kpis(empty_df)
        
        # Should return empty DataFrame but with correct schema
        assert result.count() == 0
        assert "month" in result.columns
    
    def test_revenue_calculation_accuracy(self, processor, sample_sales_data):
        """Test that revenue calculations are accurate."""
        result = processor.calculate_monthly_kpis(sample_sales_data)
        
        # Calculate expected total revenue manually
        expected_total = 1000.0 + 1500.0 + 2000.0 + 500.0 + 3000.0
        actual_total = sum(row["total_revenue"] for row in result.collect())
        
        assert abs(actual_total - expected_total) < 0.01


class TestIntegration:
    """
    Integration tests for the full workflow.
    """
    
    def test_full_workflow(self, spark):
        """Test the complete data processing workflow."""
        # Create processor
        processor = SalesDataProcessor(spark)
        
        # Create sample data
        sales_df = create_sample_data(spark)
        
        # Calculate KPIs
        monthly_kpis = processor.calculate_monthly_kpis(sales_df)
        assert monthly_kpis.count() > 0
        
        # Add trends
        kpis_with_trends = processor.add_revenue_trends(monthly_kpis)
        assert "mom_growth_pct" in kpis_with_trends.columns
        
        # Identify top performers
        top_customers = processor.identify_top_performers(sales_df)
        assert top_customers.count() <= 10


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])