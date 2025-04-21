# Dockerfile
FROM apache/airflow:2.6.2

USER root

# Install Spark
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && apt-get clean

# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

USER airflow