# CloudWatch SNS Notificaitons into Microsoft Teams
# Author: Seff Parker
# Version: 20210612
# URL: https://github.com/seffparker/aws-cloudwatch-msteams-notification

import json
import logging
import os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HOOK_URL = os.environ['WebhookUrl']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    namespace = message['Trigger']['Metrics'][0]['MetricStat']['Metric']['Namespace']
    resource = message['Trigger']['Metrics'][0]['MetricStat']['Metric']['Dimensions'][0]['value']
    metric = message['Trigger']['Metrics'][0]['MetricStat']['Metric']['MetricName']
    if "AccountId" in os.environ:
        awsAccountId = os.environ['AccountId']
    else:
        awsAccountId = message['AWSAccountId']
    
    if new_state.lower() == 'alarm':
        state_colour = "ff3300"
    elif new_state.lower() == 'ok':
        state_colour = "009900"
    else:
        state_colour = "cccccc"

    base_data = {
        "colour": state_colour,
        "title": new_state + ": " + alarm_name,
        "info": [ 
            { "facts":
                [{ "name": "Status", "value": "Changed from " + old_state + " to " + new_state },
                 { "name": "Resource", "value": namespace + "/" + resource + " in account " + awsAccountId},
                 { "name": "Metric", "value":  metric },
                 { "name": "Summary", "value": reason }
                 ], "markdown": 'true' }
            ]
    }

    messages = {
        ('ALARM', 'my-alarm-name'): {
            "colour": "d63333",
            "title": "Red Alert - A bad thing happened.",
            "text": "These are the specific details of the bad thing."
        },
        ('OK', 'my-alarm-name'): {
            "colour": "64a837",
            "title": "The bad thing stopped happening",
            "text": "These are the specific details of how we know the bad thing stopped happening"
        }
    }
    data = messages.get((new_state, alarm_name), base_data)

    message = {
      "summary": "summary",
      "@context": "https://schema.org/extensions",
      "@type": "MessageCard",
      "themeColor": data["colour"],
      "title": data["title"],
      "sections": data["info"]
    }

    req = Request(HOOK_URL, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted")
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
