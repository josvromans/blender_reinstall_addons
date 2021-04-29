bl_info = {
    "name": "Reinstall addon(s)",
    "author": "Jos Vromans",
    "version": (0, 0, 1),
    "blender": (2, 92, 0),
    "location": "Addons -> Reinstall add-on(s)",
    "description": "Reinstall custom add-ons after code changes",
}
import shutil
import sys
from importlib import reload
from pathlib import Path

import bpy
import addon_utils


class MyAddons_OT_add(bpy.types.Operator):
    bl_idname = "my_addons.add"
    bl_label = "Add the path to a personal add-on"
    bl_options = {'REGISTER'}

    def execute(self, context):
        context.preferences.addons[__name__].preferences.my_addons.add()
        return {'FINISHED'}


class MyAddons_OT_remove(bpy.types.Operator):
    bl_idname = 'my_addons.remove'
    bl_label = 'Remove this add-on path'
    bl_options = {'REGISTER'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        context.preferences.addons[__name__].preferences.my_addons.remove(self.index)
        return {'FINISHED'}


class MyAddons_OT_reinstall(bpy.types.Operator):
    bl_idname = "my_addons.reinstall"
    bl_label = "Reinstall the selected add on"
    bl_options = {'REGISTER'}

    def execute(self, context):
        """
        1) Disable the add-on in Blender (if there is one that matches on the directory name)
        2) Remove the add-on in Blender (if there is one that matches on the directory name)
        3) Make a zipfile of the add-on directory
        4) Install the add-on with the zipfile
        5) Unlink the zipfile
        6) Reload the classes from the add-on that were registered by blender
           (determined by name startswith directory name)
        7) Enable the add-on (by directory name)
        """
        my_addons = context.preferences.addons[__name__].preferences.my_addons

        if not any(addon.selected and addon.path != '' for addon in my_addons):
            self.report({'ERROR'}, f"Please add and/or select at least one directory.")
            return {'FINISHED'}

        unregister_errors = []
        reinstalled_addons = []
        installed_addons = []

        for my_addon in my_addons:
            if not my_addon.selected:
                continue

            directory_path = Path(my_addon.path)

            if not directory_path.is_dir():
                self.report({'ERROR'}, f"{directory_path} is not a directory!")
                continue

            addon_name = directory_path.name

            # True for reinstall, False for (first) install
            reinstall = addon_name in [_addon.__name__ for _addon in addon_utils.modules()]
            if reinstall:
                try:
                    # addon_disable is not necessary, because addon_remove will also unregister.
                    # But the latter will not raise an error when something goes wrong on unregister. It does log
                    # the error to the Python console. I like to catch the error to report a message to the
                    # user in Blender, and let addon_remove encounter the same error and logs it to the console
                    bpy.ops.preferences.addon_disable(module=addon_name)
                except Exception as e:
                    unregister_errors.append(addon_name)

                bpy.ops.preferences.addon_remove(module=addon_name)

            # make a zipfile, install the addon in Blender and unlink the zipfile
            zipfile_path = Path(shutil.make_archive(str(directory_path), 'zip', str(directory_path.parent), addon_name))
            bpy.ops.preferences.addon_install(filepath=str(zipfile_path), overwrite=True)
            zipfile_path.unlink()

            sys.modules[__name__] = reload(sys.modules[__name__])
            for name, module in sys.modules.items():
                if name.startswith(f"{addon_name}."):
                    globals()[name] = reload(module)

            try:
                bpy.ops.preferences.addon_enable(module=addon_name)
            except Exception as e:
                # An exception happened in addon_enable, before raising the exception, make sure the modules that
                # were loaded are deleted. Otherwise they will cause errors for the next install
                print('Exception in addon_enable, delete the following modules that were loaded already:')
                for name in [name for name, module in sys.modules.items() if name.startswith(f"{addon_name}.")]:
                    print(f'del sys.modules[{name}]')
                    del sys.modules[name]

                raise e

            # These methods are useful for related add on reloading,
            # but I believe they are not needed when reinstalling the addon with a zipfile
            # bpy.ops.preferences.addon_refresh()
            # bpy.ops.script.reload()
            # bpy.ops.wm.save_userpref()

            if reinstall:
                reinstalled_addons.append(addon_name)
            else:
                installed_addons.append(addon_name)

        msg = ''
        report_type = 'INFO'
        if reinstalled_addons:
            msg += f"Reinstalled: {', '.join(reinstalled_addons)}. "
        if installed_addons:
            msg += f"Installed: {', '.join(installed_addons)}. "
        if unregister_errors:
            msg += f"Check unregister errors for: {', '.join(unregister_errors)}"
            report_type = 'ERROR'
        if not msg:
            msg = 'Something went wrong'
            report_type = 'ERROR'

        self.report({report_type}, msg)

        return {'FINISHED'}


class MyAddon(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        default='',
        name='',
        description='The path to the original directory of the addon code',
        subtype="DIR_PATH",
    )
    selected: bpy.props.BoolProperty(default=True, name='')


class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    my_addons: bpy.props.CollectionProperty(type=MyAddon)

    def draw(self, context):
        if not self.my_addons:
            # just add one directory row by default, to save one click...
            self.my_addons.add()

        layout = self.layout
        label_row = layout.row()

        row = label_row.row(align=True)
        row.label(text="List of your local add-on development directories.")
        row.scale_x = 0.8
        row = label_row.row(align=True)
        row.operator('my_addons.add', text='Add directory', icon='ADD')
        row.scale_x = 0.2

        for index, my_addon in enumerate(self.my_addons):
            row = layout.row()

            icon = "CHECKBOX_HLT" if my_addon.selected else "CHECKBOX_DEHLT"
            row.prop(my_addon, 'selected', icon=icon, text="", emboss=False)
            row.prop(my_addon, 'path')
            row.operator('my_addons.remove', text='', icon='TRASH').index = index
            row.scale_y = 2.0

        row = layout.row()
        row.operator('my_addons.reinstall', text='Reinstall selected add-ons', icon='FILE_REFRESH')
        row.scale_y = 2.0


blender_classes = [
    MyAddon,
    MyAddonPreferences,

    MyAddons_OT_add,
    MyAddons_OT_remove,
    MyAddons_OT_reinstall,
]


addon_keymaps = []


def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('my_addons.reinstall', 'R', 'PRESS', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)
