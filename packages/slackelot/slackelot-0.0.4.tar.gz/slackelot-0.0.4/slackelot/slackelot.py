import time
import requests


class SlackNotificationError(Exception):
    pass


def send_message(message, webhook_url, pretext='', title='', author_name='', color=None):
    """Send slack message using webhooks

    Args:
        message (string)
        webhook_url (string), 'https://hooks.slack.com/services/{team id}/{bot or channel id}/{auth token}'
        pretext (string)
        title (string)
        author_name (string)
        color (string) e.g. '#336699'
    """
    if 'https://hooks.slack.com/services/' not in webhook_url:
        raise SlackNotificationError(
            'webhook_url is not in the correct format. It should look like this:\n\
            https://hooks.slack.com/services/{team id}/{bot or channel id}/{auth token}')

    fallback ='\n'.join([title, author_name, message])

    payload = {
        'attachments': [
            {
                'fallback': fallback,
                'color': color,
                'pretext': pretext,
                'author_name': author_name,
                'title': title,
                'text': message,
                'mrkdwn_in': ['text', 'pretext']
            }
        ],
        'link_names': '1',
        'as_user': True
    }

    for i in range(10):
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            return True
        else:
            time.sleep(3)
        # If the notification doesn't go through after 10 attempts, raise an error.
        raise SlackNotificationError('Slack notification failed after 10 attempts.')
