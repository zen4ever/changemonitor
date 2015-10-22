import boto3
import difflib
import hashlib
import requests
from botocore.exceptions import ClientError


def check_if_changed(url, bucket_name):
    """
    Polls a given URL, checks if there are any differences from previous version.
    Then stores a current version in S3 bucket.
    Returns a unified diff generator.
    """
    response = requests.get(url)
    s3 = boto3.resource('s3')
    key = hashlib.md5(url).hexdigest()
    obj = s3.Object(bucket_name, key)
    try:
        obj_body = obj.get()
        previous_version = obj_body['Body'].read()
    except ClientError:
        previous_version = response.content
    obj.put(Body=response.content)
    return difflib.unified_diff(
        [x.rstrip() for x in response.content.splitlines()],
        [x.rstrip() for x in previous_version.splitlines()],
        lineterm=""
    )


def notify(sns_topic_arn, diff_text, url):
    """
    Sends a message with your changes to to SNS topic
    """
    sns = boto3.resource('sns')
    topic = sns.Topic(sns_topic_arn)
    topic.publish(
        Message=diff_text,
        Subject="Content for {url} has changed".format(url=url)
    )
