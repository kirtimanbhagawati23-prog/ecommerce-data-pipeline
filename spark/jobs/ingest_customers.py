from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim

spark = (
    SparkSession.builder
    .appName("customer_ingestion")
    .getOrCreate()
)

df = (
    spark.read
    .option("header", True)
    .csv("/data/customers.csv")
)

print("Raw Data")
df.show()

clean_df = (
    df
    .dropDuplicates()
    .filter(col("customer_id").isNotNull())
    .filter(col("first_name").isNotNull())
    .withColumn("email", lower(trim(col("email"))))
)

print("Clean Data")
clean_df.show()

clean_df.write.mode("overwrite").parquet(
    "/data/output/customers"
)

spark.stop()