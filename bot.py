
import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

def main():
    offset = None

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": 50,
                    "allowed_updates": ["chat_join_request"]
                },
                timeout=60
            ).json()

            if not response.get("ok"):
                continue

            for update in response["result"]:
                offset = update["update_id"] + 1
                request = update.get("chat_join_request")

                if request:
                    result = requests.post(
                        f"{API}/approveChatJoinRequest",
                        json={
                            "chat_id": request["chat"]["id"],
                            "user_id": request["from"]["id"]
                        },
                        timeout=20
                    )
                    print(result.text)

        except Exception as error:
            print(error)

if __name__ == "__main__":
    main()
