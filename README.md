# Led-Badge-44x11
Upload tool for an led name tag with USB-HID interface

![LED Mini Board](green_badge.jpg)

# Warning

There are many different versions of LED Badges on the market.
Some even look identical, but are not.
This one uses an USB-HID interface, while many others use USB-Serial.

The type supported by this project has an array of 44 x 11 LEDs and
identifies itself on the USB as

    idVendor=0416, idProduct=5020
    Mfr=1, Product=2, SerialNumber=0
    LSicroelectronics LS32 Custm HID

# Command line parameters

<pre>
Usage: led-badge-11x44.py [-h] [-s SPEED] [-m MODE] [-l FILE]
                          message [message ...]

./led-badge-11x44.py Version 0.3 -- upload messages to a 44x11 led badge via
USB HID. https://github.com/jnweiger/led-badge-44x11

positional arguments:
  message               Up to 8 message texts or image file names

optional arguments:
  -h, --help            show this help message and exit
  -s SPEED, --speed SPEED
                        Scroll speed. Up to 8 comma-seperated values (range
                        1..8)
  -m MODE, --mode MODE  Up to 8 mode values: Scroll-left(0) -right(1) -up(2)
                        -down(3); still-centered(4) -left(5); drop-down(6);
                        curtain(7); laser(8)
  -l FILE, --load FILE  Bitmap images, made available as ^A, ^B, ^C, ... in
                        text messages

</pre>



## References (all USB-Serial)
 * https://github.com/Caerbannog/led-mini-board
 * http://zunkworks.com/projects/programmablelednamebadges/
 * https://github.com/DirkReiners/LEDBadgeProgrammer
 * https://bitbucket.org/bartj/led/src
 * http://www.daveakerman.com/?p=1440
 * https://github.com/stoggi/ledbadge
