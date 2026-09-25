"""Verify the generated key can process events but cannot list the audio bucket."""
import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError

values = json.loads(os.environ['METRICS_BOOTSTRAP_JSON'])
client = boto3.client('s3', endpoint_url=f"https://{values['vault_metrics_r2_account_id']}.r2.cloudflarestorage.com",
    aws_access_key_id=values['vault_metrics_r2_access_key_id'],
    aws_secret_access_key=values['vault_metrics_r2_secret_access_key'], region_name='auto')
bucket = 'bitflip-analytics-events'
key = 'verification/' + str(uuid.uuid4())
try:
    client.list_objects_v2(Bucket=bucket, MaxKeys=1)
    client.put_object(Bucket=bucket, Key=key, Body=b'bitflip-metrics-key-check')
    try:
        assert client.get_object(Bucket=bucket, Key=key)['Body'].read() == b'bitflip-metrics-key-check'
    finally:
        client.delete_object(Bucket=bucket, Key=key)
    try:
        client.list_objects_v2(Bucket='bitflip-audio', MaxKeys=1)
    except ClientError as error:
        if error.response['Error']['Code'] not in ('AccessDenied', 'Unauthorized', 'AllAccessDisabled'):
            raise
    else:
        raise ValueError('metrics key unexpectedly has access to the audio bucket')
except Exception:
    raise SystemExit('R2 key verification failed; secret-bearing error details suppressed') from None
print('Verified event list/write/read/delete and denied audio bucket access.')
