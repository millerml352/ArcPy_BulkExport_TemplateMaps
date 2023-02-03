# ArcPy_BulkExport_NSLICS
NSLICS maps are made for use by U.S.A.C.E. MVS as part of contract work, sensitive info redacted. This script simply automates exporting of maps from ArcGIS Pro 3.0.3 APRX project files.
### Why
- Each of these maps goes through several rounds of editing and review, requiring very minute changes, meaning a new export needs to be produced (JPEG and PDF) each time an edit is needed, and then at final stage for submittal.

- While a lovely piece of software, ArcPro isn't exactly the picture of speed. Running through a Citrix instance it can take several minutes to open a project, export once to JPG, export again to PDF, then navigate to the next project and repeat. A lot of time spent looking at loading circles and pulling hair when you want to be done with the review process.

### Time Savings
- Using this script which runs fully in the background, time to export 40 APRXs into 80 maps is **15 +/- 1 minutes.**
- Traditional workflow to open each project and manually export from Pro conservative estimate of approximately 5 min/project * 40 projects = 200 min / 60 min = **3.333 hours**

### GIS Technician Brain Savings
- priceless

### To-do list
Want to make things even simpler so no code editing required on part of technician making maps
- add simple file explorer gui to select which files export is desired for; bonus of being able to only export subset if full export is not needed
