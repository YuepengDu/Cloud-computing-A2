from decimal import Decimal
import json
import boto3
import boto3.s3
import requests
import os
import urllib
from botocore.client import Config

s3 = boto3.resource('s3',
    aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', 
    aws_secret_access_key='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',
    config=Config(signature_version='s3v4')
    )

def load_musics(musics, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    
    table = dynamodb.Table('Musics')
    for music in musics["songs"]: 
        title = music['title']
        artist = music['artist']
        year = music['year']
        web_url = music['web_url']
        image_url = music['img_url']  
        table.put_item(Item=music) 
        bucket_name = "1musicpic"
        req_for_image = requests.get(image_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()
        s3.Bucket(bucket_name).put_object(Key=title, Body=req_data)

def put_user(email,user_name,password,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Login')
    user = table.put_item(
        Item={
            'email' : email,
            'user_name' : user_name,
            'password' : password
        }
    )
    return user

def put_sub(email,title,artist,year,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Subscribe')
    sub = table.put_item(
        Item={
            'email' : email,
            'title' : title,
            'artist' : artist,
            'year' : year
        }
    )
    return sub

if __name__ == '__main__':
    with open("a2.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
    load_musics(music_list)
    put_user('s36987280@student.rmit.edu.au','Yuepeng Du 0','012345')
    put_user('s36987281@student.rmit.edu.au','Yuepeng Du 1','123456')
    put_user('s36987282@student.rmit.edu.au','Yuepeng Du 2','234567')
    put_user('s36987283@student.rmit.edu.au','Yuepeng Du 3','345678')
    put_user('s36987284@student.rmit.edu.au','Yuepeng Du 4','456789')
    put_user('s36987285@student.rmit.edu.au','Yuepeng Du 5','567890')
    put_user('s36987286@student.rmit.edu.au','Yuepeng Du 6','678901')
    put_user('s36987287@student.rmit.edu.au','Yuepeng Du 7','789012')
    put_user('s36987288@student.rmit.edu.au','Yuepeng Du 8','890123')
    put_user('s36987289@student.rmit.edu.au','Yuepeng Du 9','901234')