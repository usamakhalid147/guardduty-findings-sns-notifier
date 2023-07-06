import boto3
import os
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize boto3 clients for GuardDuty and SNS
    guardduty_client = boto3.client('guardduty')
    sns_client = boto3.client('sns')
t
    # Set the GuardDuty detector ID and SNS Topic ARN as environment variables
    detector_id = os.environ['DETECTOR_ID']
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']

    # Get the GuardDuty findings
    findings = guardduty_client.list_findings(DetectorId=detector_id)

    # Get the current time and subtract 1 hour
    current_time = datetime.utcnow()
    one_hour_ago = current_time - timedelta(hours=1)

    # If there are findings, publish the ones from the last hour to the SNS topic
    if findings['FindingIds']:
        for finding_id in findings['FindingIds']:
            finding = guardduty_client.get_findings(DetectorId=detector_id, FindingIds=[finding_id])

            # Convert the 'CreatedAt' string to a datetime object
            finding_date = datetime.strptime(finding['Findings'][0]['CreatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # Check if the finding was created within the last hour
            if finding_date > one_hour_ago:
                # Publish the finding to the SNS topic
                sns_client.publish(
                    TopicArn=sns_topic_arn,
                    Message=json.dumps({'id': finding_id, 'created_at': finding_date.isoformat()}),
                    Subject='New GuardDuty Finding'
                )

        return {
            'statusCode': 200,
            'body': 'Findings from the last hour sent to the SNS topic'
        }
    else:
        return {
            'statusCode': 200,
            'body': 'No new findings found'
        }
