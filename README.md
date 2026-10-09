# Hello Stormworkers!

Version: 1.1

This tool is here to help manage vehicle groups (the new-ish method for keeping your Stormworks vehicles organized).

## Features:
 - add, remove, and merge groups
 - rename and reorder groups
 - rename vehicles
 - assign vehicles to groups in bulk
 - 100% local - no network, server, steam, etc.
 - decent gui

## Features in-progress
 - Workshop vehicles are visible and can be assigned to groups, but are listed under their workshop ID
   This is because I couldn't figure out where Steam stores the vehicle names. 
   If you figure out where these are stored, please let me know in the official stormworks discord (@ForzaMeccanica)
    - update: I am 100% confident they are stored locally (as I can load them in-game in a 100% offline boot), 
      but I am pulling my hair out trying to find it. If you find it, PLEASE TELL ME!

 - I intend to add a Ctrl + F feature and preview images



## How To

### Startup
 - You cannot save your groups effectively while Stormworks is running.
 - You do need to have put something in a vehicle group before starting the tool so that the parser has a target to look for. 
 - Simply run "grouping_tool.py"
 - Under normal conditions, you **do not** change the text at the bottom, just click the button near the top of the window associated with the user who's vehicles you would like to organize.
 - Select your user

### Groups
 - Select a group by clicking it or with the up/down arrow keys.
 - Rename groups by clicking the pencil ( 🖉 ) icon.
 - Bump groups up and down the list with the arrow buttons ( ⇑ / ⇓ ) or Ctrl + up/down arrows.
 - Delete a group with the trash can ( 🗑 ) icon. Deleting a group will move all its contents to the "Default" group.
 - Merge the contents of a group and the one above it by clicking the hook arrow ( ↰ ) button.
    - The group above retains its name 
 - Press the plus ( + ) above the group list to add a new group
 - "Default" group cannot be moved or modified as it is a part of the game.

### Vehicles
 - Select/Disselect vehicles by clicking them.
 - Rename vehicles by clicking the pencil ( 🖉 ) icon.
    - The pencil icon is not visible next to workshop vehicles as they cannot be renamed.
    - Renaming vehicles saves instantly. Every other action must be saved explicitly.
 - Click the "All" checkbox in the actionbar or use Ctrl + A and Ctrl + Shift + A to Select/Disselect all visible vehicles.

### Action Bar
 - Select a group and press "Assign" (Alt + A) in the action bar to assign any selected vehicles to that group.
 - Select a group and press "Filter" (Alt + F) to only view members of that group.
 - press "Defilter" (Alt + D) to view all.
 - press "Refresh" (Ctrl + R) to refresh the editor. This will cause it to resize but will not have any other significant effects.
 - press "Read" (Ctrl + Shift + R) to pull data from the files. Do this if you have changed the files since you opened this tool
 - press "Write" (Ctrl + S) to publish the new group data. You need to press this button before closing to save group changes