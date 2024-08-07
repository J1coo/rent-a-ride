
from boto3.dynamodb.conditions import Attr, Key
import boto3

# =% DATABASE
db = boto3.resource(service_name = 'dynamodb',region_name = 'us-east-1',
        aws_access_key_id = 'AKIAX3OUKCBBZKLTD3SH',
        aws_secret_access_key = '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')


# =% S3 BUCKET
s3 = boto3.client(service_name = 's3',region_name = 'us-east-1',
        aws_access_key_id = 'AKIAX3OUKCBBZKLTD3SH',
        aws_secret_access_key = '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')


def checkFileExist(bucketName,folderNamePath):
    try:
        url=s3.head_object(Bucket=bucketName, Key=folderNamePath)
        return True
    except:
        return False
    
def get_all_item(tableName):
    response = db.Table(f'{tableName}').scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = db.Table(f'{tableName}').scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    return items


def get_item(tableName,docId):
    itemData = db.Table(tableName).get_item(Key={'docId':docId})['Item']
    return itemData



def put_item(tableName,listOfAttributes):
    db.Table(tableName).put_item(Item=listOfAttributes)
    return True



def put_image(folderName,allFiles,docId):
    storedLocation={}
    for each,val in allFiles.items():
        stored_loaction =f'{folderName}/{docId}/{val.name}'
        check=checkFileExist('gcbimages',f'{folderName}/{docId}/{val.name}')
        if not check:   
            s3.put_object(Bucket='gcbimages', Key=f'{folderName}/{docId}/{val.name}',Body=val)

        image_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': 'gcbimages',
                'Key': f'{stored_loaction}'
            },
            ExpiresIn=3600 
            )    
        url=image_url.split('?')[0]
        storedLocation[each]=url
    return storedLocation


def getDataOfSameType(table,indexName,fieldName,text):
    productQuery = db.Table(table).query(
        IndexName=f'{indexName}',
        KeyConditionExpression=Key(f'{fieldName}').eq(text)
    )
    items = productQuery['Items']
    while 'LastEvaluatedKey' in productQuery:
        productQuery = db.Table(table).query(
            ExclusiveStartKey=productQuery['LastEvaluatedKey'],
            IndexName=f'{indexName}',
            KeyConditionExpression=Key(f'{fieldName}').eq(text)
        )   
        items.extend(productQuery['Items'])
    return items