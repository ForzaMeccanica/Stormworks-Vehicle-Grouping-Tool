# Hello Stormworkers!

Version: 1.0.1

This tool is here to help manage vehicle groups (the new-ish method for keeping your Stormworks vehicles organized).

## Features:
 - add, remove, and merge groups
 - rename and reorder groups
 - rename vehicles
 - assign vehicles to folders in bulk

## Features in-progress
 - Workshop vehicles are visible and can be assigned to groups, but are listed under their workshop ID
   This is because I couldn't figure out where Steam stores the vehicle names. 
   If you figure out where these are stored, please let me know in the official stormworks discord (@ForzaMeccanica)

## How To

### Startup
 - Simply run "grouping_tool.py"
 - Under normal conditions, you **do not** change the text at the bottom and click the button near the top of the window associated with the user who's vehicles you would like to organize.

### Icon Buttons
 - Rename groups and vehicles by clicking the pencil ( 🖉 ) icon.
    - The pencil icon is not visible next to workshop vehicles as they cannot be renamed.
 - Bump groups up and down the list with the arrow buttons ( ⇑ / ⇓ ).
 - Delete a group with the trash can ( 🗑 ) icon. Deleting a group will move all its contents to the "Default" folder.
 - Merge the contents of a group and the one above it by clicking the hook arrow ( ↰ ) button.
    - The group above retains its name 
 - Press the plus ( + ) above the group list to add a new group

### Action Bar
 - Select a group and press "Assign" in the action bar to assign any selected vehicles to that group.
 - Select a group and press "Filter" to only view members of that group.
 - press "Defilter" to view all.
 - press "Refresh" to refresh the editor. This will cause it to resize but will not have any other significant effects.
 - press "Read" to pull data from the files. Do this if you have changed the files since you opened this tool
 - press "Write" to publish the new group data. You need to press this button before closing to save group changes
    - Note: vehicle name change operations apply automatically and do not rely on the "write" button
