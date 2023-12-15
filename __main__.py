import json
import boto3
import logging
from botocore.exceptions import ClientError
import os
import pulumi 
import pandas as pd
import openpyxl
from datetime import datetime

file_name = "test.txt"

session = boto3.Session(region_name='us-east-2')

s3client = session.client('s3')

bucket_name = 'my-bucket2-2-2'
s3_location = {
    'LocationConstraint': 'us-east-2'
}

#creating bucket (COMMENTED OUT BECAUSE IT IS ALREADY CREATED)
#s3client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=s3_location)
bucket_list = s3client.list_buckets()
for bucket in bucket_list['Buckets']:
    #print(bucket['Name'] + '/' + file_name)
    key = bucket['Name'] + '/' + file_name

s3 = boto3.resource('s3')
database_name = 'test_database.xlsx'

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

#uploading file to aws s3 bucket my-bucket2-2-2
s3.Bucket(bucket_name).upload_file(file_name, file_name)


#code for implementing into the functions
# data_frame = pd.DataFrame([[file_name,current_time]],index=['data'], columns=['file name', 'current time'])
# print(data_frame)
# data_frame.to_excel('test_database.xlsx', index=False, header=False)

#creating dataframe with input current_time and file_name and output data_frame
def create_dataframe(current_time,key):
    data_frame = pd.DataFrame([[key,current_time]],index=['data'], columns=['file name', 'current time'])
    #print(data_frame)
    return data_frame

#writing data frame with input database_name and data_frame
def write_dateframe(database_name, data_frame):
    print(data_frame)
    data_frame.to_excel(database_name, index=False, header=False)

#calling functions to create database and write to the database
data_frame = create_dataframe(current_time, key)
write_dateframe(database_name, data_frame)

s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')






#IGNORE PSUEDO CODE FOR PERSONAL REFERENCE

# def create_bucket(Bucket='my-bucket', region='us-east-2'):
#     """Create an S3 bucket in a specified region

#     If a region is not specified, the bucket is created in the S3 default
#     region (us-east-1).

#     :param my_bucket: Bucket to create
#     :param region: String region to create bucket in, e.g., 'us-west-2'
#     :return: True if bucket created, else False
#     """

#     # Create bucket
#     try:
#         if region is None:
#             s3_client = boto3.client('s3')
#             s3_client.create_bucket(Bucket)
#         else:
#             s3_client = boto3.client('s3', region_name=region)
#             location = {'LocationConstraint': region}
#             s3_client.create_bucket(Bucket,
#                                     CreateBucketConfiguration=location)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

# def upload_file(test, bucket, object_name=None):

#     if object_name is None:
#         object_name = os.path.basename(test)

#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(test, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True