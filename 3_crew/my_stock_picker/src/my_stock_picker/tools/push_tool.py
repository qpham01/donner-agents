from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class PushNotificationInput(BaseModel):
    """A message to be send to the user."""
    message: str = Field(..., description="Message to be sent to the user.")

class PushNotificationTool(BaseTool):
    name: str = "Send a push notification to the user"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotificationInput

    def _run(self, message: str) -> str:
        # Implementation goes here
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = f"https://api.pushover.net/1/messages.json"

        print(f"Push notification: {message}")
        payload = {
            "token": pushover_token,
            "user": pushover_user,
            "message": message
        }
        response = requests.post(pushover_url, data=payload)
        return response.json()
