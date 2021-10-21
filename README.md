# 14848HW3

## Major Steps

### I. access AWS resources with a pair of access and secret key

### II. create AWS S3 bucket to host DynamoDB table

### III. upload data-master table (experiment.txt) and 3 other experiment tables (exp1.txt, exp2.txt, exp3.txt) to the S3 bucket

### IV. create a DynamnoDB table to store metadata and ingest data into the experiment table. Please see details in the python script

### V. query contents from the table

## query used on local machine to pull data from DynamoDB
![query](https://github.com/ELizXiong/14848HW3/blob/main/NoSQL/query_used.png)

## query all items in the table created
![all_rows](https://github.com/ELizXiong/14848HW3/blob/main/NoSQL/query_result_all_rows.png)

![all_items](https://github.com/ELizXiong/14848HW3/blob/main/NoSQL/query_results_all_items.png)

## query a specific row from the table (ex. row with RowKey=3)
![row3](https://github.com/ELizXiong/14848HW3/blob/main/NoSQL/query_specific_row.png)
