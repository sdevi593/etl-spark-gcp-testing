# ETL-Spark-GCP-week3
This repository is about ETL some flight records data with json format and convert it to parquet, csv, BigQuery by running the job in GCP using Dataproc and Pyspark. (Windows 10)

# Data Sources
A bunch of flight records data with json format

# Prerequisites
1. Python 3.7.9
  - pyspark 2.4.8
2. Visual Studio Code
3. Java SE
4. Winutils.exe file from Hadoop-2.6.0
5. Google Cloud Platform
  - Dataproc
  - Google Cloud Storage
  - Google BigQuery

# Setting Up

## Java SE
1. Download Java SE (https://www.oracle.com/java/technologies/javase-downloads.html) and install it
2. Set JAVA_HOME by adding its PATH to Environment Variables with Variable name is JAVA_HOME and Variable values is the path of your java folder was located (ex : C:\Program Files\Java\jdk-16.0.1)

## Winutils.exe file
1. Download Winutils.exe file from Hadoop-2.6.0 version
2. Create a folder within your C drive called winutils and save the winutils.exe file there
3. Create a system variable named HADOOP_HOME with Variable value is C:\winutils

## Create Python Script
1. Code a script on Visual Studio Code for ETL the json data and upload it to BigQuery and convert it to parquet and csv

## GCP Dataproc 
1. Enable Dataproc API to create cluster and submit your pyspark job here later

## Create Dataproc CLuster
1. From GCP Navigator, go to dataproc, click new cluster by clicking "Create Cluster" option
2. Complete your Cluster Configuration and click "Create" Button, wait for the cluster to be provisioned and make sure your cluster status is Running in the end
3. After you're done creating new cluster, now you need to submit a new pyspark job within it, thus your converting and uploading job (the one you had code as python file) can be ran here.


# Output
