# Slackelot
Simple wrapper around the Slack Web API to post messages.


## Details

Slackelot contains a single function:  
`send_message(message, webhook_url, pretext='', title='', author_name='', color=None)`


**webhook_url** should be in the following format:
`'https://hooks.slack.com/services/TEAM_ID/BOT_OR_CHANNEL_ID/AUTH_TOKEN'`

*Example*
```
from slackelot import send_message


webhook_url = 'https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX'
message = 'Who wants to push the pram?\n@lancelot @percival'
pretext = 'Knights of the Round Table'
title = 'Spamelot'
author_name = 'Arthur'
color = '#663399'

send_message(message, webhook_url, pretext=pretext, title=title, author_name=author_name, color=color)
```
![https://github.com/Chris-Graffagnino/slackelot/blob/master/slackelot_example.png](https://github.com/Chris-Graffagnino/slackelot/blob/master/slackelot_example.png)

### Extra Goodness
Paid teams have the option to mention other subteams, (ie. channel). In that
case, you might append something like this to your message:

`'\n<!subteam^ID|HANDLE>'`
(replace `ID` and `HANDLE` with your subteam's id and name, respectively).

For more information on message formatting, see the [Slack API docs](https://api.slack.com/docs/message-formatting)


## FAQ

[Where do I find my Slack team id?](https://api.slack.com/methods/team.info/test)

[Where do I find my Slack channel ids?](https://api.slack.com/methods/channels.list/test)

[Where do I create a  Slack auth token?](https://api.slack.com/tokens)

[How do I create a Slack bot user?](https://api.slack.com/bot-users)



