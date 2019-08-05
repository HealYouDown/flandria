from discord_webhooks import DiscordWebhooks

WEBHOOK_URL = "https://discordapp.com/api/webhooks/\
    607912891643068427/bblw4t0nhO530QZJ842Q92mhYXFfBeSf5xP6M2y7LicHHyn23mZykaVETykoI9ZS9aEz"

# Initialize the webhook class and attaches data.
webhook = DiscordWebhooks(WEBHOOK_URL)

# Sets some content for a basic message.
webhook.set_content(content='Drop added!')

# Triggers the payload to be sent to Discord.
webhook.send()
