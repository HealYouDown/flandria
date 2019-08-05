import hmac
import hashlib
from flask import current_app, request
import git


def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


def update_server():
    x_hub_signature = request.headers.get("X-Hub-Signature", None)
    if x_hub_signature is None:
        return "Missing signature"

    github_webhook_secret = current_app.config["GITHUB_WEBHOOK_SECRET"]

    if not is_valid_signature(x_hub_signature, request.data, github_webhook_secret):
        return "Unvalid"

    repo = git.Repo("https://github.com/HealYouDown/flandria")
    origin = repo.remotes.origin

    pull_info = origin.pull()

    return "Updated server"
