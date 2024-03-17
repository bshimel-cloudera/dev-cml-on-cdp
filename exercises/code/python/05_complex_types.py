# # Complex Types

# Copyright © 2010–2022 Cloudera. All rights reserved.
# Not to be reproduced or shared without prior written 
# consent from Cloudera.


# ## Overview

# In this module we consider the complex collection data types provided by
# Spark SQL: arrays, maps, and structs.  We show how to construct and
# transform columns with complex collection data types.


# ## Complex Collection Data Types

# * Complex collection data types provide a way to renormalize the denormalized
# data that is common in the big-data world

# * The complex collection data types are defined in the `pyspark.sql.types`
# module:
#   * The *ArrayType* represents a variable-length collection of elements
#   * The *MapType* represents a variable-length collection of key-value pairs
#   * The *StructType* represents a fixed-length collection of named elements

# * Complex collection data types are obtained in several ways:
#   * Inherited from Hive/Impala tables
#   * Inferred from nested JSON files
#   * Generated by aggregate functions such as `collect_list` and `collect_set`
#   * Constructed manually


# ## Setup

# Create a SparkSession:
from pyspark.sql import SparkSession
import cml.data_v1 as cmldata
from env import S3_ROOT, S3_HOME, CONNECTION_NAME

conn = cmldata.get_connection(CONNECTION_NAME)
spark = conn.get_spark_session()

# Read the raw data from HDFS:
rides = spark.read.csv(S3_ROOT + "/duocar/raw/rides/", header=True, inferSchema=True)
drivers = spark.read.csv(S3_ROOT + "/duocar/raw/drivers/", header=True, inferSchema=True)
riders = spark.read.csv(S3_ROOT + "/duocar/raw/riders/", header=True, inferSchema=True)


# ## Arrays

# Use the
# [array](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.array)
# function to create an array from multiple columns:
from pyspark.sql.functions import array
drivers_array = drivers \
  .withColumn("vehicle_array", array("vehicle_make", "vehicle_model")) \
  .select("vehicle_make", "vehicle_model", "vehicle_array")
drivers_array.printSchema()
drivers_array.show(5, False)

# Use index notation to access elements of the array:
from pyspark.sql.functions import col
drivers_array \
  .select("vehicle_array", col("vehicle_array")[0]) \
  .show(5, False)

# Use the
# [size](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.size)
# function to get the length of the array:
from pyspark.sql.functions import size
drivers_array \
  .select("vehicle_array", size("vehicle_array")) \
  .show(5, False)

# Use the
# [sort_array](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.sort_array)
# function to sort the array:
from pyspark.sql.functions import sort_array
drivers_array \
  .select("vehicle_array", sort_array("vehicle_array", asc=True)) \
  .show(5, False)

# Use the `array_contains` function to search the array:
from pyspark.sql.functions import array_contains
drivers_array \
  .select("vehicle_array", array_contains("vehicle_array", "Subaru")) \
  .show(5, False)

# Use the `explode` and `posexplode` functions to explode the array:
from pyspark.sql.functions import explode, posexplode
drivers_array \
  .select("vehicle_array", explode("vehicle_array")) \
  .show(5, False)
drivers_array \
  .select("vehicle_array", posexplode("vehicle_array")) \
  .show(5, False)

# Note that you can pass multiple names to the `alias` method:
drivers_array \
  .select("vehicle_array", posexplode("vehicle_array").alias("position", "column")) \
  .show(5, False)


# ## Maps

# Use the
# [create_map](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.create_map)
# function to create a map:
from pyspark.sql.functions import lit, create_map
drivers_map = drivers \
  .withColumn("vehicle_map", create_map(lit("make"), "vehicle_make", lit("model"), "vehicle_model")) \
  .select("vehicle_make", "vehicle_model", "vehicle_map")
drivers_map.printSchema()
drivers_map.show(5, False)

# Use dot notation to access a value by key:
drivers_map.select("vehicle_map", col("vehicle_map").make).show(5, False)

# Use the `size` function to get the length of the map:
drivers_map.select("vehicle_map", size("vehicle_map")).show(5, False)

# Use the `explode` and `posexplode` functions to explode the map:
drivers_map.select("vehicle_map", explode("vehicle_map")).show(5, False)
drivers_map.select("vehicle_map", posexplode("vehicle_map")).show(5, False)


# ## Structs

# Use the
# [struct](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.struct)
# function to create a struct:
from pyspark.sql.functions import struct
drivers_struct = drivers \
  .withColumn("vehicle_struct", struct(col("vehicle_make").alias("make"), col("vehicle_model").alias("model"))) \
  .select("vehicle_make", "vehicle_model", "vehicle_struct")
drivers_struct.printSchema()
drivers_struct.show(5, False)

# **Note:** The struct is a `Row` object (embedded in a `Row` object).
drivers_struct.head(5)

# Use dot notation to access struct elements:
drivers_struct \
  .select("vehicle_struct", col("vehicle_struct").make) \
  .show(5, False)

# Use the `to_json` function to convert the struct to a JSON string:
from pyspark.sql.functions import to_json
drivers_struct \
  .select("vehicle_struct", to_json("vehicle_struct")) \
  .show(5, False)


# ## Exercises

# (1) Create an array called `home_array` that includes the driver's home
# latitude and longitude.

# (2) Create a map called `name_map` that includes the driver's first and last
# name.

# (3) Create a struct called `name_struct` that includes the driver's first
# and last name.


# ## References

# [Spark Python API -
# pyspark.sql.functions.array](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.array)

# [Spark Python API -
# pyspark.sql.functions.create_map](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.create_map)

# [Spark Python API -
# pyspark.sql.functions.struct](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.functions.struct)


# ## Cleanup

# Stop the SparkSession:
spark.stop()
