from flask import session, request
import boto3
from boto3.dynamodb.conditions import Key,Attr
from botocore.client import Config
import requests
import os
from PIL import Image

s3 = boto3.resource('s3',
    aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', 
    aws_secret_access_key='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',
    config=Config(signature_version='s3v4')
    )

def get_all_music(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.scan()
    return response['Items']

def music_index(offset = 0, per_page = 10):
    p = get_all_music()
    return p[offset:offset+per_page]

def update_subscribtion(title,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Login')
    response = table.update_item(
        Key={
            'email' : session['user']
        },
    UpdateExpression="set subscription.title=:t",
    ExpressionAttributeValues={
        ':t' : title
    },
    ReturnValues="UPDATED_NEW"
    )
    return response

def scan_user(email,password,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')

    table = dynamodb.Table('Login')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email) & Key('password').eq(password)
    )
    return response['Items']

def create_user(email,user_name,password,dynamodb=None):
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

def scan_for_duplicate(email,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')

    table = dynamodb.Table('Login')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response['Items']

def scan_duplicate_username(username,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')

    table = dynamodb.Table('Login')
    response = table.scan(
        FilterExpression=Key('user_name').eq(username)
    )
    return response['Items']

def check_sub(email,title,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')

    table = dynamodb.Table('Subscribe')
    response = table.scan(
        FilterExpression=Attr('email').eq(email) & Attr('title').eq(title)
    )
    return response['Items']

def query_all_sub(email,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Subscribe')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response['Items'] 

def delete_sub(email,title,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Subscribe')
    response = table.delete_item(
        Key={
            'email' : email,
            'title' : title
        }
    )
    return response

def query_music_by_title(title,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.query(
        KeyConditionExpression=Key('title').eq(title)
    )
    return response['Items'] 

def query_music_by_artist(attr,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.scan(
        FilterExpression=Attr('artist').eq(attr)
    )
    return response['Items']

def query_music_by_year(year,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.scan(
        FilterExpression= Attr('year').eq(year)
    )
    return response['Items']

def query_music_by_year_title(title,year,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.scan(
        FilterExpression=Attr('year').eq(year) & Attr('title').eq(title)
    )
    return response['Items']

def query_music_by_year_artist(artist,year,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.scan(
        FilterExpression=Attr('year').eq(year) & Attr('artist').eq(artist)
    )
    return response['Items']
def query_music_by_title_artist(title,artist,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.scan(
        FilterExpression=Attr('title').eq(title) & Attr('artist').eq(artist)
    )
    return response['Items']

def query_music_by_all_three(title,artist,year,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    table = dynamodb.Table('Musics')
    response = table.query(
        KeyConditionExpression=Key('artist').eq(artist) & Key('title').eq(title),
        FilterExpression=Attr('year').eq(year)
    )
    return response['Items']


def get_search_result(title,artist,year,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAU62FGA2O7DO7DGQ2', aws_secret_access_key='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', region_name='us-east-1')
    results = []
    emp= ""
    if title is emp and year is emp:
        results = query_music_by_artist(artist)
    elif artist is emp and year is emp:
        results = query_music_by_title(title)
    elif year is emp:
        results = query_music_by_title_artist(title,artist)
    elif artist is emp and title is emp:
        results = query_music_by_year(year)
    elif artist is emp:
        results = query_music_by_year_title(title,year)
    elif title is emp:  
        results = query_music_by_year_artist(artist, year)
    elif title and year and artist: 
        results = query_music_by_all_three(title,artist,year) 
    if len(results) == 0:
        flash('No result is retrieved. Please query again!','danger')
    return results

from forms import SearchForm