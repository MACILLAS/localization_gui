# GUI for Localization Server

Displays several localized patches for each region of interest (ROI)
from the localization server. 

## Architecture

This program has two components...

1. Flask Server
   1. Receives API call from localization server (idx, Q, R, q, r)
   2. Stores and Serves localization results to PYQT5 GUI
2. PYQT5 GUI
   1. Communicates with Flask server
   2. Retrieve and display localization results

## Using the GUI
1. Run app.py (Flask Server)
   1. Change the host as required.
   2. Ensure localization server can reach the app route host/visualize
   3. See sendquery.py for sample request
2. Run gui.py (PYQT5 GUI)
   1. Make sure to enter the correct host of the Flask server.
   2. Select the number of ROI windows to open.
   3. Press 'LAUNCH'. Please note that you will not be able to press
   launch again without first pressing 'RESET', which will close all windows