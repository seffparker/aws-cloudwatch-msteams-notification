# AWS CloudWatch Teams Notification
Push AWS CloudWatch Notifications into Microsoft Teams as Webhook using AWS Lambda Function

This is an improved version of https://medium.com/@sebastian.phelps/aws-cloudwatch-alarms-on-microsoft-teams-9b5239e23b64

# AWS Lambda Function
 - **Runtime:** Python 3.8
 - **Code:** aws-cloudwatch-msteams-notification.py
 - **Environment Variables:** 

| KEY        | VALUE                    | SCOPE    |
|------------|--------------------------|----------|
| WebhookUrl | https://webhook_url_here | Required |
| AccountId  |      My AWS Account      | Optional |

# SNS Topic
- **Type:** Standard
- **Access Policy**: (Proceed with default)
- **Subscription**: (The Lambda function Name or ARN)

# CloudWatch Alarm
- **SNS Topic:** (The SNS Topic Name or ARN)

# Microsoft Teams Incoming Webhook
Refer [here](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) to generate a WebHook URL for a Teams Channel.

# Sample Notificaiton
![Sample Teams Notification](/cloudwatch-teams-notification.png)
