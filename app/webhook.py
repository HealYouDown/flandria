import os

from discord_webhooks import DiscordWebhooks

WEBHOOK_URL = os.environ.get("DROPS_WEBHOOK_URL", None)
BASE_URL = "https://www.flandria.info"

# Colors as decimal
GREEN = 3329330
RED = 15605837
LIGHTBLUE = 5674452


def get_image_url(path):
    return BASE_URL + "/static/assets/" + path


def get_item_url(item):
    return BASE_URL + f"/database/{item.table}/{item.code}"


def send_add_drop_webhook(monster, item, user):
    if WEBHOOK_URL is None:
        return

    webhook = DiscordWebhooks(WEBHOOK_URL)
    webhook.set_content(
        title=item.name, description=f"was added to {monster.name}",
        color=GREEN, url=get_item_url(item)
    )

    item_icon_url = get_image_url("item_icons/" + item.icon)
    webhook.set_thumbnail(url=item_icon_url)

    webhook.set_footer(text=f"by {user.username}")

    webhook.send()


def send_delete_drop_webhook(monster, item, user):
    if WEBHOOK_URL is None:
        return

    webhook = DiscordWebhooks(WEBHOOK_URL)
    webhook.set_content(
        title=item.name, description=f"was deleted from {monster.name}",
        color=RED, url=get_item_url(item)
    )

    item_icon_url = get_image_url("item_icons/" + item.icon)
    webhook.set_thumbnail(url=item_icon_url)

    webhook.set_footer(text=f"by {user.username}")

    webhook.send()


def send_edit_drop_webhook(monster, item, quantity, user):
    if WEBHOOK_URL is None:
        return

    webhook = DiscordWebhooks(WEBHOOK_URL)
    webhook.set_content(
        title=item.name, description=f"from {monster.name} was edited.",
        color=LIGHTBLUE, url=get_item_url(item)
    )

    item_icon_url = get_image_url("item_icons/" + item.icon)
    webhook.set_thumbnail(url=item_icon_url)

    webhook.add_field(name="Quantity", value=quantity)

    webhook.set_footer(text=f"by {user.username}")

    webhook.send()
