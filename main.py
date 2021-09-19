import cv2
import argparse
from video import VideoCaptureWindow
from frameprocessing import ConditionalFrameEvaluator, NotYourFaceChecker, MultipleFaceChecker, FrameDebugger
from slackbot import SlackBot
import os
from datetime import datetime
import time

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

def get_conditional_evaluator(args):
    if args.condition == 'not-my-face':
        if not args.user_img_file:
            print('Need --user_img_file argument for not-my-face condition')
            return None
        return ConditionalFrameEvaluator(NotYourFaceChecker(args.user_img_file), args.frames)
    elif args.condition == 'multi-face':
        return ConditionalFrameEvaluator(MultipleFaceChecker(), args.frames)
    else:
        return None


def main(args):
    # define a video capture object
    video_capture = cv2.VideoCapture(0)

    window = VideoCaptureWindow()

    conditional_evaluator = get_conditional_evaluator(args)

    if not conditional_evaluator:
        return

    debugger = FrameDebugger() if args.debug else None

    slack_user_id, slack_bot_token = get_user_id_and_token_from_env()
    if not slack_user_id or not slack_bot_token:
        return

    slack_bot = SlackBot(slack_user_id, slack_bot_token, conditional_evaluator.alert())

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

        window_event = window.handle_button_event()
        if window_event == VideoCaptureWindow.QUIT_BUTTON:
            break

        if window_event == VideoCaptureWindow.PAUSE_BUTTON:
            print('Video Capture paused!')
            while True:
                time.sleep(0.5)
                if window.handle_button_event() == VideoCaptureWindow.PAUSE_BUTTON:
                    print('Video Capture unpaused!')
                    break


    # Release the video capture object
    video_capture.release()

    # Destroy the video capture window
    window.destroy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('condition', choices=['not-my-face', 'multi-face'], help='the condition that is in each frame')
    parser.add_argument('frames', type=int, help='number of frames that satisfies a condition before sending slack message')
    parser.add_argument('--debug', action='store_true', help='flag turns on debug logic')
    parser.add_argument('--with_image', action='store_true', help='sends captured image with alert through slack')
    parser.add_argument('--user_img_file', help='user image file used for classification')
    main(parser.parse_args())