from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class SlackBot:
	def __init__(self, slack_user_id, slack_bot_token, alert_message):
		self.user_id = slack_user_id
		self.client = WebClient(token=slack_bot_token)
		self.alert_message = alert_message

	def send_user_alert(self):
		try:
			response = self.client.chat_postMessage(
				channel=f"@{self.user_id}",
				text=self.alert_message
			)
			
		except SlackApiError as e:
			print(f"Error sending message: {e}")

	def send_user_alert_with_img(self, image_file_name):
		try:
			response = self.client.files_upload(
				channels=f"@{self.user_id}",
				title="Slack Bot",
				initial_comment=self.alert_message,
				file=image_file_name
			)

		except SlackApiError as e:
			print(f"Error uploading file: {e}")