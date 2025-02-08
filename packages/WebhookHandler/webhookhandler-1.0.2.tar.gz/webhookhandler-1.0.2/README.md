# DiscordWebhookManager

![License](https://img.shields.io/github/license/your-repo/WebhookHandler)
![Python Version](https://img.shields.io/pypi/pyversions/WebhookHandler)

A lightweight Python module for sending, editing, and managing Discord webhooks effortlessly.

## Features

- Send messages and embeds via Discord webhooks
- Edit and delete webhook messages
- Manage webhook settings (username, avatar, etc.)
- Retrieve webhook information from channels and guilds

## Installation

You can install DiscordWebhookManager via pip:

```sh
pip install WebhookHandler
```

## Quick Start

### Sending a Webhook Message

```python
from discord_webhook import Send

webhook_url = "your_webhook_url"
Send.normal(webhook_url, "Hello, Discord Webhook!")
```

### Sending an Embed Message

```python
Send.embed(
    url=webhook_url,
    title="Embed Title",
    description="This is an embedded message.",
    color=0xFF0000
)
```

### Editing a Webhook Message

```python
from discord_webhook import Edit

message_id = "your_message_id"
Edit.edit_message(webhook_url, message_id, "Updated content")
```

### Deleting a Webhook Message

```python
Edit.delete_message(webhook_url, message_id)
```

## Managing Webhooks

### Creating a Webhook

```python
Edit.create_webhook(channel_id="your_channel_id", name="New Webhook")
```

### Retrieving Webhooks

```python
from discord_webhook import Get

Get.channel_webhook("your_channel_id")
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Links

- [GitHub Repository](https://github.com/SyncWide-Solutions/WebhookHandler)
- [PyPI Package](https://pypi.org/project/WebhookHandler/)