# NSLICS BULK EXPORT TOOL
# ARCGIS PRO 3.0.x PYTHON 3.9.x
# MMILLER@BRISTOL-COMPANIES.COM

import arcpy, os, threading
from tkinter import *
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from datetime import datetime

# Project Files (.APRXs) default directory
folderPath = r'\\bi-az-gis\GIS\GIS\IRM Omaha P2 G1-G2'
# Map Exports default directory
outputfolder = r'\\bi-az-gis\GIS\GIS\IRM Omaha P2 G1-G2'
# Initial globals
selectedFiles=[]
outputLocation=''
running = False

'''
PRINT BLOCK BECAUSE TEXT WIDGET
listbox['state'] = NORMAL
listbox.insert("end",'\n')
listbox.insert('end','Working on: ' + fileprefix)
listbox['state'] = DISABLED
listbox.see('end')
'''

class userInterface:

    def __init__(self):
        root = Tk()
        root.title('ArcPro Export Tool')
        root.minsize(800, 490)
        root.maxsize(800, 490)  # constrain window size, does not resize automatically
        root.config(bg='palegreen2')  # specify background color

        # Create frames
        buttonFrame = Frame(root, bg='grey')
        buttonFrame.grid(row=0, column=0, padx=5, pady=9)
        
        layoutFrame = Frame(root, bg='grey')
        layoutFrame.grid(row=0, column=1, padx=0, pady=9)

        # Create labels
        Label(buttonFrame, text='Map Export Tool').grid(row=0, column=0, padx=5, pady=5)
        Label(buttonFrame, text='Progress Bar').grid(row=6, column=0, padx=5, pady=5)
        
        # Create inner frames
        toolBar = Frame(buttonFrame, width=380, height=400)
        toolBar.grid(row=3, column=0, padx=10, pady=2)

        # Dropdown menu options
        options = [
            "NSLICS",
            "SG",
            "CAS",
            "MILFACs"
            ]
        # datatype of menu text
        clicked = StringVar()
  
        # initial menu text
        clicked.set( "Select Map Type" )
        
        dropDown = OptionMenu(buttonFrame, clicked, *options)
        dropDown.grid(row=2, column=0, pady=5)
        
        optionArea = Frame(toolBar, width=500, height=100)
        optionArea.grid(row=5, column=0, padx=10, pady=5)
        
        progressBar = ttk.Progressbar(buttonFrame, orient="horizontal",
                                      mode="determinate", maximum=100,
                                      value=0, length=235)
        progressBar.grid(row=7, column=0, padx=15, pady=5)
        
        # Project Listbox
        listbox = Text(layoutFrame,
                       state=DISABLED,
                       wrap=WORD,
                          font = ("Courier", 10),
                          width=62,
                          height=28,
                          bg = "white",
                          fg = "black")
        listbox.grid(row=5, column=0, padx=10, pady=10)
        listbox['state'] = NORMAL
        listbox.insert('end','Select map type, project files, export directory, and export options to begin...')
        listbox['state'] = DISABLED
        def selectProjects():
            # File selection using Tkinter lib, output is tuple
            global selectedFiles, folderPath
            selectedFiles = fd.askopenfilenames(parent=root, initialdir=folderPath, title='Select .APRXs')

            if selectedFiles:
                listbox['state'] = NORMAL
                listbox.insert("end",'\n')
                listbox.insert("end", 'Files Selected:')
                for i in selectedFiles:
                    if os.path.isfile(i):
                        basename, extension = os.path.splitext(i)
                        basename_split = basename.replace('/','\\').split('\\')
                        fileprefix = basename_split[-1]
                        listbox.insert("end",'\n')
                        listbox.insert("end", fileprefix)
                listbox['state'] = DISABLED
                listbox.see('end')
            
            # remember location of last selected .aprx's
            if selectedFiles:
                dirNum = selectedFiles[0].count('/')
                pathsplit = selectedFiles[0].split('/')
                folderPath = '/'.join(pathsplit[:dirNum])
            else:
                # if no selection reset to initial directory, bugs when going back and forth bt buttons
                folderPath = r'\\bi-az-gis\GIS\GIS\IRM Omaha P2 G1-G2'
            
        def selectExportDirectory():
            # Select output file location
            global outputLocation, outputfolder
            outputLocation = fd.askdirectory(parent=root, initialdir=outputfolder, title='Select Export Location')
            # remember last selected folder
            if outputLocation:
                listbox['state'] = NORMAL
                listbox.insert("end",'\n')
                listbox.insert("end", 'Export Directory:')
                listbox.insert("end",'\n')
                listbox.insert("end", outputLocation)
                outputfolder = outputLocation
                listbox['state'] = DISABLED
                listbox.see('end')
            else:
                # if no selection reset to initial directory, bugs when going back and forth bt buttons
                outputfolder = r'\\bi-az-gis\GIS\GIS\IRM Omaha P2 G1-G2'          
                    
        def exportMaps():
            # Reset iterable vars and get start time
            # Also get checkbox states and create function local assignment
            global running
            
            pdf_val = var2.get()
            jpg_val = var1.get()
            progTracker = 0
            progComplete = 0
            mapcount = 0
            exportType = str(clicked.get())
            output_georef = int(georef.get())
            output_dpi = int(dpiSelect.get())
            startTime=datetime.now()
            listbox['state'] = NORMAL
            listbox.insert("end",'\n')
            listbox.insert('end','--------------------------')
            listbox.see('end')
            
            # No export options check
            if pdf_val == 0 and jpg_val == 0:
                listbox.insert("end",'\n')
                listbox.insert('end','Check boxes to indicate which file formats you would like exported: JPEG and/or PDF.')
                listbox.see('end')
                return
            # No-file-selected check
            if not selectedFiles:
                listbox.insert("end",'\n')
                listbox.insert('end',"No files selected. Please select at least one .APRX file to export.")
                listbox.see('end')
                return
            # No Export location check
            if not outputLocation:
                listbox.insert("end",'\n')
                listbox.insert('end',"No export location selected. Please choose a folder.")
                listbox.see('end')
                return
            # Valid DPI Check
            if output_dpi < 50:
                listbox.insert("end",'\n')
                listbox.insert('end','Please choose a valid DPI value: between 50 and 1000.')
                listbox.see('end')
                return
            elif output_dpi > 1000:
                listbox.insert("end",'\n')
                listbox.insert('end','Please choose a valid DPI value: between 50 and 1000.')
                listbox.see('end')
                return
            else:
                pass
            listbox['state'] = DISABLED
            listbox.see('end')
            
            # Disable buttons while thread running to prevent user error ;)
            b1['state'] = DISABLED
            b2['state'] = DISABLED
            b3['state'] = DISABLED
            c1['state'] = DISABLED
            c2['state'] = DISABLED
            georefSelect['state'] = DISABLED
            dpiSelect['state'] = DISABLED

            # Overwrite export button with interrupt button and set function state
            running = True
            global b4
            b4 = Button(toolBar, text='STOP EXPORT', fg='red', command=exportInterrupt, state=NORMAL, relief=RAISED, width=32, height=4)
            b4.grid(row=2, padx=5, pady=10)

            # Loop through selected files
            for filename in selectedFiles:
                progComplete = len(selectedFiles)

                # If allows interrupting loop
                if running == True:
                
                    # Check valid then formatting filepath and variables
                    if os.path.isfile(filename):  
                        basename, extension = os.path.splitext(filename)
                        basename_split = basename.replace('/','\\').split('\\')
                        fileprefix = basename_split[-1]
                        maptype = ''
                    
                        # Ignore anything that isn't an .aprx in directory
                        if extension.lower() == ".aprx":
                            listbox['state'] = NORMAL
                            listbox.insert("end",'\n')
                            listbox.insert('end','Working on: ' + fileprefix)
                            listbox['state'] = DISABLED
                            proj = arcpy.mp.ArcGISProject(filename)
                        
                            # Layout list
                            listbox['state'] = NORMAL
                            listbox.insert("end",'\n')
                            listbox.insert('end','Opening project layout...')
                            listbox['state'] = DISABLED
                            listOfLayouts = proj.listLayouts()
                            listbox['state'] = NORMAL
                            listbox.insert('end','Beginning export...')
                            listbox['state'] = DISABLED
                            listbox.see('end')

                            # Validate Map Type
                            if 'MilitaryFacilities' in fileprefix:
                                maptype = 'Layout'
                            elif 'INSTAL' in fileprefix:
                                maptype = 'INSTAL 1'
                            elif 'CTT' in fileprefix:
                                maptype = 'CTT'
                            elif 'Cover' in fileprefix:
                                maptype = 'Layout 1'
                            elif 'Inside' in fileprefix:
                                maptype = 'Layout 2'
                            elif 'CASMap' in fileprefix:
                                maptype = 'Layout'
                            else:
                                listbox['state'] = NORMAL
                                listbox.insert("end",'\n')
                                listbox.insert('end','Invalid file type, skipping: ' + fileprefix + extension)
                                listbox.insert("end",'\n')
                                listbox.insert('end','--------------------------')
                                listbox['state'] = DISABLED
                                pass
                        
                            # Loop through list var and export
                            for lyt in listOfLayouts:
                                if lyt.name == maptype and running == True:
                                
                                    # Export
                                    if pdf_val == 1 and running == True:
                                        lyt.exportToPDF(os.path.join(outputLocation, fileprefix + '.pdf'), resolution=output_dpi, georef_info=output_georef)
                                        listbox['state'] = NORMAL
                                        listbox.insert("end",'\n')
                                        listbox.insert('end',f'PDF done: {fileprefix}')
                                        listbox['state'] = DISABLED
                                        listbox.see('end')
                                        mapcount += 1
                                    if jpg_val == 1 and running == True:
                                        lyt.exportToJPEG(os.path.join(outputLocation, fileprefix + '.jpg'), resolution=output_dpi)
                                        listbox['state'] = NORMAL
                                        listbox.insert("end",'\n')
                                        listbox.insert('end',f'JPEG done: {fileprefix}')
                                        listbox['state'] = DISABLED
                                        mapcount += 1
                                        listbox.see('end')
    
                                    # Update progress bar each run
                                    progTracker += 1
                                    progFraction = (progTracker / progComplete) * 100
                                    progressBar['value'] = progFraction
                                    listbox['state'] = NORMAL
                                    listbox.insert("end",'\n')
                                    listbox.insert('end','--------------------------')
                                    listbox['state'] = DISABLED
                                    listbox.see('end')
                        else:
                            # Add to progTracker for non-APRXs to increase progressbar still
                            progTracker += 1
                            progFraction = (progTracker / progComplete) * 100
                            progressBar['value'] = progFraction
                            pass
                # Continue to allow final stats and variable reset after export is interrupted
                else:
                    continue
                
            # Time delta calc and format
            endTime = datetime.now()
            runtime = endTime - startTime
            runtimeS = round(runtime.total_seconds()%60, 0)
            runtimeM = round(runtime.total_seconds()/60, 2)
            
            # Reset progress to 0 and re-enable buttons/checkboxes
            progressBar['value'] = 0
            b4 = Button(toolBar, text='EXPORT', command=run_exportMaps, state=NORMAL, relief=RAISED, width=32, height=4)
            b4.grid(row=2, padx=5, pady=10)
            b1['state'] = NORMAL
            b2['state'] = NORMAL
            b3['state'] = NORMAL
            c1['state'] = NORMAL
            c2['state'] = NORMAL
            #georefSelect['state'] = NORMAL
            dpiSelect['state'] = NORMAL
            listbox['state'] = NORMAL
            listbox.insert("end",'\n')
            listbox.see('end')
            
            # Final runtime stats and no APRX check
            if mapcount == 0:
                listbox.insert('end','No valid .APRX files selected.')
                running = False
            elif running == False and runtime.total_seconds() > 60:
                listbox.insert('end',f'Export process interrupted. {mapcount} maps exported. \nTime elapsed: {runtimeM} minutes.')
                running = False
            elif running == False and runtime.total_seconds() < 60:
                listbox.insert('end',f'Export process interrupted. {mapcount} maps exported. \nTime elapsed: {runtimeS} seconds.')
                running = False
            elif runtime.total_seconds() < 60:
                listbox.insert('end',f'Export complete: {mapcount} maps total.\nTime elapsed: {runtimeS} seconds.')
                running = False
            elif runtime.total_seconds() > 60:
                listbox.insert('end',f'Export complete: {mapcount} maps total.\nTime elapsed: {runtimeM} minutes.')
                running = False
            else:
                listbox.insert('end','Error, check maps for quality.')
                running = False
            listbox['state'] = DISABLED
            listbox.see('end')
                
        # Interrupt export midway
        def exportInterrupt():
            global running
            running = False
            listbox['state'] = NORMAL
            listbox.insert("end",'\n')
            listbox.insert('end','INTERRUPTING EXPORT AFTER NEXT ITERATION...')
            listbox.see('end')
            b4['state'] = DISABLED
            listbox['state'] = DISABLED
    
        # Run export in new thread so that GUI can be moved still
        def run_exportMaps():
            export_thread = threading.Thread(target=exportMaps)
            export_thread.start()

        # Validate DPI Entry
        def validateInput(entry):
            if entry.isdigit() and int(entry) < 1001 and int(entry) > 49:
                #print(entry)
                return True
                          
            elif entry == "":
                #print(entry)
                return True
  
            else:
                #print(entry)
                return False
            
        # Buttons
        # Main Frame
        b1 = Button(toolBar, text="Select .APRX files", command=selectProjects, state=NORMAL, relief=RAISED, width=32, height=4)
        b1.grid(row=0, padx=5, pady=10)  # ipadx is padding inside the Label widget
        b2 = Button(toolBar, text="Select map output directory", command=selectExportDirectory, state=NORMAL, relief=RAISED, width=32, height=4)
        b2.grid(row=1, padx=5, pady=10)
        b3 = Button(toolBar, text='EXPORT', command=run_exportMaps, state=NORMAL, relief=RAISED, width=32, height=4)
        b3.grid(row=2, padx=5, pady=10)
        
        # Quality Options - define and default to selected
        # JPEG Export
        var1 = IntVar()
        c1 = Checkbutton(optionArea, text="JPEG", variable=var1, onvalue=1, offvalue=0, state=NORMAL)
        c1.grid(row=3, column=1)
        c1.select()
        # PDF Export
        var2 = IntVar()
        c2 = Checkbutton(optionArea, text="PDF", variable=var2, onvalue=1, offvalue=0, state=NORMAL)
        c2.grid(row=3, column=2)
        c2.select()
        # Georeference PDF
        georef = BooleanVar()
        georefSelect = Checkbutton(optionArea, text="GeoReferenced PDF", variable=georef, onvalue=True, offvalue=False, state=DISABLED)
        georefSelect.grid(row=4, column=2)
        georefSelect.select()
        # Select DPI for exports
        reg = root.register(validateInput)
        dpiLabel = Label(optionArea, text="DPI:")
        dpiLabel.grid(row=4, column=0)
        dpi = IntVar()
        dpi.set(350)
        dpiSelect = Spinbox(optionArea, from_=50, to=1000, width=5, justify=RIGHT, textvariable=dpi, state=NORMAL, validate='focus', validatecommand=(reg, '%P'))
        dpiSelect.grid(row=4, column=1)
        
        root.mainloop()

userInterface()
