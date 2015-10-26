# zm-tattletale

## Synopsis
zm-tattletale is a *multi-platform* small python client which connects to a ZoneMinder event server, and creates notifications of varying types to alert the user to new ZoneMinder events.


## Motivation
I pay more attention to my computer than my phone, so I needed a way to maintain my constant paranoid awareness while I was away from my phone (immersed in my computer), so I wrote this.

## Warnings
~~This software is no good yet. It needs a lot of polish and some TLC. User beware. It'll probably be totally re-written.~~ It got re-written. It's OK; but not great. You get what you pay for.

## Requirements
* Python 3
* ZoneMinder 1.28.107 or greater
* [zmeventserver] (https://github.com/pliablepixels/zmeventserver)

## Installation
pip install websockets
pip install pyglet (sound alert support)

## Problems
*TODO*
* It's still ignoring SSL certs
* It has no option for what monitors to watch
* No good interface (no one wants to ctrl-c)
* using the dialog window options is blocking, no threading yet.

## Screenshots
![SS1](https://raw.githubusercontent.com/segordon/zm-tattletale/master/screenshot1.png)
![SS2](https://raw.githubusercontent.com/segordon/zm-tattletale/master/screenshot2.png)

## License
*TODO*

## Thanks
thanks to [@pliablepixels](https://github.com/pliablepixels/) for teaching me how to use their [zmeventserver] (https://github.com/pliablepixels/zmeventserver)
