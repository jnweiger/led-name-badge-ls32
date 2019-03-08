# Led-Badge-44x11
Upload tool for an led name tag with USB-HID interface

![LED Mini Board](photos/green_badge.jpg)

## Warning

There are many different versions of LED Badges on the market.
Some even look identical, but are not.
This one uses an USB-HID interface, while many others use USB-Serial.

The type supported by this project has an array of 44 x 11 LEDs and
identifies itself on the USB as

    idVendor=0416, idProduct=5020
    Mfr=1, Product=2, SerialNumber=0
    LSicroelectronics LS32 Custm HID

## Command Line Installation and Usage

Required dependencies on Debian/Ubuntu Systems:

    sudo apt install python3-usb

#### Examples:

    sudo python3 ./led-badge-11x44.py "Hello World!"

loads the text 'Hello World!' as the first message, and scrolls it from right to left (default scroll mode=0) and speed 4 (default). After each upload, press the little button next to the USB connector once to see the first message permanently. If you don't press the button, the device shows the message only once and returns to the charging screen. Sudo may or may not be needed, depending on your system.

    sudo python3 ./led-badge-11x44.py -m 6 -s 8 Hello World!

loads the text 'Hello' as message one and 'World!' as message two. Note the diffrence in quoting. Up to 8 messages can be uploaded. This example uses mode 6, which is dromps the words with a nice little animation vertically into the display area. Speed is set to maximum here, so that the animation is very smooth. Per default you will only see 'Hello'. To get both messages alternating, press the little button next to the USB connector two more times, so that the message 'M1-8' appears. Now the display loops through all uploaded messages.

    sudo python3 ./led-badge-11x44.py -m 5 gfx/fablabnbg_logo_44x11.png

loads a fullscreen still image. (Or displays the pathname, if the image was not found. That is a hack. Sorry)

    sudo python3 ./led-badge-11x44.py -l gfx/heart.png -l gfx/fablab_logo_16x11.png  "I^Amy^Bfablab^B"

preloads two images, a heart and a crude fablab logo as images 1 and two. The images can then be embedded in a message by using control characters. To enter the ^A control character on the shell, press CTRL-V followed by CTRL-A.

![LED Mini Board](photos/love_my_fablab.jpg)


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
