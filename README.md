# Led-Badge-44x11
Upload tool for an led name tag with USB-HID interface

![LED Mini Board](photos/green_badge.jpg)

## Warning

There are many different versions of LED Badges on the market.
This one uses an USB-HID interface, while others use USB-Serial (see references below).

The type supported by this project has an array of 44 x 11 LEDs and
identifies itself on the USB as

    idVendor=0416, idProduct=5020
    Mfr=1, Product=2, SerialNumber=0
    LSicroelectronics LS32 Custm HID

## Command Line Installation and Usage

Required dependencies on Debian/Ubuntu Systems:

    sudo apt install python3-usb

#### Examples:

Sudo may or may not be needed for accessing the USB device, depending on your system.

    sudo python3 ./led-badge-11x44.py "Hello World!"

loads the text 'Hello World!' as the first message, and scrolls it from right to left (default scroll mode=0) and speed 4 (default). After an upload the device shows the first message once and returns to the charging screen if still connected to USB. Either pull the plug or press the small button next to the USB connector.

    sudo python3 ./led-badge-11x44.py -m 6 -s 8 "Hello" "World!"

loads the text 'Hello' as message one and 'World!' as message two. Compare the difference in quoting to the previous example. Up to 8 messages can be uploaded. This example uses mode 6, which drops the words with a nice little animation vertically into the display area. Speed is set to maximum here, for smoothness.

Per default you will only see 'Hello'.  To see all messages, press the small button next to the USB connector multiple times, until you briefly see 'M1-8'. Now the display loops through all uploaded messages.

    sudo python3 ./led-badge-11x44.py -m 5 :gfx/fablabnbg_logo_44x11.png:

loads a fullscreen still image. Avoid whitespace between colons and name.

    sudo python3 ./led-badge-11x44.py "I:HEART2:my:gfx/fablab_logo_16x11.png:fablab:1:"

uses one builtin and one loaded image. The heart is builtin, and the fablab-logo is loaded from file. The fablab logo is used twice, once before the word 'fablab' and again behind through the reference ':1:' (which references the first loaded image).

![LED Mini Board](photos/love_my_fablab.jpg)

    sudo python3 ./led-badge-11x44.py sudo ./led-badge-11x44.py -s7 -m0,1 :bicycle: :bicycle_r:

shows a bicycle crossing the display in left-to-right and right-to-left (as a second message). If you select the 'M1-8' mode, the bike permanently runs back and forth the display. You may add a short message to one or both, to make it appear the bike is pulling the text around.

    python3 ./led-badge-11x44.py --list-names

prints the list of builtin icon names, including :happy: :happy2: :heart: :HEART: :heart2: :HEART2: :fablab: :bicycle: :bicycle_r: :owncloud: ::

    python3 ./led-badge-11x44.py --help

prints some condensed help:

<pre>
Usage: led-badge-11x44.py [-h] [-s SPEED] [-m MODE] [-p FILE] [-l]
                          MESSAGE [MESSAGE ...]

Upload messages or graphics to a 44x11 led badge via USB HID. Version 0.5 from
https://github.com/jnweiger/led-badge-44x11 -- see there for more examples and
for updates.

positional arguments:
  MESSAGE               Up to 8 message texts with embedded builtin icons or
                        loaded images within colons(:) -- See -l for a list of
                        builtins

optional arguments:
  -h, --help            show this help message and exit
  -s SPEED, --speed SPEED
                        Scroll speed. Up to 8 comma-seperated values (range
                        1..8)
  -m MODE, --mode MODE  Up to 8 mode values: Scroll-left(0) -right(1) -up(2)
                        -down(3); still-centered(4) -left(5); drop-down(6);
                        curtain(7); laser(8)
  -p FILE, --preload FILE
                        Load bitmap images. Use ^A, ^B, ^C, ... in text
                        messages to make them visible. Deprecated, embed
                        within ':' instead
  -l, --list, --list-names, --listnames
                        list named icons to be embedded in messages and exit

Example combining image and text: sudo ./led-badge-11x44.py "I:HEART2:you"
</pre>



## Related References (for USB-Serial devices)
 * https://github.com/Caerbannog/led-mini-board
 * http://zunkworks.com/projects/programmablelednamebadges/
 * https://github.com/DirkReiners/LEDBadgeProgrammer
 * https://bitbucket.org/bartj/led/src
 * http://www.daveakerman.com/?p=1440
 * https://github.com/stoggi/ledbadge
