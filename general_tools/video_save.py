import cv2
from datetime import datetime

def gen_time():
    now = datetime.now()
    dt_string = now.strftime("%H%M%S_%m%d%Y")
    return dt_string  

# Create an object to read 
# from camera
url = 0
video = cv2.VideoCapture(url)
   
# We need to check if camera
# is opened previously or not
if (video.isOpened() == False): 
    print("Error reading video file")
  
# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))
fps = video.get(cv2.CAP_PROP_FPS)

size = (frame_width, frame_height)
   
# Below VideoWriter object will create
# a frame of above defined The output 
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('%s.mp4' %gen_time(), 
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         fps, size)
    
while(True):
    ret, frame = video.read()
  
    if ret == True: 
  
        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)
  
        # Press S on keyboard 
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
  
    # Break the loop
    else:
        break
  
# When everything done, release 
# the video capture and video 
# write objects
video.release()
result.release()
    
# Closes all the frames
   
print("The video was successfully saved")
