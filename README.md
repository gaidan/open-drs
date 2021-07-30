# open-drs
DRS Review system in cricket for python.

# Usage
```
python open-drs.py number-of-frames folder balltype WxH amount-of-pixels-per-image-to-count-as-ball
```
<br>
Note that the last argument can be set to 0 if every frame contains the ball, it is just so that a frame without the ball, which may contain 10 pixels the same colour as the ball does not get misconstrued as a ball by the drs system. <br>

# Ball Types
p - pink <br>
r - red <br>

# Folder
Inside the folder frames, create a folder for the ball with images inside each labeled out-xxx.jpg, e.g. frames/ball1/out-009.jpg
