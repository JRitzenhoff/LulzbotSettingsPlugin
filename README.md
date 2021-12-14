# LulzbotMenuPlugin

This plugin is HEAVILY based off of the ["Z Offset"](https://github.com/fieldOfView/Cura-ZOffsetPlugin) plugin created by github user "fieldOfView" - Aldo Hoeben.

It adds setting named "Lulzbot" to the Lulzbot Print section of Cura. Entering values in the respective fields will override the default values calcualted for the start and end gcode of Lulzbot prints.

This plugin adds settings required by the Lulzbot Taz6 Start GCode including:
* `material_soften_temperature`
* `material_wipe_temperature`
* `material_probe_temperature`

This plugin adds settings required by the Lulzbot Taz6 End GCode including:
* `material_part_removal_temperature`
* `material_keep_part_removal_temperature`


The LulzbotMenu setting can be found in the Custom print setup by using the Search field on the top of the settings. To make these settings permanently visible in the sidebar, right click and select "Keep this setting visible".

With Cura not running, copy this entire directory to this
specific folder and restart Cura:

  * Windows: `%USERPROFILE%\AppData\Roaming\cura\4.7\plugins\`
  * MacOS: `~/Library/Application Support/Cura/4.7/plugins/`
  * Linux: `/home/<username>/.local/share/cura/4.7/plugins/`


# Using the Lulzbot settings
1. Open up the settings tab once the part has been imported
2. Expand the "Material Section"
3. Edit the values for the following using the [material](https://www.lulzbot.com/taz-6-cura-profiles)
and basing the temperature off of the Lulzbot [guide](https://www.lulzbot.com/learn/tutorials/taz-6-gcode)

| Parameter                 | Taz 6 ABS Value |
|:--------------------------|:----------------|
| softening                 | 160 deg C (70% of extrusion)  |
| wipening                  | 160 deg C (70% of extrusion)  |
| probing                   | 160 deg C (70% of extrusion)  |
| part removal              | 50 deg C  |
| maintaining part removal  | 50 deg C  |


# Printer Setup

To effectively use the LulzbotMenuPlugin, there must be a Lulzbot Printer loaded on Ultimaker

I am using the [Lulzbot Taz-6](https://www.lulzbot.com/store/printers/lulzbot-taz-6) and retrieved the print bed information from the Lulzbot website
This comes with the [Single Extruder 0.5mm Print Head](https://www.matterhackers.com/store/l/lulzbot-taz-single-extruder-tool-head-v21/sk/MJQWTAMV)


## NOTE: 
The Taz 6 I'm using has a removable glass plate on it. It, however, also has raised auto-leveling plates.

The net additional offset between the two ends up being -1.0mm.

This exceeds the Z-offset range in Cura "Build Plate Adhesion"
. Therefore, this should be manipulated in the printer settings.
    `Configuration >> Z-Offset >>`

## GCode

This plugin works because the [start gcode](./start_gcode.txt) and [end gcode](./end_gcode.txt) are modified.

These gcode values are taken from the Lulzbot gcode website. It is required for the build-plate auto-leveling and 
nozzle cleaning unique to Lulzbot printers.

## Printhead Settings

The Gantry height is the lowest point on the rails in which the extruder assembly rides to the print bed when the nozzle is at height Z=0

| Parameter         | Explanation |
|:------------------|:------------|
| X min             | horizontal distance between the nozzle and the left edge of the printhead     |
| Y min             | horizontal distance between the nozzle and the front edge of the printhead    |
| X max             | horizontal distance between the nozzle and the right edge of the printhead    |
| Y max             | horizontal distance between the nozzle and the rear edge of the printhead     |
| Gantry Height     | the vertical distance between the build plate and the gantry that holds the printhead |

I believe that for the Luzbot Taz 6, these values are

| Parameter         | Value |
|:------------------|:------|
| X min             | -5mm  |
| Y min             | -8mm  |
| X max             | 15mm  |
| Y max             | 8mm   |
| Gantry Height     | 250mm |

## Editing the Plugin

The `UM` python directory comes from the [Uranium](git@github.com:Ultimaker/Uranium.git) project.

To have accurate dependencies for developing: clone the Uranium project and extract the "UM" directory 
into the same parent as the Plugin. 

