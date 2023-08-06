Simple SlackCat
===============

Pipe command output to Slack from your terminal!

Installation
============

(This will change once registered w/ pypi).

1. Download slackcat to ``/usr/local/bin``
3. Make it executable ``chmod +x /usr/local/bin/slackcat``
3. add your slack webhook url to your bash profile:

```bash

export SLACKCAT_WEBHOOK_URL='https://hooks.slack.com/services/TXXX/BXXXX/ZZZ'
```

that's it. (Better docs coming, WIP)

Usage
=====

send to user from target path

```
slackcat @nick /path/to/file
```

send to user using pipes

```
cat /path/to/file | slackcat @nick
```

send to a channel

```
cat /path/to/file | slackcat "#general"
```
