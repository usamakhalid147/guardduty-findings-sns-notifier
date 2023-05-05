GuardDuty-to-SNS Notifier
This script is a Python Lambda function that retrieves GuardDuty findings from the last hour and publishes them to an SNS topic.

Getting Started
To use this script, you will need:

An AWS account
The AWS CLI installed and configured
The AWS SDK for Python (Boto3)
Installation
Clone this repository or download the script.
Create an SNS topic and note the ARN.
Create an IAM role for the Lambda function with permissions to access GuardDuty and publish to the SNS topic. The policy should look something like this:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "guardduty:ListFindings",
        "guardduty:GetFindings"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:us-east-1:123456789012:my-topic"
    }
  ]
}
Set the environment variables DETECTOR_ID and SNS_TOPIC_ARN in the Lambda function configuration.
Deploy the script as a Python Lambda function.
Usage
When the Lambda function is triggered, it will retrieve GuardDuty findings from the last hour and publish them to the specified SNS topic. If no new findings are found, it will return a message saying so.
