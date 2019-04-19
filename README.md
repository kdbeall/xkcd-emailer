# About

A Python3 program that fetches xkcd comics every Monday, Wednesday, and Friday and then emails them to you.

## How to

First, change the xkcd_emailer.ini file with your personal settings.

Example Usage

    [Default]
    smtp_server: smtp.foo.com
    smtp_port: 587
    sender_email: sender@example.com
    sender_password: foopassword
    receiver_email: receiver@example.com

Ideally, you want this script to automatically run at startup. The process for doing this will vary by operating system. But, on most Linux systems, [systemd](https://en.wikipedia.org/wiki/Systemd) is what is used for managing services. I've included a sample systemd .service, xkcd-emailer.service, to allow the script to be run on startup. You can follow the instructions [here](https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) to use the .service file.
