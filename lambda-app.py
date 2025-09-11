import io
import json
import logging
import os
import sys
# sys.path.append('/mnt/efs/msgraph/python/lib/python3.11/site-packages')# access point root.path=/lambda


import pathlib

import asyncio

# import dotenv
# dotenv.load_dotenv('/Users/cn/sn/env/dev.env')

# Values from app registration
s3_bucket = os.getenv('AWS_S3_BUCKET', '')
username = os.getenv('MICROSOFT_GRAPH_USERNAME')
client_id = os.getenv('MICROSOFT_GRAPH_CLIENTID')
client_secret = os.getenv('MICROSOFT_GRAPH_CLIENTSECRET')
# Multi-tenant apps can use "common",
# single-tenant apps must use the tenant ID from the Azure portal
tenant_id = os.getenv('MICROSOFT_GRAPH_TENANTID', 'common')
scopes_1 = os.getenv('MICROSOFT_GRAPH_SCOPE_1', 'https://graph.microsoft.com/.default')

import boto3
import botocore.client
import botocore.session
session = boto3.Session(botocore_session=botocore.session.get_session())
config = botocore.client.Config(connect_timeout=5, read_timeout=5)
s3 = session.client("s3", config=config)

def send_mail(body):
    from msgraph.generated.models.body_type import BodyType
    from msgraph.generated.models.file_attachment import FileAttachment
    import graph
    api = graph.GraphApi(username, tenant_id, client_id, client_secret, [scopes_1])
    if isinstance(body, str):
        body = json.loads(body)
    to = body['to']
    cc = body['cc'] if 'cc' in body else None
    # 如果to和cc为字符串，则用[,; ]分割转换为列表
    if isinstance(to, str):
        to = to.replace('，', ';').replace('；', ';').replace(' ', ';')
        to = to.split(';')
    if isinstance(cc, str):
        cc = cc.replace('，', ';').replace('；', ';').replace(' ', ';')
        cc = cc.split(';')

    subject = body['subject']
    content = body['content'] if 'content' in body else ''
    content_type = body['content_type'] if 'content_type' in body else BodyType.Html
    s3bucket = body['s3bucket'] if 's3bucket' in body else None

    if 's3' == content_type:
        content = s3.get_object(Bucket=s3bucket, Key=content)['Body'].read().decode('utf-8')
    content_type = BodyType.Html # if content_type == 'html' else BodyType.Text

    s3_attachments= body['s3_attachments'] if 's3_attachments' in body else []  # attachments store on s3
    attachments = [FileAttachment(
        # odata_type = "#microsoft.graph.fileAttachment",
        name=pathlib.Path(s3key).name,
        content_bytes=s3.get_object(Bucket=s3bucket, Key=s3key)['Body'].read(),
    ) for s3key in s3_attachments]

    asyncio.run(api.sendMail(
        to,
        subject,
        content_type,
        content,
        attachments,
        cc
    ))

def codedeploy(subject, message):
    # get mail account list
    configkey = 'codedeploy/notify-config.json'
    config = json.loads(s3.get_object(Bucket=s3_bucket, Key=configkey)['Body'].read().decode('utf-8'))
    body = {
        'to': config['to'],
        'cc': config['cc'],
        'subject': f"{'🟢' if message['status']=='SUCCEEDED' else '🔴'}{message['applicationName']}:{subject}",
        'content_type': 'html',
        'content': f'''
            <table>
            <tr><td>applicationName</td><td> {message['applicationName']}</td></tr>
            <tr><td>eventTriggerName</td><td> {message['eventTriggerName']}
            <tr><td>status</td><td> <text style="color:{'green' if message['status']=='SUCCEEDED' else 'red'}">{message['status']}</text></td></tr>
            <tr><td>deploymentId</td><td> {message['deploymentId']}</td></tr>
            <tr><td>deploymentGroupName</td><td> {message['deploymentGroupName']}</td></tr>
            <tr><td>createTime</td><td>{message['createTime']}</td></tr>
            <tr><td>completeTime</td><td> {message['completeTime']}</td></tr>
            <tr><td>deploymentOverview</td><td> {message['deploymentOverview']}</td></tr>
            <tr><td>creator</td><td> {message['creator']}</td></tr>
            </table>
            <br><image src="https://www.smith-nephew.com/-/media/project/smithandnephew/examples/logo.svg">
        '''
        .replace('                ', '')
        .replace('\n', '<br>\n')
    }
    send_mail(body)

# curl "http://localhost:8080/2015-03-31/functions/function/invocations" -d @$PWD/src/data/sendmail.json
def index(event, context):
    print(json.dumps(event))
    records = event['Records'] # sns
    for record in records:
        if 'Sns' in record:
            sns = record['Sns']
            subject = sns['Subject']
            message = json.loads(sns['Message'])
            if 'deploymentId' in message:
                codedeploy(subject, message)
            else:
                logging.error('Unsupport SNS message', json.dumps(event))
            #if '' in message:
        else:
            body = record
            send_mail(body)

    return {
        'statusCode': 200,
        'body': json.dumps(records)
    }


if __name__ == "__main__":
    event = json.loads(io.open('src/data/sendmail.json').read())
    index(event, None)
