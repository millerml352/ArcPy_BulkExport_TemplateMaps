# SG Map APRX Export Tool
# ARCGIS PRO 3.0.3 2/23/2023
# MMILLER@BRISTOL-COMPANIES.COM

import arcpy, os, threading
from tkinter import *
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from datetime import datetime

# Project Files (.APRXs) default dir
folderPath = r'\\bi-az-gis\GIS\GIS'
# Map Exports default dir
outputfolder = r'\\bi-az-gis\GIS\GIS'
# Globals
selectedFiles=[]
outputLocation=''

class userInterface:

    def __init__(self):
        root = Tk()  # create root window
        root.title('SG Map Export Tool')  # title of the GUI window
        root.minsize(295, 410)
        root.maxsize(295, 410)  # constrain window size, does not resize automatically
        root.config(bg='skyblue')  # specify background color

        # Create frames
        buttonFrame = Frame(root, width=400, height=600, bg='grey')
        buttonFrame.grid(row=0, column=0, padx=5, pady=0)
        progressFrame = Frame(root, width=400, height= 100, bg='grey')
        progressFrame.grid(row=1, column=0, padx=5, pady=5)

        # Create frames and labels
        Label(buttonFrame, text='SG Map Export Tool').grid(row=0, column=0, padx=5, pady=5)
        Label(progressFrame, text='Progress Bar').grid(row=0, column=0, padx=5, pady=5)
        
        
        # Create inner frames
        toolBar = Frame(buttonFrame, width=380, height=300)
        toolBar.grid(row=3, column=0, padx=10, pady=10)
        progressBar = ttk.Progressbar(progressFrame, orient="horizontal", mode="determinate", maximum=100, value=0, length=235)
        progressBar.grid(row=1, column = 0, padx=20, pady=10)

        def selectProjects():
            # File selection using Tkinter lib, output is tuple
            global selectedFiles
            selectedFiles = fd.askopenfilenames(parent=root, initialdir=folderPath, title='Select .APRXs')
            if selectedFiles:
                print('Files: ',*selectedFiles, sep='\n')
        
        def selectExportDirectory():
            # Select output file location
            global outputLocation
            outputLocation = fd.askdirectory(parent=root, initialdir=outputfolder, title='Select Export Location')
            if outputLocation:
                print('Directory: \n' + outputLocation)
        
        def exportMaps():
            # Reset iter vars and get start time
            progTracker = 0
            progComplete = 0
            mapcount = 0
            startTime=datetime.now()
            print('--------------------------')
            # No-file-selected check
            if not selectedFiles:
                print("No files selected. Please select at least one .aprx file to export.")
                return
            if not outputLocation:
                print("No export location selected. Please choose a folder.")
                return
            # Disable buttons while thread running to prevent user error ;)
            b1['state'] = DISABLED
            b2['state'] = DISABLED
            b3['state'] = DISABLED
            # Loop through selected files
            for filename in selectedFiles:
                progComplete = len(selectedFiles)
                #fullpath = os.path.join(folderPath, filename)
                #print(fullpath)
                # Check valid then formatting filepath and variables
                if os.path.isfile(filename):  
                    basename, extension = os.path.splitext(filename)
                    basename_split = basename.replace('/','\\').split('\\')
                    fileprefix = basename_split[-1]
                    maptype = ''
                    if 'Cover' in fileprefix:
                        maptype = 'Layout 1'
                    elif 'Inside' in fileprefix:
                        maptype = 'Layout 2'
                    else:
                        pass
                    # Ignore anything that isn't an .aprx in directory
                    if extension.lower() == ".aprx":
                        print('Working on: ' + fileprefix)
                        proj = arcpy.mp.ArcGISProject(filename)
                        # Layout list
                        print('Opening project layout...')
                        listOfLayouts = proj.listLayouts()
                        print('Beginning export...')
                        # Loop through list var and export
                        for lyt in listOfLayouts:
                            if lyt.name == maptype:
                                # Export
                                lyt.exportToPDF(os.path.join(outputLocation, fileprefix + '.pdf'), resolution = 150, georef_info = "False")
                                print(f'PDF done: {fileprefix}')
                                mapcount += 1
                                lyt.exportToJPEG(os.path.join(outputLocation, fileprefix + '.jpg'), resolution = 150)
                                print(f'JPEG done: {fileprefix}')
                                mapcount += 1
                                # Update progress bar each run
                                progTracker += 1
                                progFraction = (progTracker / progComplete) * 100
                                progressBar['value'] = progFraction
                                print('--------------------------')
            # Final runtime stats and no APRX check
            endTime = datetime.now()
            runtimeS = endTime - startTime
            runtimeM = round(runtimeS.total_seconds()/60, 2)
            if mapcount == 0:
                print('No valid .APRX files selected.')
            elif runtimeS.total_seconds() < 60:
                print(f'Export complete: {mapcount} maps total.\nTime elapsed: {runtimeS} seconds.')
            elif runtimeS.total_seconds() > 60:
                print(f'Export complete: {mapcount} maps total.\nTime elapsed: {runtimeM} minutes.')
            else:
                print('Error, check maps for quality.')
            # Reset progress to 0 and re-enable buttons for new batch
            progressBar['value'] = 0
            b1['state'] = NORMAL
            b2['state'] = NORMAL
            b3['state'] = NORMAL
      
        
        # Run export in new thread so that GUI can be moved still
        def run_exportMaps():
            export_thread = threading.Thread(target=exportMaps)
            export_thread.start()
        
        # Buttons
        b1 = Button(toolBar, text="Select .APRX files", command=selectProjects, state=NORMAL, relief=RAISED, width=32, height=4)
        b1.grid(row=0, column=0, padx=5, pady=10, ipadx=10)  # ipadx is padding inside the Label widget
        b2 = Button(toolBar, text="Select map output directory", command=selectExportDirectory, state=NORMAL, relief=RAISED, width=32, height=4)
        b2.grid(row=1, column=0, padx=5, pady=10, ipadx=10)
        b3 = Button(toolBar, text='EXPORT', command=run_exportMaps, state=NORMAL, relief=RAISED, width=32, height=4)
        b3.grid(row=2, column=0, padx=5, pady=10, ipadx=10)
        
        root.mainloop()

userInterface()
