import tkinter as tk
import time as tm
import datetime
import os
import glob
import inspect
import pandas as pd

# SETTINGS
#=======================================================================================================================================
my_resolution = 0  #auto-detects if 0
fullscreen_boolean = False

# Gets the canonical path, eliminating any symbolic links
module_path = inspect.getfile(inspect.currentframe())

# Builds working directory using canonical path
module_dir = os.path.realpath(os.path.dirname(module_path))

# Folder containing .csv files
path = module_dir + "/bucha_logs"
file_prefix = 'bucha_log'

# Padding character
padding_char = '_'

# Create a list populated with temperature values
#tempList = []   #TODO: replace list with dictionary using date/time as the keys

# FUNCTIONS
#=======================================================================================================================================


# Function to retrieve the last line from most recent file
def get_last_line():
    file_list = glob.glob(path + '/' + file_prefix + '*.csv')
    file_list.sort()
    datafile = file_list[-1] #most recent data file
    
    with open(datafile, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = (f.readline().decode())
        return(last_line)

# Function to determine minimum and maximum temperature values in file
def get_min_max_temp():
    file_list = glob.glob(path + '/' + file_prefix + '*.csv')
    file_list.sort()
    datafile = file_list[-1] # most recent data file
    datafile2 = file_list[-2] # second most recent data file

    df = pd.read_csv(datafile) # populates dataframe
    df2 = pd.read_csv(datafile2)

    min_temp1 = df[' temperature'].min()
    max_temp1 = df[' temperature'].max()

    min_temp2 = df2[' temperature'].min()
    max_temp2 = df2[' temperature'].max()


# Function to update background color variable based on air quality index
def update_bg_color(PM_type):
            
    aqi_color = 'black'

    return(aqi_color)


def update_my_window_label():
    my_window['bg'] = update_bg_color('0')
    
    my_window.after(5000, update_my_window_label)


def update_title_label():
    title_label['bg'] = update_bg_color('0')
    
    title_label.after(5000, update_title_label)



# TEMPERATURE 
#======================================================================================================================================
def update_temp_title_label():
    temp_title_label['bg'] = update_bg_color('0')
    
    temp_title_label.after(5000, update_temp_title_label)

def update_temp_data_label():
    raw_data_line = get_last_line().rstrip()
    temperature = raw_data_line.split(',')[1]
    temp_data_label['text'] = "{:6.1f}".format(float(temperature))

    temp_data_label['bg'] = update_bg_color('0')
    
    temp_data_label.after(5000, update_temp_data_label)

def update_temp_unit_label():
    temp_unit_label['bg'] = update_bg_color('0')
    
    temp_unit_label.after(5000, update_temp_unit_label)

def update_min_temp_title_label():
    min_temp_title_label['bg'] = update_bg_color('0')
    
    min_temp_title_label.after(5000, update_min_temp_title_label)

def update_min_temp_data_label():
    raw_data_line = get_last_line().rstrip()
    temperature = raw_data_line.split(',')[2]

    temperature = float(temperature)
    #tempList.append(temperature)

    # TODO: remove temperature values older than 24 hours
    # while date of first measurement > 24 hours + current time
    #     if date of first measurement > 24 hours + current time
    #         delete first measurement      

    # while len(tempList) > 1439: #TEMPORARY WORKAROUND, ONLY WORKS IF PROGRAM RUNS FOR 24+ HOURS CONTINUOUSLY
    #     del tempList[0]

    min_temp_data_label['bg'] = update_bg_color('0')

    min_temp_data_label['text'] = "{:6.1f}".format(temperature)

    min_temp_data_label.after(5000, update_min_temp_data_label)


def update_min_temp_unit_label():
    min_temp_unit_label['bg'] = update_bg_color('0')
    
    min_temp_unit_label.after(5000, update_min_temp_unit_label)


# TIME 
#=====================================================================================================================


# Function to update clock_label widget with system clock reading
def display_time():
    current_time = tm.strftime('%I:%M:%S %p')
    clock_label['text'] = current_time
    clock_label.after(200, display_time)

def update_clock_label():
    clock_label['bg'] = update_bg_color('0')
    
    clock_label.after(5000, update_clock_label)

# Function to update time_last_measurement widget
# based on dt value from latest recording
def update_time_last_measurement_data_label():
    #current_time = tm.strftime('%I:%M:%S %p')
    raw_data_line = get_last_line().rstrip()
    dt_latest = raw_data_line.split(',')[0]
    dt_latest_obj = datetime.datetime.strptime(dt_latest, "%Y-%m-%d %H:%M:%S.%f")
    time_last_measurement = dt_latest_obj.strftime("%I:%M:%S %p")
    time_last_measurement_data_label['text'] = time_last_measurement

    time_last_measurement_data_label['bg'] = update_bg_color('0')

    time_last_measurement_data_label.after(5000, update_time_last_measurement_data_label)

def update_time_last_measurement_label():
    time_last_measurement_label['bg'] = update_bg_color('0')
    
    time_last_measurement_label.after(5000, update_time_last_measurement_label)





# MAIN FUNCTION
#======================================================================================================================================

# Create the main window and set its attributes
my_window = tk.Tk()
my_window.title('RaspBucha Monitor')
my_window['bg']=update_bg_color('0') 

# Checks if display resolution has been set manually
if my_resolution == 0:
    # Gets resolution of display and sets it automatically
    screen_width = my_window.winfo_screenwidth()
    screen_height = my_window.winfo_screenheight()
    monitor_resolution = str(screen_width) + 'x' + str(screen_height)
else:
    monitor_resolution = my_resolution


my_window.geometry(monitor_resolution)
#my_window.overrideredirect(True)
my_window.wm_attributes('-fullscreen',fullscreen_boolean)
#my_window.wm_attributes('-topmost','true')

# Create the title_label widget
title_label = tk.Label(my_window, text='Kombucha Monitor', font='ariel 70', fg='white')
title_label.grid(row=0, column=0, columnspan=2)
update_title_label()

# Create the clock_label widget
clock_label = tk.Label(my_window, font='ariel 25', fg='gray')
clock_label.grid(row=100, column=0, columnspan=1)
display_time()
update_clock_label()


# Create the temp_title_label widget
temp_title_label = tk.Label(my_window, text='Temperature'.ljust(23,padding_char), font='courier 45', fg='gray')
temp_title_label.grid(row=3, column=0, sticky='W')
update_temp_title_label()

# Create the temp_data_label widget
temp_data_label = tk.Label(my_window, font='courier 45 bold', fg='gray')
temp_data_label.grid(row=3, column=1)
update_temp_data_label()

# Create the temp_unit_label widget
degree_sign = u'\N{DEGREE SIGN}' #unicode
temp_unit_label = tk.Label(my_window, text=degree_sign+'C', font='courier 45', fg='gray')
temp_unit_label.grid(row=3, column=2, sticky='W')
update_temp_unit_label()


# Create min_temp_title_label widget
min_temp_title_label = tk.Label(my_window, text='Max. Temperature'.ljust(23,padding_char), font='courier 45', fg='gray')
min_temp_title_label.grid(row=4, column=0, sticky='W')
update_min_temp_title_label()

# Creates min_temp_data_label widget
min_temp_data_label = tk.Label(my_window, font='courier 45 bold', fg='gray')
min_temp_data_label.grid(row=4, column=1)
update_min_temp_data_label()

# Create min_temp_unit_label widget
degree_sign = u'\N{DEGREE SIGN}' #unicode
min_temp_unit_label = tk.Label(my_window, text=degree_sign+'C', font='courier 45', fg='gray')
min_temp_unit_label.grid(row=4, column=2, sticky='W')
update_min_temp_unit_label()


# Create time_last_measurement_label widget
time_last_measurement_label = tk.Label(my_window, text = 'updated:', font = 'courier 25', fg='gray')
time_last_measurement_label.grid(row=100, column=1)
update_time_last_measurement_label()

# Create time_last_measurement_data_label widget
time_last_measurement_data_label = tk.Label(my_window, font = 'ariel 25', fg ='gray')
time_last_measurement_data_label.grid(row=100, column=2, columnspan=2)
update_time_last_measurement_data_label()



# Initiate the window's main loop that waits for user's actions
my_window.mainloop()
