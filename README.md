# led-badge-44x11
Upload tool for an led name tag with USB-HID interface

# Warning

There are many different versions of LED Badges on the market.
Some even look identical, but are not.
This one uses an USB-HID interface, while many others use USB-Serial.

The type supported by this project has an array of 44 x 11 LEDs and
identifies itself on the USB as

    idVendor=0416, idProduct=5020
    Mfr=1, Product=2, SerialNumber=0
    LSicroelectronics LS32 Custm HID


## References (all USB-Serial)
 * https://github.com/Caerbannog/led-mini-board
 * http://zunkworks.com/projects/programmablelednamebadges/
 * https://github.com/DirkReiners/LEDBadgeProgrammer
 * https://bitbucket.org/bartj/led/src
 * http://www.daveakerman.com/?p=1440
 * https://github.com/stoggi/ledbadge
