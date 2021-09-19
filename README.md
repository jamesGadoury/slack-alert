# slack-alert
Alerts a configured slack user of whether some condition has been met for a certain threshold of frames captured in a video camera.

## Configuration
You need to set a `SLACK_BOT_TOKEN` and a `SLACK_USER_ID` environment variables. For `SLACK_BOT_TOKEN`, you need to setup a slack app on api.slack.com and create a bot token by adding an authorization to the slack app. You need the `chat::write` and `files::write` authorizations for your app. For `SLACK_USER_ID` click on more under your profile in slack and click 'Copy member ID'. 

## How To Use
The current behavior is for the executable to capture video data from your camera and check if some condition has been fulfilled for more than the count equal to the `frames` position argument. The `condition` argument options are `not-my-face` or `multi-face`. `not-my-face` requires the argument `user_img_file` which is a path to a picture of your face, and will check every frame to see if there is a face not your own in the frame. The `multi-face` condition just checks if there is more than one face in the scene. If the condition is fulfilled for more frames than the `frames` positional argument, it will send a slack message using the bot to the configured user id. Running the following will send a slack message to the configured user id after seeing another face for more than 10 frames:
```bash
python3 main.py multi-face 10
```
ALternatively, you can use your own picture and check for faces that aren't your own in the frame:
```bash
python3 main.py not-my-face 10 --user_img_file my_pic.jpg
```
There is also a debug flag you can run, that will add debug information to the video stream. The current behavior is to draw squares around faces.
```bash
python3 main.py multi-face 10 --debug
```
You can also have the last image that met the threshold saved and sent to the configured slack user id as follows:
```bash
python3 main.py multi-face 10 --with_image
```
When the video is streaming, you can press 'q' on the window to quit and 'p' on the window to pause/unpause the stream.