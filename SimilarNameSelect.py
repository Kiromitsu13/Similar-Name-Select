bl_info = {
    "name": "Select Objects by Name Parts",
    "description": "Select objects by name similarities",
    "author": "Kiromitsu",
    "version": (1, 0, 1),
    "blender": (3, 5, 0),
    "location": "Select Menu / Hotkey: Ctrl+Alt+S",
    "warning": "",
    "category": "Selection",
}

import bpy

class SimilarNameSelectOperator(bpy.types.Operator):
    """Select objects with similar names."""
    bl_idname = "object.similar_name_select"
    bl_label = "Similar Name Select"

    # Define the search_text property as a StringProperty
    search_text: bpy.props.StringProperty(name="Search Text")

    # Define add_to_selection and remove_from_selection as BoolProperties with default values of False
    add_to_selection: bpy.props.BoolProperty(name="Add to Selection", default=False)
    remove_from_selection: bpy.props.BoolProperty(name="Remove from Selection", default=False)

    def execute(self, context):
        # Get the currently selected objects
        selection = bpy.context.selected_objects

        # Create a list of objects that match the search text
        to_select = [obj for obj in bpy.context.scene.objects if self.search_text.lower() in obj.name.lower()]

        if self.add_to_selection:
            # If the add_to_selection checkbox is checked, add the matched objects to the selection
            for obj in to_select:
                obj.select_set(True)
        elif self.remove_from_selection:
            # If the remove_from_selection checkbox is checked, remove the matched objects from the selection
            for obj in to_select:
                obj.select_set(False)
        else:
            # If neither checkbox is checked, deselect all objects and select the matched objects
            bpy.ops.object.select_all(action='DESELECT')
            for obj in to_select:
                obj.select_set(True)

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        # Add a text box for the search text
        row = layout.row()
        row.prop(self, "search_text")

        # Add checkboxes for adding and removing objects from the selection
        row = layout.row()
        row.prop(self, "add_to_selection")
        row.prop(self, "remove_from_selection")

def menu_func(self, context):
    # Add the SimilarNameSelectOperator to the Select menu
    self.layout.operator(SimilarNameSelectOperator.bl_idname)

addon_keymaps = []

def register():
    bpy.utils.register_class(SimilarNameSelectOperator)
    # Add the SimilarNameSelectOperator to the VIEW3D_MT_select_object menu
    bpy.types.VIEW3D_MT_select_object.append(menu_func)

    # Add a keymap entry for the SimilarNameSelectOperator
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
    kmi = km.keymap_items.new(SimilarNameSelectOperator.bl_idname, 'F', 'PRESS', ctrl=True, shift=True, alt=False)
    addon_keymaps.append((km, kmi))

def unregister():
    # Remove the SimilarNameSelectOperator from the VIEW3D_MT_select_object menu
    bpy.types.VIEW3D_MT_select_object.remove(menu_func)
    # Unregister the SimilarNameSelectOperator
    bpy.utils.unregister_class(SimilarNameSelectOperator)

if __name__ == "__main__":
    register()