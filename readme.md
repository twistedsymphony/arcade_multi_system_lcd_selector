# twistedsymphony's universal multi-kit LCD Selector (aka CAERTF-MS)

# F.A.Q.

**What is this thing?**

This is a small remote selector that can be adapted and used on DIP-switch based arcade multi-systems. 
Once the device is configured and installed, rather than selecting your game by setting dip switches, users can push the "Up" (D0) and "Down" (D2) buttons to navigate visually through the game list, then push "Select" (D1) to select the game. The selector will then hold the arcade board in reset and electrically configure the dip switches before releasing reset allowing the selected game to boot.

**What is a DIP-switch based arcade multi-system?**

It's pretty niche, but some arcade games share the same electronics and only really have differing software. Arcade Enthusiests have designed and built "multi-systems" that allow switching out the software so that rather than having a whole separate set of electronics for each game, one set of electronics can play multiple games. The simpliest of these multi-systems will often use Dip-switches to set the game, which is cheap and effective but can be quite clumsy and unintuitive to use.

**Why was this made?**

Selecting your game using dip-switches can be frustrating, annoying, and very much non-intuitive. You typically need to have a little chart near by that tells you how to set the dip switches for the game you want to play, and if you want to switch games you have to power everything down to change it. Doing this while your arcade PCB is inside of an arcade cabinet means you sometimes have to be a contortionist with night-vision and the dexterity of a bomb-diffusal expert just to change that game you're playing. A selector like this one, that is easy to use and understand, solves most of those problems. 

This is being made open source in the hopes that future multi-systems that get developed by anyone in the community can easily incorporate support for this benefiting both the functionality of their multi and the users in the community. 

**What features/functinoality does this have?**

You get a full-color TFT display to show the game logos, you get 3 buttons: up, down, and select, so you can scroll through the game list and select the game you'd like to play. Selecting the game displays a loading screen while it resets the PCB and virtually configures the dip switches for game you selected. If an image isn't found it it will display the title of the game as text on the screen, and can seemilessly scroll between text and image based entries. It uses a standard 10-pin IDC ribon cable connection to the multi so you can remote mount the selector outside the cab by simply buying a cable long enough for your setup.

Through the menu configuration file you can control:
* what image is displayed with each game
* what image to display for the loading screen
* what text is to be displayed if an image isn't available
* what the dip configuration is for each selection
* what order you would like the games to appear in (you can even have the same game appear multiple times, in multiple places or with multiple names or images if you like)
* which games you would like displayed in the list or not displayed in the list
* which game you would like to load by default when you first power on
* the amount of idle time before the menu to goes back to displaying the current running game if you scrolled without selecting anything and then stopped

See the section below on "reconfiguring the menu_config.json file" for details on how to adjust these settings.

future features:
* remember last game. The code has support to remember the last selected game on power down and select that game on next power up, but there's a bug that's preventing that from functioning
* Selection over WiFi from your phone or other devie. the selector has Wifi Support so this is possible, the software just needs to be built.

**How Difficult is this to setup and use?**

If you're designing and building a multi kit this will add exactly $0 to your production costs. For the bare minimum support you simply need to add a 10-pin header footprint to your PCB for the selector and a 1-pin header footprint for a reset wire. This adds no cost to production and maybe an hour (not even) of your time to add the header to your schematic and PCB layout. I've even provided pre-configured footprints to allow mounting of the selector directly to your PCB if you have the room for it. If you want stronger support still you can spend a few extra cents per PCB and solder in the headers to each of the footprints you added to make use of the LCD selector completely plug and play for your users.

If you're a user of multis the difficulty varies depending on the multi-kit, setting up the kit at most would require soldering of some simple through-hole parts. The selector itself uses an off-the-shelf display and MCU unit from Adafruit coupled with a custom designed interface PCB that is open source and you can send the design files out and have made completely, or find someone selling them. Installing the software is as simple as copying files over to a USB thumb drive.

**Can this be used on multi-kits that weren't designed for it?**

Potentially, from an electrical standpoint this can be used with any multikit design to select games by up to 7 dip-switches (or jumpers). The challenge is wiring it up in a way that doesn't look like a science-experiment, which will vary greatly depending on the multi. The software is fully customizable, in addition to the "menu" config file there is a separate "multi" config file that allows you to specify the parameters of the multi for the software to tailor itself for it's use without any code changes.

# Putting Together a Selector as a Multi-Kit User

## Building a Selector
To piece together a selector you need 3 parts:
1. An Adafruit ESP32-S2 Reverse TFT Feather, which can be [purchased directly from Adafruit](https://www.adafruit.com/product/5345)
2. An CAERTF-MS Interface PCB, the schematics footprint, BOM, and ready-to-go production files are available within this repo
3. a 10-pin IDC cable. Multi-kits designed for selector mounting using the footprints in this repo are designed to utilize a 1.5in (38mm) length cable which can be [purchased from Adafruit](https://www.adafruit.com/product/556) though any 10-pin (2x5 female to female) IDC cable should work.

the Adafruit ESP32-S2 Reverse TFT Feather unit includes 2 male pin header rows, you will need to solder these to the unit to allow it to plugin to the CAERTF-MS interface PCB. While looking at the LCD with USB port on the left you will want to solder the entire bottom row of pins and the first 4 pins on the top left to allow it to plug into a CAERTF-MS Interface PCB and complete the assembly. 

## Setting up a Software release on a new Selector.
1. With the selector disconnected from both the multi-kit and the CAERTF-MS interface board, and disconnected from any power source, connect a USB-C cable between the selctor and your PC. 
2a. If this is the first time configuring the selector the display on the selector should say "Adafruit Feather" with some information about the button and "battery" voltages, this is just the default software loaded. On the back of the display you should see a green and blue LED and there is a small reset button next to the USB port, you'll want to click this button once to reset, then double click it to put it into bootloader mode. If successful you should see the screen change and your PC should recognize a USB storage device called "FTHRS2BOOT" If not, attempt the reset button sequence again (the timing between the first click to reset and the subsequent double click can be tricky to get right)
2b. Copy the latest Circuit Python .UF2 file file to the root of the "FTHRS2BOOT" drive. You can [get this file from the circuitpython website]( https://circuitpython.org/board/adafruit_feather_esp32s2_reverse_tft/) (at the time of this writing 9.2.8 was the lastest version and known to work)
2c. Once the file has been copied over, the display should automatically restart and it will display some small white text on the screen and you will now see a new USB storage device attached to your computer called "CIRCUITPY"
3. Copy the entire content of a release file over to the root folder of the CIRCUIT PY drive. your computer will likely ask if you want to overwrite code.py, select yes to overwrite.

Releases should include:
  * code.py from the he /source directory here on github 
  * multi_config.json and menu_config.json configuring the selector specificlly to your multi kit
  * a /lib folder with the adafruit_display_text library
  * a /images fold that includes the loading.bmp image along with .bmp images for each game the multi supports.
4. you can now test out the menu to make sure it has the games you expect and see how it functions before connecting it to your multi. If you'd like to ajust settings in "menu_config.json" file you can do so to configure the menu to your liking and confirm those changes work while you still have it hooked up to your PC. it is NOT recommended to adjust the multi_config.json settings as these determine the electrical configurain for the multi.
5. once you're done simply unplug the USB-C cable from the display and now the software on the selector is ready for the multi.

**NOTE: Do not connect the USB-C on the Selector at the same time the 10-pin connector is attached to the Multi PCB ** Doing so risks damaging your USB host device. The interface PCB has some protections to help prevent voltage back-feed from the USB port to the Multi-PCB but there are no protections to stop voltage back feed from the multi-PCB to the USB port as such there is risk of damage to your USB Host device.

## Installing a Selector onto your Multi
1. Follow the steps above to build the selector hardware
2. Follow the steps above to install the software on the selector
3. Ensure that all Dips switches on your multi are set to "OFF" (0) and that any rotary selectors are set to position "0". Alternatively, you can completely remove any dips or rotary switches from your multi-PCB (if you set any of these switches to other positions it causes that dip to perminently register as "on" resuling in different selections being made other than the game you selected on the LCD selector)
3. Plug the Adafruit ESP32-S2 Reverse TFT Feather into the CAERTF-MS Interface PCB, Make sure the USB-C port is disconnected (Do not connect the USB-C on the Selector at the same time the 10-pin connector is attached to the Multi PCB ** the interface PCB has some protections to help prevent voltage back-feed from the USB port to the Multi-PCB but there are no protections to stop voltage back feed from the multi-PCB to the USB port as such there is risk of damage to your USB Host device.)
4. Connect the 10-pin IDC cable between the selector and the appropriate header on your multi-PCB
5. (optional) Install any mounts or brackets that may be avalable for your particular multi

## Making Images for the Selector
Images for the selector should be 240x135 pixels and .bmp format. it's recommended to used 8-bit indexed color format for the .bmp as this should set the file size to 33kb for each image. This is small enough to support 32 images for multis with 5-dip switches (32 game slots) or less. For multis with 6 dips (64 game slots) or 7 dips (128 game slots) you will likely need to get creative with lower bit-depth color or use text rather than images for some games.

While BMP files are larger the processing speed required to decode .jpg or .png compression on images takes about 1-2 seconds per image load which dramatically slows down menu navigation making the game selection experience feel extremely laggy. BMP was chosen as it is essentially uncompressed and is able to load instantly and at 8-bit indexed color is still small enough to support images for all games on nearly all dip-switch based multis.

## reconfiguring the menu_config.json file
(Details Coming Soon)

# Adding Support for this Selector to your Multi as a Multi-Kit Developer
(Details Coming Soon)

## Electrical Pinout for 10-Pin header and Reset Wire
(Details Coming Soon)

## Footprints and mounting considerations
(Details Coming Soon)

## Configuring the multi_config.json File
(Details Coming Soon)
