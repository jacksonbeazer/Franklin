import os
import time
from slackclient import SlackClient
from subprocess import Popen
import csv


Franklin = "ABCDEFG"


# instantiate Slack client
token = "xxxx-1234-5678"
slack_client = SlackClient(token)

def filter_func (rtm_output):
	output = rtm_output
	if output and len(output) > 0:
		for i in output:
			if i and 'text' in i and len(i['text']) >0:
				return i['text'], i['channel'], i['user']
	return None, None, None
				
def reply_func (text, channel):
	response = "I don't know how to do that yet."
	if "resend daily" in text or "Resend daily" in text:
		response = "I'll take care of that right now."
		Popen("C:\TabCMD\scripts\Resend_Scripts\Daily_Resend.bat")
	elif "resend GTM" in text or "Resend GTM" in text:
		response = "I'll take care of that right now."
		os.chdir('C:\TabCMD\scripts')
		import GTM
	elif "resend completed daily" in text or "Resend completed daily" in text:
		response = "I'll take care of that right now."
		Popen("C:\TabCMD\scripts\Resend_Scripts\weekly_review_resend.bat")
	elif "resend GAP" in text or "Resend GAP" in text:
		response = "I'll take care of that right now."
		Popen("C:\TabCMD\scripts\Resend_Scripts\GAP_resend.bat")
	elif "disable daily" in text or "Disable daily" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Disabling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\Daily_Dash_Disable.bat")
		response = "Done"
	elif "enable daily" in text or "Enable daily" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Enabling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\Daily_Dash_Enable.bat")
		response = "Done"
	elif "disable GAP" in text or "Disable GAP" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Disabling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\GAP_Disable.bat")
		response = "Done"
	elif "enable GAP" in text or "Enable GAP" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Enabling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\GAP_Enable.bat")
		response = "Done"
	elif "disable completed daily" in text or "Disable completed daily" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Disabling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\WIR_Disable.bat")
		response = "Done"
	elif "enable completed daily" in text or "Enable completed daily" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Enabling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\WIR_Enable.bat")
		response = "Done"
	elif "status" in text or "Status" in text:
		slack_client.api_call("chat.postMessage", channel=channel, text="Compiling...", as_user=True)
		Popen("C:\TabCMD\scripts\Enable_Disable\Status.bat")
		os.chdir('C:\TabCMD\scripts\Enable_Disable')
		files = ['Daily_status.csv', 'GAP_Status.csv', 'WIR_Status.csv']
		file_list = []
		for i in files:
			f = open(i,'rb')
			reader = csv.reader(f)
			file_list.append(list(reader))
		response = "\n".join([file_list[0][1][0].split('\\')[2]+": "+file_list[0][1][2],file_list[1][1][0].split('\\')[2]+": "+file_list[1][1][2],file_list[2][1][0].split('\\')[2]+": "+file_list[2][1][2]])
	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


#Interact with Slack Messages
if slack_client.rtm_connect():
	print("Franklin's alive!")
	while True:
		text, channel, user  = filter_func(slack_client.rtm_read())
		if text and channel and str(user) != Franklin:
			reply_func(text, channel)
		time.sleep(1)
		
