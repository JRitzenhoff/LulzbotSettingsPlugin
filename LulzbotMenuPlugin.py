# Copyright (c) 2021 ritzenhoffj
# The LulzbotMenuPlugin is released under the terms of the AGPLv3 or higher.

import re
from collections import OrderedDict

# NOTE: 
#   Cura is built on the project Uranium under the Ultimaker git repository
#   The UM referenced here is a package inside of the Uranium repository (under the root)
#       https://github.com/Ultimaker/Uranium/blob/master/docs/plugins.md
# 
#   This project can be defined as an "Extension"
#       Hence the plugin inherits the extension class

# Used for real coding
from UM.Extension import Extension
from UM.Application import Application
from UM.Settings.SettingDefinition import SettingDefinition
from UM.Settings.DefinitionContainer import DefinitionContainer
from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.Logger import Logger


class LulzbotMenuPlugin(Extension):
    def __init__(self):
        super().__init__()

        # By adding a MenuItem, a subMenu can be added to the "Extensions" tab in Cura
        #  As this plugin is only meant to add settings to the settings menu, an Extensions Menu addition is unnecessary

        self._application = Application.getInstance()

        # "Internationization is the process of preparing software so that it can support local languages and
        #       cultural settings"
        #   This application is only for me (in english) so doing anything with internationalization is unneccessary 
        self._i18n_catalog = None

        self._settings_dict = OrderedDict()

        self._settings_dict["material_soften_temperature"] = {
            "label": "Softening",
            "description": "",
            "type": "float",
            "unit": " °C",
            "default_value": 0,
            "minimum_value": "0",
            "maximum_value_warning": "365",
            "enabled": True,
            "settable_per_mesh": False,
            "settable_per_extruder": False,
            "settable_per_meshgroup": False
        }

        self._settings_dict["material_wipe_temperature"] = {
            "label": "Wiping",
            "description": "",
            "type": "float",
            "unit": " °C",
            "default_value": 0,
            "minimum_value": "0",
            "maximum_value_warning": "365",
            "enabled": True,
            "settable_per_mesh": False,
            "settable_per_extruder": False,
            "settable_per_meshgroup": False
        }

        self._settings_dict["material_probe_temperature"] = {
            "label": "Probing",
            "description": "",
            "type": "float",
            "unit": " °C",
            "default_value": 0,
            "minimum_value": "0",
            "maximum_value_warning": "365",
            "enabled": True,
            "settable_per_mesh": False,
            "settable_per_extruder": False,
            "settable_per_meshgroup": False
        }

        self._settings_dict["material_part_removal_temperature"] = {
            "label": "Part Removal",
            "description": "",
            "type": "float",
            "unit": " °C",
            "default_value": 0,
            "minimum_value": "0",
            "maximum_value_warning": "365",
            "enabled": True,
            "settable_per_mesh": False,
            "settable_per_extruder": False,
            "settable_per_meshgroup": False
        }

        self._settings_dict["material_keep_part_removal_temperature"] = {
            "label": "Maintaining Part Removal",
            "description": "",
            "type": "float",
            "unit": " °C",
            "default_value": 0,
            "minimum_value": "0",
            "maximum_value_warning": "365",
            "enabled": True,
            "settable_per_mesh": False,
            "settable_per_extruder": False,
            "settable_per_meshgroup": False
        }

        # self._settings_dict["adhesion_z_offset"] = {
        #     "label": "Z Offset",
        #     "description": "An additional offset of the build platform in relation to the nozzle. A negative value 'squishes' the print into the buildplate, a positive value will result in a bigger distance between the buildplate and the print.",
        #     "type": "float",
        #     "unit": "mm",
        #     "default_value": 0,
        #     "minimum_value": "-(layer_height_0 + 0.15)",
        #     "maximum_value_warning": "layer_height_0",
        #     "resolve": "extruderValue(adhesion_extruder_nr, 'adhesion_z_offset') if resolveOrValue('adhesion_type') != 'none' else min(extruderValues('adhesion_z_offset'))",
        #     "settable_per_mesh": False,
        #     "settable_per_extruder": False,
        #     "settable_per_meshgroup": False
        # }
        # self._settings_dict["adhesion_z_offset_extensive_processing"] = {
        #     "label": "Extensive Z Offset Processing",
        #     "description": "Apply the Z Offset throughout the Gcode file instead of affecting the coordinate system. Turning this option on will increae the processing time so it is recommended to leave it off.",
        #     "type": "bool",
        #     "default_value": False,
        #     "value": "True if machine_gcode_flavor == \"Griffin\" else False",
        #     "settable_per_mesh": False,
        #     "settable_per_extruder": False,
        #     "settable_per_meshgroup": False
        # }

        # Container Stacks are how settings in Cura are handled
        #   "The profiles that are currently in use are stored in several container stacks. 
        #       These container stacks always have a definition container at the bottom, 
        #       which defines all avaiable settings and all available properties for each setting."

        # In essence, once all of the settings are loaded, this extension want's to make changes and add a few
        ContainerRegistry.getInstance().containerLoadComplete.connect(self._onContainerLoadComplete)

    def _onContainerLoadComplete(self, container_id):
        if not ContainerRegistry.getInstance().isLoaded(container_id):
            # skip containers that could not be loaded, or subsequent findContainers() will cause an infinite loop
            return

        try:
            container = ContainerRegistry.getInstance().findContainers(id = container_id)[0]
        except IndexError:
            # the container no longer exists
            return

        if not isinstance(container, DefinitionContainer):
            # skip containers that are not definitions
            return
        if container.getMetaDataEntry("type") == "extruder":
            # skip extruder definitions
            return

        material_category = container.findDefinitions(key="material")

        # Just makes sure that the container hasn't already been added
        setting_definitions = container.findDefinitions(key=list(self._settings_dict.keys())[0])
        # returns a list of "SettingDefinition" -- UM.Settings.SettingDefinition.py

        if material_category and not setting_definitions:
            # this machine doesn't have the defined settings yet
            material_category = material_category[0]
            for setting_key, setting_dict in self._settings_dict.items():

                definition = SettingDefinition(setting_key, container, material_category, self._i18n_catalog)
                definition.deserialize(setting_dict)

                # add the setting to the already existing platform adhesion settingdefinition
                # private member access is naughty, but the alternative is to serialise, nix and deserialise the whole
                # thing, which breaks stuff
                material_category._children.append(definition)
                container._definition_cache[setting_key] = definition
                container._updateRelations(definition)
