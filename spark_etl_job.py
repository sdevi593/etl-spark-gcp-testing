from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

#define constant
BUCKET_NAME = "input_etl_spark"
PROJECT_ID = "sunlit-amulet-318910"
DATASET_ID = "flight_data"
DAYS_DIFFERENT = 753

#create SparkSession
spark_session = SparkSession.builder \
    .appName("JSONtoBigQuery")\
    .getOrCreate() #bring back the available SparkSession, if isn't available, create a new one

schema = StructType([
    StructField("id", IntegerType()),
    StructField("flight_num", IntegerType()),
    StructField("airline_code", StringType()),
    StructField("flight_date", DateType()),
    StructField("source_airport", StringType()),
    StructField("destination_airport", StringType()),
    StructField("distance", LongType()),
    StructField("departure_time", LongType()),
    StructField("arrival_time", LongType()),
    StructField("departure_delay", LongType()),
    StructField("arrival_delay", LongType()),
    StructField("airtime", LongType()),
])

#Extract From GCS to Spark Dataframe
start = time.time()
df_schema = spark_session.read.format("json") \
    .load(f"gs://{BUCKET_NAME}/input/2021/*.json", schema=schema)
print(f"Read data execution time with schema: {time.time() - start} seconds")
df_schema.printSchema()

#Transform Flight Date
df_add_daysdiff = df_schema.withColumn("flight_date", date_add(df_schema.flight_date, DAYS_DIFFERENT))
df_add_daysdiff.show()

#Partition Spark Dataframe for BigQuery
#summarize flight data by airline code per day
start = time.time()
total_flight_airline = df_add_daysdiff.groupBy("flight_date", "airline_code") \
    .count() \
    .orderBy("flight_date", "airline_code")

total_flight_airline.show()

#summarize flight data by source_airport and destination_airport per day
total_flight_airport = df_add_daysdiff.groupBy("flight_date", "source_airport", "destination_airport") \
    .count() \
    .orderBy("flight_date")

total_flight_airport.show()

#Load Spark Dataframe to BigQuery
start = time.time()
df_add_daysdiff.write.mode('overwrite').format('bigquery') \
    .option('temporaryGcsBucket', BUCKET_NAME) \
    .option('createDisposition', 'CREATE_IF_NEEDED') \
    .option('partitionField', 'flight_date') \
    .option('partitionType', 'DAY') \
    .save(f"{PROJECT_ID}:{DATASET_ID}.flights")
print(f"Execution time write flights data to BigQuery: {time.time() - start} seconds")

start = time.time()
df_add_daysdiff.write.mode('overwrite').format('bigquery') \
    .option('temporaryGcsBucket', BUCKET_NAME) \
    .option('createDisposition', 'CREATE_IF_NEEDED') \
    .save(f"{PROJECT_ID}:{DATASET_ID}.count_total_flight_airlines_per_day")
print(f"Execution time write count_total_flight_airlines_per_day data to BigQuery: {time.time() - start} seconds")

start = time.time()
df_add_daysdiff.write.mode('overwrite').format('bigquery') \
    .option('temporaryGcsBucket', BUCKET_NAME) \
    .option('createDisposition', 'CREATE_IF_NEEDED') \
    .save(f"{PROJECT_ID}:{DATASET_ID}.count_flight_travels_per_day")
print(f"Execution time write count_flight_travels_per_day data to BigQuery: {time.time() - start} seconds")

#Convert Spark Dataframe to others format
start = time.time()
df_add_daysdiff.repartition(1).write.mode('overwrite') \
    .partitionBy("flight_date") \
    .format('csv') \
    .save(f'gs://{BUCKET_NAME}/output/flights.csv')
print(f"Excetion time of writing partitioned csv data to BigQuery: {time.time() - start} seconds")

start = time.time()
df_add_daysdiff.repartition(1).write.mode('overwrite') \
    .partitionBy("flight_date") \
    .format('parquet') \
    .save(f'gs://{BUCKET_NAME}/output/flights.parquet')
print(f"Excetion time of writing partitioned parquet data to BigQuery: {time.time() - start} seconds")

start = time.time()
df_add_daysdiff.repartition(1).write.mode('overwrite') \
    .partitionBy("flight_date") \
    .format('json') \
    .save(f'gs://{BUCKET_NAME}/output/flights.json')
print(f"Excetion time of writing partitioned json data to BigQuery: {time.time() - start} seconds")

spark_session.stop