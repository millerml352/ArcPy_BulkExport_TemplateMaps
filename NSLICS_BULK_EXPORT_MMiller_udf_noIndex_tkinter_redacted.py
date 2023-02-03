# NSLICS BULK EXPORT TOOL
# ARCGIS PRO 3.0.3 2/2/2023
# MMILLER@BRISTOL-COMPANIES.COM
import arcpy, os, tkinter
import tkinter as tk
import tkinter.filedialog as fd

root = tk.Tk()


### change these lines ###
# Enter current (or desired) date for end of file in YYYYMMDD format
# change to user input
exportdate = ''

# Enter directory where .APRXs are located
folderPath = r'\\'

# File selection using Tkinter lib, output is tuple
selectedFiles = fd.askopenfilenames(parent=root, initialdir=folderPath, title='Choose your .APRXs')
#print(selectedFiles)

# Enter directory where you would like maps to be exported to
outputfolder = r'\\'

### do not change below this line unless experimenting ###

print('Wait... Tool will take about a minute to begin exporting...')
# Function to export 'CTT' or 'INSTAL 1' layout depending on .APRX filename
def export_maps(fileprefix, maptype, lyt):
    if lyt.name == maptype:
        lyt.exportToPDF(os.path.join(outputfolder, fileprefix + exportdate + '.pdf'), resolution = 150, georef_info = "False")
        print(f'PDF done: {fileprefix}{exportdate}')
        lyt.exportToJPEG(os.path.join(outputfolder, fileprefix + exportdate + '.jpg'), resolution = 150)
        print(f'JPEG done: {fileprefix}{exportdate}')
        
# Loop through selected files
for filename in selectedFiles:
    fullpath = os.path.join(folderPath, filename)
    
    # Formatting filepath and variables
    if os.path.isfile(fullpath):  
        basename, extension = os.path.splitext(fullpath)
        print(basename)
        print(extension)
        basename_split = basename.split('/')
        print(basename_split)
        fileprefix = basename_split[-1][:-8]
        print(fileprefix)
        maptype = ''
        if 'INSTAL' in fileprefix:
            maptype = 'INSTAL 1'
        elif 'CTT' in fileprefix:
            maptype = 'CTT'
        else:
            pass
            
        # Ignore anything that isn't an .aprx in directory
        if extension.lower() == ".aprx":  
            proj = arcpy.mp.ArcGISProject(fullpath)
                
            # Layout list
            listOfLayouts = proj.listLayouts()

            # List lyt.name prop
            #for lyt in proj.listLayouts():
                #print(f"  {lyt.name} ({lyt.pageHeight} x {lyt.pageWidth} {lyt.pageUnits})")
            #print(*listOfLayouts,sep=',')
            
            # Loop through list var and export
            for lyt in listOfLayouts:
                export_maps(fileprefix, maptype, lyt)
