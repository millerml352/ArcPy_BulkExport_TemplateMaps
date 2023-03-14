# ArcPy_BulkExport_NSLICS
This script simply automates exporting of particular map formats for me using ArcGIS Pro 3.0.4 APRX project files, python 3.9.11
### Why
- Each of these maps goes through several rounds of editing and review, requiring very minute changes, meaning a new export needs to be produced (JPEG and PDF) each time an edit is needed, and then at final stage for submittal.

- While a lovely piece of software, ArcPro isn't exactly the picture of speed. Running through a Citrix instance it can take several minutes to open a project, export once to JPG, export again to PDF, then navigate to the next project and repeat. A lot of time spent looking at loading circles and pulling hair when you want to be done with the review process.

### Time Savings
- Using this script which runs fully in the background, time to export 80 APRXs into 160 map files is **26 +/- 1 minutes.**
- Traditional workflow to open each project and manually export from Pro conservative estimate of approximately 5 min/project * 80 projects = 400 min / 60 min = **6.667 hours** pretty much an entire day holy cow millerml352 what a subtle but significant savings!

### GIS Technician Brain Savings
- priceless

### Notes
2/10/23- first expanded on procedural script, run and it asks you to choose APRXs, then export directory, then automatically begins exporting and ends. created a full GUI with tkinter, reorganized to more object oriented/class structured program. GUI has buttons to choose files, select output directory, export, and determinate progress bar on bottom using counter as fraction of total files selected to determine % complete. Honestly pretty stoked about creating something like this where you can go back and forth in the options, select and change your selection before running. added error handlers to ensure it does not try to run and terminate if no files or export directory have been selected. on the verge of overkill for the current application purposes but great practice especially with creating a working interface and defining custom classes and functions as methods.

2/23/23 - disabled buttons from being able to be pressed while export thread is running because it overwrites global var. Some very minor layer issues, speed increases even more when running through citrix instance counter to my expectations. Worked well for several other technicians, only one has had issues with layers displaying in PDF format. 

3/14/23 - uploaded full gui version, abstracted output away from python shell into text element (incongruously named listbox because that was my first attempt). follow up will involve cleaning up that script now that its functional, validating map type selection (at the moment its more of a placebo), maybe trying some binding and reformatting things to be cleaner or dryer

p.s. also thinking about a more general layout exporter - load any project in, pick the layout and settings you want out. these all work based on the projects sticking to the templates they should be. if people go off piste theres room for error
