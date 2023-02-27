# -- User Configuration Settings for motrack.py -------

#======================================
# Logging Settings
#======================================
LOGGING_ON = True     # Show individual track xy points
SHOW_SETTINGS = True   # Display settings on launch


#======================================
# Camera and Image Settings
#======================================
CAMERA = "usbcam"    # valid values usbcam, rtspcam, pilibcam, pilegcam
 
USBCAM_SRC = 0
RTSPCAM_SRC = "rtsp://user:passwd@192.168.1.200:554/12"  # Set per IP Cam Docs and config

# NOTE: To Scan for Pi Lib or legacy CAM Set WEBCAM_ON and IPCAM_ON to False

IM_PREFIX = "track-"   # Prefix for image files
IM_DIR = "./media/images"  # directory for saving images (auto created)
IM_SIZE = (640, 480)   # Image resolution (width, height) pixels
IM_BIGGER = 1.75       # Resize the stream image before saving
IM_VFLIP = True        # True enables flipping image vertically
IM_HFLIP = True        # True enables flipping image horizonally.
IM_FRAMERATE = 30      # Legacy Picamera Framerate

#======================================
# Motion Tracking Settings
#======================================
TRACK_MIN_AREA = 500    # Minimum area of contours to track
TRACK_TRIG_AUTO = True  # True Auto Calculates TRIG_LEN and INTERVAL_LEN.
TRACK_TRIG_LEN = 150    # Number of pixels to end tracking
TRACK_INTERVAL_LEN = 50 # Max allowed px distance from previous
TRACK_TIMEOUT_SEC = 2.0 # If no motion for timeout seconds end tracking
TRACK_DELAY_SEC = 3.0   # seconds to delay after successful track.  Avoids duplicates
TRACK_HIST_ON = True    # Show track History overlay on last image

#======================================
# Color data for OpenCV lines and text
#======================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

#======================================
# opencv settings. (Should Not need to be changed)
#======================================
GUI_ON = False      # Display image Stream on Desktop GUI
CIRCLE_ON = True
CIRCLE_SIZE = 5
LINE_COLOR = RED
LINE_THICKNESS = 2

THRESHOLD_SENSITIVITY = 25 # black pixels below value, white above to enhance contours
BLUR_SIZE = 10    # Enlarge white area around contour pixels to aid detection

#======================================
#       webserver.py Settings
#======================================
web_server_port = 8080        # Default= 8080 Web server access port eg http://192.168.1.100:8080
web_server_root = "media"     # Default= "media" webserver root path to webserver image/video sub-folders
web_page_title = "MOTRACK Media"  # web page title that browser show (not displayed on web page)
web_page_refresh_on = True    # False=Off (never)  Refresh True=On (per seconds below)
web_page_refresh_sec = "900"  # Default= "900" seconds to wait for web page refresh  seconds (15 minutes)
web_page_blank = False        # True Starts left image with a blank page until a right menu item is selected
                              # False displays second list[1] item since first may be in progress

# Left iFrame Image Settings
# --------------------------
web_image_height = "768"       # Default= "768" px height of images to display in iframe
web_iframe_width_usage = "70%" # Left Pane - Sets % of total screen width allowed for iframe. Rest for right list
web_iframe_width = "100%"      # Desired frame width to display images. can be eg percent "80%" or px "1280"
web_iframe_height = "100%"     # Desired frame height to display images. Scroll bars if image larger (percent or px)

# Right Side Files List
# ---------------------
web_max_list_entries = 0           # 0 = All or Specify Max right side file entries to show (must be > 1)
web_list_height = web_image_height # Right List - side menu height in px (link selection)
web_list_by_datetime = True        # True=datetime False=filename
web_list_sort_descending = True    # reverse sort order (filename or datetime per web_list_by_datetime setting

# ---------- End of User Variables ------------
