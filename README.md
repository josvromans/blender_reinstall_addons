# Reinstall your add-on during development, with one action within Blender

The goal of this add-on is to re-install an add-on that is in development.
After some code changes, the addon can be completely reinstalled by pressing one button or hitting one keypress.

This means: make a zipfile of that directory and re-install it in Blender, without restarting Blender.
The add-on directory does not have to be linked to blender, and there is no need to add additional code in your addon directory.

To be more specific, te following steps will be taken:

1) Disable the add-on in Blender (if there is one that matches on the directory name)
2) Remove the add-on in Blender (if there is one that matches on the directory name)
3) Make a zipfile of the add-on directory
4) Install the add-on with the zipfile
5) Unlink the zipfile
6) Reload the classes from the add-on that were registered by blender
   (determined by name startswith directory name)
7) Enable the add-on (by directory name)


## Instructions

- Install this add-on in Blender.
- In the add-on preferences for this add-on you can add directory paths to the project(s) you are working on.
- Make sure to select the project(s) that needs to be reinstalled
- By hitting the button in the user preferences, the selected add-on(s) will be reinstalled. 
- A hotkey could be assigned to make this process easier. 
  Then you don't have to go to the add-on preferences as long as you work on the same project.


## This is an experiment
There are many ways to achieve a similar result. 
The most popular is to add extra code in your project, for development purposes only, that checks if modules have to be reloaded.
When your project is linked with Blender, addon changes can be picked up automatically.
That might be the first solution you could try.

The disadvantages of that solution are.
- the additional code has to be removed every time you share the add-on. And added everytime you work on another add-on.
- there is no proper feedback on the actual reloading / reinstall action. 
  
I don't might to hit one action purposely to launch a re-installation (and watch the feedback). 
Furthermore, I just like to uninstall, remove, and install an addon again with a zipfile of the directory. 
To make sure I work with the exact same code I would send to other users.

Some discussion on this topic: https://developer.blender.org/T67387


## Known bugs / issues
- This add-on does not work with single file add-ons, only with directories. (non bug) 
- When an add-on fails on register, and the error is solved, it will fail the second time on module loading. 
  It is best to restart Blender in that case.
- Unregister for this add-on 'reinstall_addons' can give an error in some cases. 
  (only after some loading / unloading of other add-ons was done..)
  