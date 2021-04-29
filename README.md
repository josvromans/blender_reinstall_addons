# Reinstall your add-on during development, with one action within Blender

The goal of this add-on is to re-install an add-on that is in development.
After some code changes, the addon can be completely reinstalled by pressing one button or hitting Ctrl + Shift + R.

This means: make a zipfile of that directory and re-install it in Blender, without restarting Blender.
The add-on directory does not have to be linked to blender, and there is no need to add additional code in your add-on directory.

To be more specific, the following steps will be taken:

1) Disable the add-on in Blender (if there is one that matches on the directory name)
2) Remove the add-on in Blender (if there is one that matches on the directory name)
3) Make a zipfile of the add-on directory
4) Install the add-on with the zipfile
5) Unlink the zipfile
6) Reload the classes from the add-on that were registered by blender
   (determined by name startswith directory name)
7) Enable the add-on (by directory name)

You can keep track of several directories in the user preferences for this add-on. Only the ones that you select will be reinstalled.


## Instructions

- Install this add-on in Blender.
- In the add-on preferences for this add-on you can add directory paths to the project(s) you are working on.
- Make sure to select the project(s) that needs to be reinstalled
- By hitting the button in the user preferences, the selected add-on(s) will be reinstalled.
- Ctrl + Shift + R (for re-install) is the hotkey. 
  
So when this is set up, you only have to hit the hotkey, and look at the report message on the bottom of Blender 
  and keep an eye on the Python console.


## This is an experiment
There are many ways to achieve a similar result. 
The most popular is to add extra code in your project, for development purposes only, that checks if modules have to be reloaded.
When your project is linked with Blender, add-on changes can be picked up automatically.
That might be the first solution you could try.

The disadvantages of that solution are.
- the additional code has to be removed every time you share the add-on, and added everytime you work on another add-on.
- there is no proper feedback on the actual reloading / reinstall action. 
  
I don't might to hit one action purposely to launch a re-installation (and watch the feedback). 
Furthermore, I like a real re-install from time to time, by installing the add-on with a zipfile, exactly as another user would. 
(suggestions are welcome to mimic this approach as best as possible without restarting Blender..).
I might explore a 'softer' approach later (only reloading / deleting modules in Python, and not installing a zip file everytime)

Some discussion on this topic: https://developer.blender.org/T67387


## Known bugs / issues
- This add-on does not work with single file add-ons, only with directories. (non bug)
- Unregister for this add-on 'reinstall_addons' can give an error in some cases. 
  (only after some loading / unloading of other add-ons was done..)
  
## General troubleshooting
Remove the add-on in the user preferences and restart Blender.
