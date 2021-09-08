import cv2
import argparse
from video import VideoCaptureWindow
from frameprocessing import ConditionalFrameEvaluator, MultipleFaceChecker, FrameDebugger
from slackbot import SlackBot
import os
from datetime import datetime

def get_user_id_and_token_from_env():
    try:
        slack_user_id   = os.environ['SLACK_USER_ID']
        slack_bot_token = os.environ['SLACK_BOT_TOKEN']
        return (slack_user_id, slack_bot_token)

    except KeyError as e:
        print("Tried to initialize SlackBot, but a required environent variable wasn't set!")
        print("Ensure you set environment variables: SLACK_BOT_TOKEN and SLACK_USER_ID!")
        print("SlackBot ")
        return (None, None)

def main(args):
    # define a video capture object
    video_capture = cv2.VideoCapture(0)

    window = VideoCaptureWindow()

    conditional_evaluator = ConditionalFrameEvaluator(MultipleFaceChecker(), args.frames)

    debugger = FrameDebugger() if args.debug else None

    slack_user_id, slack_bot_token = get_user_id_and_token_from_env()
    if not slack_user_id or not slack_bot_token:
        return

    slack_bot = SlackBot(slack_user_id, slack_bot_token, "Multiple faces detected!")

    while(True):
        # Capture the video frame by frame
        ret, frame = video_capture.read()

        window.generate()

        if debugger:
            debugger.debug(frame)

        if conditional_evaluator.evaluate(frame):
            print("Condition threshold met in frame, sending slack alert")
            if args.with_image:
                image_file_name = f'captured_image_{datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")}.jpg'
                cv2.imwrite(image_file_name, frame)
                slack_bot.send_user_alert_with_img(image_file_name) 
            else:
                slack_bot.send_user_alert()

        # Display the resulting frame
        window.update_frame(frame)

        if window.exit_event():
            break

    # Release the video capture object
    video_capture.release()

    # Destroy the video capture window
    window.destroy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frames', type=int, help='number of frames that satisfies a condition before sending slack message')
    parser.add_argument('--debug', action='store_true', help='flag turns on debug logic')
    parser.add_argument('--with_image', action='store_true', help='sends captured image with alert through slack')
    main(parser.parse_args())