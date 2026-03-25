import os
import time
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk
from enum import Enum, auto

class Status(Enum):
    SUCCESS = 0
    IP_ERROR = 1
    FAILED_PING = 2


#####
# Open the UI
#####
def prompt_user():
    root = Tk()
    root.title("Device Information")

    mainframe = ttk.Frame(root, padding=(3,3,12,12))        # Create the parent, "mainframe"
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))    # Create the grid

    # Create the Username input
    User = StringVar()
    User_entry = ttk.Entry(mainframe, width=20, textvariable=User)
    User_entry.insert(0, "bvassallo")
    User_entry.grid(column=2, row=1, sticky=W)

    # Create the IP Address input
    IP_addr = StringVar()
    IP_entry = ttk.Entry(mainframe, width=14, textvariable=IP_addr)
    IP_entry.grid(column=2, row=2, sticky=W)

    # Create the File Path input
    file_path = StringVar()
    FP_entry = ttk.Entry(mainframe, width=40, textvariable=file_path)
    FP_entry.grid(column=2, row=4, sticky=(W, E))

    # Create the Destination Path input
    dest_path = StringVar()
    DEST_entry = ttk.Entry(mainframe, width=40, textvariable=dest_path)
    DEST_entry.grid(column=2, row=5, sticky=(W, E))

    # Create the text labels
    ttk.Label(mainframe, text="Username for Device: ").grid(column=1, row=1, sticky=E)
    ttk.Label(mainframe, text="IP Address of Device: ").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="File Path: ").grid(column=1, row=4, sticky=E)
    ttk.Label(mainframe, text="Destination Path: ").grid(column=1, row=5, sticky=E)

    ping_status = ttk.Label(mainframe, text="Waiting to Ping...")
    ping_status.grid(column=4, row=2, sticky=E)

    # Create the ping button
    ttk.Button(mainframe, text="Ping", command=lambda: ping_IP(IP_addr, ping_status)).grid(column=3, row=2, sticky=W)

    # Create the Destination Path Auto Fill buttons
    ttk.Button(mainframe, text="Update Plugins", command=lambda: update_autofill(DEST_entry)).grid(column=3, row=5, sticky=W)
    ttk.Button(mainframe, text="~/Desktop", command=lambda: desktop_autofill(DEST_entry)).grid(column=4, row=5, sticky=W)

    # Create the run SCP button
    ttk.Button(mainframe, text="Initalize SCP", command=lambda: run_scp(User, IP_addr, file_path, dest_path)).grid(column=2, row=6, sticky=W)

    root.columnconfigure(0, weight=1)           # Fill in any extra space if resized
    root.rowconfigure(0, weight=1)	

    mainframe.columnconfigure(2, weight=1)      # Add some padding to reduce scrunch
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    IP_entry.focus()                            # When opened, focus on IP_entry, the first field

    root.mainloop()

#####
# Ping the requested IP
#####
def ping_IP(ip_addr: tk.StringVar, ping_status: ttk.Label):
    ip_addr_str = ip_addr.get()
    IP_status = check_IP(ip_addr_str)   # Check IP Valididy

    if IP_status == Status.IP_ERROR:    # If the IP doesn't exists, don't ping
        ping_status.config(text="IP Address incorrect format", foreground="orange")
        return

    # Actually ping the device
    ping_status.config(foreground="blue")
    ping_status.update_idletasks()      # Force the ping_status label to update
    result = subprocess.run(["ping", "-n", "1", ip_addr_str], capture_output=True)

    # Did it work?
    if result.returncode == 0:
        ping_status.config(text=f"Ping to [{ip_addr_str}] was successful", foreground="green")

    else:
        ping_status.config(text=f"Ping to [{ip_addr_str}] FAILED", foreground="red")      



#####
# Check if the IP is the correct format
#####
def check_IP(ip_addr):
    ip_array = ip_addr.split(".")   # Split the provided IP Address

    if len(ip_array) != 4:           # Check if there are 4 values
        return Status.IP_ERROR
    
    for ip_seg in ip_array:         # Check that the 4 values are within range
        try:
            temp = int(ip_seg)
            if temp < 0 or temp > 255:
                return Status.IP_ERROR
            
        except ValueError:          # Check that the 4 values are actual numbers
            return Status.IP_ERROR

    return Status.SUCCESS


def update_autofill(DEST_entry: ttk.Entry):
    DEST_entry.delete(0, tk.END)
    DEST_entry.insert(0, "~/minecraft/server/plugins/update")   # Autofill the plugins path

def desktop_autofill(DEST_entry: ttk.Entry):
    DEST_entry.delete(0, tk.END)
    DEST_entry.insert(0, "~/Desktop")   # Autofill the Desktop Path

def run_scp(SV_username: tk.StringVar, SV_ip_addr: tk.StringVar, SV_file_path: tk.StringVar, SV_dest_path: tk.StringVar):
    usename = SV_username.get()     # Get each field for string use
    IP_address = SV_ip_addr.get()
    file_path = SV_file_path.get()

    # Remove any quotes when copying over a filepath
    if file_path[0] == "\"":
        file_path = file_path[1:]
    if file_path[-1] == "\"":
        file_path = file_path[:-1]

    dest_path = SV_dest_path.get()

    command = f"scp {file_path} {usename}@{IP_address}:{dest_path}" # Run the SCP command in the shell
    subprocess.run(command, shell=True)



def main():
    prompt_user()
    pass

main()