#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 05:12:26 2021

@author: Yiru Xiong
"""
import boto3
import csv
# update local path before proceeding 
data_path = "./local-data-path/"
# hide access credentials for security purpose
s3 = boto3.resource('s3', aws_access_key_id='', aws_secret_access_key='')
s3.create_bucket(Bucket = 'expdatahw3', CreateBucketConfiguration={'LocationConstraint':'us-east-2'})
bucket = s3.Bucket('expdatahw3')
# upload files to S3
s3.Object('expdatahw3', "exp1.csv").put(Body=open(data_path + "exp1.csv", 'rb'))
s3.Object('expdatahw3', "exp2.csv").put(Body=open(data_path + "exp2.csv", 'rb'))
s3.Object('expdatahw3', "exp3.csv").put(Body=open(data_path + "exp3.csv", 'rb'))
s3.Object('expdatahw3', "experiments.csv").put(Body=open(data_path + "experiments.csv", 'rb'))

# create a DynamoDB table
# partition key is similar to primary key
dyndb = boto3.resource('dynamodb', region_name='us-east-2')
table = dyndb.create_table(
        TableName= 'Experiment_Table',
        KeySchema= [
            {'AttributeName': 'PartitionKey', 'KeyType': 'HASH'},
            {'AttributeName': 'RowKey', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions= [
            {'AttributeName': 'PartitionKey', 'AttributeType': 'S'},
            {'AttributeName': 'RowKey', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput= {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
 )

table.meta.client.get_waiter('table_exists').wait(TableName='Experiment_Table')
table = dyndb.Table('Experiment_Table')


#for obj in bucket.objects.filter(Prefix="s3://expdatahw3/").all():
#[obj.Acl().put(ACL='public-read') for obj in bucket.objects.filter(Prefix="s3://expdatahw3/").all()]

# read the metadata from a CSV file and mvoe the data object into the blob store
urlbase = "https://expdatahw3.s3.us-east-2.amazonaws.com/"

with open(data_path+'experiments.csv','r') as csvfile: 
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvf,None)
    for item in csvf:
        print(item)
        body = open(data_path + item[4], 'rb')
        s3.Object('expdatahw3', item[4]).put(Body=body)
        s3.Object('expdatahw3', item[4]).Acl().put(ACL='public-read')
        url = urlbase+item[4]
        metadata_item = {'PartitionKey': item[0], 'RowKey': item[0], 'Temp':item[1],
                         'Conductivity': item[2], 'Concentration':item[3], 'url':url}
        try:
            table.put_item(Item=metadata_item)
        except:
            print("Item may already be there or another failure")

# query from created table on local 
# retrieve all rows
response = table.scan()
items = response['Items']
for idx, content in enumerate(items):
    print(f"Num: {idx} ==> {content}")

# print all items:
print(items)

# retrieve specific row from the table
# request the third row key RowKey = 3
requested_row = table.get_item(
        Key={
                'PartitionKey':'3',
                'RowKey':'3'
            })
print(requested_row)
        
        