import boto3


def create_login_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName= "Login",
        KeySchema=[
            {

            'AttributeName': 'email',

            'KeyType': 'HASH' 

            },
            {

            'AttributeName': 'password',

            'KeyType': 'RANGE' 

            }
        ],

        AttributeDefinitions=[
            {
            'AttributeName': 'email',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'password',
            'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
            }
        )

    return table
        
def create_music_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName='Musics',
        KeySchema=[
            {
            'AttributeName': 'title',
            'KeyType': 'HASH' 
            },
            {
            'AttributeName': 'artist',
            'KeyType': 'RANGE' 
            }
            
        ],
        AttributeDefinitions=[
            {
            'AttributeName': 'title',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'artist',
            'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
            }

        )
    table.wait_until_exists()
    return table

def create_sub_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName= "Subscribe",
        KeySchema=[
            {

            'AttributeName': 'email',

            'KeyType': 'HASH' 

            },
            {

            'AttributeName': 'title',

            'KeyType': 'RANGE' 

            }
        ],

        AttributeDefinitions=[
            {
            'AttributeName': 'email',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'title',
            'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
            }
        )

    return table



if __name__ == '__main__':
    music_table = create_music_table()
    login_table = create_login_table()
    sub_table = create_sub_table()
