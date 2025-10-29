"""
Knauf Sales Data Processing Module
===================================
This module demonstrates best practices for data processing in Databricks.
It includes data loading, transformation, and basic analysis functions.

Author: Hassan Ali
Date: October 2025
Purpose: PoC 1 - Software Development Practices for Data Platform 2.0
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SalesDataProcessor:
    """
    A class to handle sales data processing operations.
    
    This demonstrates object-oriented programming practices and 
    clean code structure for Databricks development.
    """
    
    def __init__(self, spark: Optional[SparkSession] = None):
        """
        Initialize the SalesDataProcessor.
        
        Args:
            spark: SparkSession instance. If None, creates a new session.
        """
        self.spark = spark or SparkSession.builder.getOrCreate()
        logger.info("SalesDataProcessor initialized")
    
    def load_sales_data(self, table_name: str) -> DataFrame:
        """
        Load sales data from Unity Catalog.
        
        Args:
            table_name: Full table name in format 'catalog.schema.table'
        
        Returns:
            DataFrame with sales data
        """
        logger.info(f"Loading data from {table_name}")
        try:
            df = self.spark.table(table_name)
            logger.info(f"Successfully loaded {df.count()} records")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def calculate_monthly_kpis(self, df: DataFrame) -> DataFrame:
        """
        Calculate monthly KPIs from sales data.
        
        Args:
            df: Input DataFrame with columns: order_date, revenue, customer_id
        
        Returns:
            DataFrame with monthly KPIs
        """
        logger.info("Calculating monthly KPIs")
        
        monthly_kpis = df.withColumn(
            "month", 
            F.date_trunc("month", F.col("order_date"))
        ).groupBy("month").agg(
            F.sum("revenue").alias("total_revenue"),
            F.count("*").alias("order_count"),
            F.countDistinct("customer_id").alias("unique_customers"),
            F.avg("revenue").alias("avg_order_value"),
            F.max("revenue").alias("max_order_value"),
            F.min("revenue").alias("min_order_value")
        ).orderBy("month")
        
        logger.info("Monthly KPIs calculated successfully")
        return monthly_kpis
    
    def add_revenue_trends(self, df: DataFrame) -> DataFrame:
        """
        Add revenue trend calculations (MoM growth, YoY growth).
        
        Args:
            df: DataFrame with monthly metrics
        
        Returns:
            DataFrame with trend columns added
        """
        logger.info("Adding revenue trend calculations")
        
        window_spec = Window.orderBy("month")
        
        df_with_trends = df.withColumn(
            "prev_month_revenue",
            F.lag("total_revenue", 1).over(window_spec)
        ).withColumn(
            "mom_growth_pct",
            ((F.col("total_revenue") - F.col("prev_month_revenue")) / 
             F.col("prev_month_revenue") * 100)
        ).withColumn(
            "prev_year_revenue",
            F.lag("total_revenue", 12).over(window_spec)
        ).withColumn(
            "yoy_growth_pct",
            ((F.col("total_revenue") - F.col("prev_year_revenue")) / 
             F.col("prev_year_revenue") * 100)
        )
        
        logger.info("Revenue trends added successfully")
        return df_with_trends
    
    def identify_top_performers(
        self, 
        df: DataFrame, 
        group_by_col: str = "customer_id",
        top_n: int = 10
    ) -> DataFrame:
        """
        Identify top performing customers/products.
        
        Args:
            df: Input DataFrame
            group_by_col: Column to group by (e.g., 'customer_id', 'product_id')
            top_n: Number of top performers to return
        
        Returns:
            DataFrame with top performers
        """
        logger.info(f"Identifying top {top_n} performers by {group_by_col}")
        
        top_performers = df.groupBy(group_by_col).agg(
            F.sum("revenue").alias("total_revenue"),
            F.count("*").alias("order_count"),
            F.avg("revenue").alias("avg_order_value")
        ).orderBy(
            F.col("total_revenue").desc()
        ).limit(top_n)
        
        return top_performers
    
    def save_to_delta(
        self, 
        df: DataFrame, 
        table_name: str, 
        mode: str = "overwrite"
    ) -> None:
        """
        Save DataFrame to Delta table in Unity Catalog.
        
        Args:
            df: DataFrame to save
            table_name: Target table name in format 'catalog.schema.table'
            mode: Write mode ('overwrite', 'append', 'merge')
        """
        logger.info(f"Saving data to {table_name} with mode={mode}")
        try:
            df.write.format("delta").mode(mode).saveAsTable(table_name)
            logger.info(f"Successfully saved {df.count()} records to {table_name}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise


def create_sample_data(spark: SparkSession) -> DataFrame:
    """
    Create sample sales data for testing purposes.
    
    Args:
        spark: SparkSession instance
    
    Returns:
        DataFrame with sample sales data
    """
    from datetime import datetime, timedelta
    import random
    
    logger.info("Creating sample sales data")
    
    # Generate sample data
    start_date = datetime(2024, 1, 1)
    data = []
    
    for i in range(1000):
        order_date = start_date + timedelta(days=random.randint(0, 300))
        data.append({
            "order_id": f"ORD_{i:05d}",
            "order_date": order_date,
            "customer_id": f"CUST_{random.randint(1, 100):04d}",
            "product_id": f"PROD_{random.randint(1, 50):03d}",
            "revenue": round(random.uniform(50, 5000), 2),
            "quantity": random.randint(1, 10)
        })
    
    df = spark.createDataFrame(data)
    logger.info(f"Created sample data with {len(data)} records")
    return df


def main():
    """
    Main execution function demonstrating the complete workflow.
    """
    logger.info("Starting Sales Data Processing workflow")
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Knauf_Sales_Processing") \
        .getOrCreate()
    
    # Initialize processor
    processor = SalesDataProcessor(spark)
    
    # For demo purposes, create sample data
    # In production, you would load from Unity Catalog
    logger.info("Creating sample data for demonstration")
    sales_df = create_sample_data(spark)
    
    # Display sample records
    logger.info("Sample sales data:")
    sales_df.show(10)
    
    # Calculate monthly KPIs
    monthly_kpis = processor.calculate_monthly_kpis(sales_df)
    logger.info("Monthly KPIs:")
    monthly_kpis.show()
    
    # Add revenue trends
    kpis_with_trends = processor.add_revenue_trends(monthly_kpis)
    logger.info("KPIs with trend analysis:")
    kpis_with_trends.show()
    
    # Identify top customers
    top_customers = processor.identify_top_performers(
        sales_df, 
        group_by_col="customer_id",
        top_n=10
    )
    logger.info("Top 10 customers:")
    top_customers.show()
    
    # testing the fuck out of databricks
    # Optional: Save results to Delta table (uncomment when ready)
    # processor.save_to_delta(
    #     kpis_with_trends, 
    #     "main.sales_analytics.monthly_kpis"
    # )
    
    logger.info("Sales Data Processing workflow completed successfully")
    
    return kpis_with_trends


if __name__ == "__main__":
    """
    Entry point when script is executed directly.
    """
    try:
        result = main()
        print("\n" + "="*60)
        print("SUCCESS: Sales data processing completed!")
        print("="*60)
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        raise