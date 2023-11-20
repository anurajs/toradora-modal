import datetime
from os import environ
import requests
import modal

stub = modal.Stub("toradora-webhook")
image = modal.Image.debian_slim().pip_install(["requests"])


@stub.function(
    schedule=modal.Cron("50 17 6-31 12 *"),
    secret=modal.Secret.from_name("toradora-webhook-secrets"),
    image=image,
)
def execute_hook():
    webhook_id = environ.get("WEBHOOK_ID")
    webhook_token = environ.get("WEBHOOK_TOKEN")
    role_id = environ.get("ROLE_ID")

    day = datetime.date.today().day
    episode = "Watching special episode" if day == 31 else f"Watching episode {day - 5}"
    body = {"content": f"<@&{role_id}> Watching toradora in 10 mins.\n{episode}"}
    url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"

    requests.post(url, body)


@stub.local_entrypoint()
def main():
    execute_hook.remote()
