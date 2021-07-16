# ETL-Spark-GCP-week3
This repository is containing PySpark jobs for batch processing of GCS to BigQuery and GCS to GCS by submitting the Pyspark jobs within a cluster on Dataproc tools, GCP. Also there's a bash script to perform end to end Dataproc process from creating cluster, submitting jobs and delete cluster.

# Data Sources
A bunch of flight records data with json format

# Prerequisites
## Windows Part
1. Python 3.7.9
  - pyspark 2.4.8
2. Visual Studio Code
3. Java SE
4. Winutils.exe file from Hadoop-2.6.0
5. Google Cloud Platform
  - Dataproc
  - Google Cloud Storage
  - Google BigQuery
 
 ## Linux Part 
 If you want to run the batch locally, you can run the bash script on linux using cloud SDK since it can't be run on windows yet)
 1. Python 3.6 (or more)
 2. Visual Studio Code
 3. Cloud SDK(https://cloud.google.com/sdk/docs/install)

# Setting Up
There's two ways to do the batch processing, you can use GUI feature on GCP, or run it locally  using Cloud SDK.

## By GUI
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
  ![image](https://user-images.githubusercontent.com/59094767/125968200-0195d404-49d7-4158-bb58-2b92275a9de2.png)
  ![image](https://user-images.githubusercontent.com/59094767/125968297-cb203860-307c-4b98-9a4c-f5bfa5fdf71e.png)
  ![image](https://user-images.githubusercontent.com/59094767/125968392-b2a0e318-efd1-4ed4-a223-0bab04ca59ad.png)

4. After you're done creating new cluster, now you need to submit a new pyspark job within it, thus your converting and uploading job (the one you had code as python file) can be ran here.
  ![image](https://user-images.githubusercontent.com/59094767/125969728-ffe248b6-a07e-4ff1-a728-49f11f1f49f5.png)

## By Shell Script on Linux
1. Install cloud SDK
2. Create your Dataproc Workflow-Template using this command :

    gcloud dataproc workflow-templates create ${TEMPLATE}\
    --region=${REGION}
    
3. Set up your cluster to perform Pyspark job

    gcloud beta dataproc workflow-templates set-managed-cluster ${TEMPLATE} \
    --region=${REGION} \
    --bucket=${BUCKET_NAME} \
    --zone=${ZONE} \
    --cluster-name=${CLUSTER_NAME} \
    --single-node \
    --master-machine-type=n1-standard-2 \
    --image-version=1.5-ubuntu18
    
    There are still many arguments that you can add to set up your cluster, for your reference, please visit this site : 
    https://cloud.google.com/sdk/gcloud/reference/dataproc/workflow-templates/set-managed-cluster
    
 4. Add your job details into your workflow template

    gcloud beta dataproc workflow-templates add-job pyspark gs://${BUCKET_NAME}/input/spark_etl_job.py \
    --step-id="week3-spark-etl" \
    --workflow-templates=${TEMPLATE} \
    --region=${REGION} \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar
    
    The job is not limited to Pyspark only, you can also submit another job such as Spark, Hadoop, etc.
    For more information, you can check it on https://cloud.google.com/sdk/gcloud/reference/dataproc/workflow-templates/add-job
 
 5. Run your workflow template by using this command
 
    gcloud dataproc workflow-templates instantiate ${TEMPLATE} \
    --region=${REGION}


# Output
This whole process will give me Google Storage Files and BigQuery Outputs

## Google Storage Files

## BigQuery
