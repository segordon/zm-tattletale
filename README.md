# zm-tattletale

## Synopsis
zm-tattletale is a small python client which connects to a ZoneMinder event server, and creates notifications of varying types to alert the user to new ZoneMinder events.


## Motivation
I pay more attention to my computer than my phone, so I needed a way to maintain my constant paranoid awareness while I was away from my phone (immersed in my computer), so I wrote this.

## Warnings
This software is no good yet. It needs a lot of polish and some TLC. User beware. It'll probably be totally re-written.

## Requirements
* Python 3 and a bunch of modules *(TODO : pip install what?)*
* Windows *FIXME: multiplatform support*
* ZoneMinder 1.28.107 or greater
* [zmeventserver] (https://github.com/pliablepixels/zmeventserver) 

## Installation
*TODO*

## Problems
*TODO*
* It doesn't care about dropped websockets
* It's still ignoring SSL certs
* It has no option for what monitors to watch
* ONE EVENT AT A TIME, with a big long queue of them behind it.
* No good interface (no one wants to ctrl-c)
* add timestamps to log and alerts.

## Screenshots
![SS1](https://raw.githubusercontent.com/segordon/zm-tattletale/master/screenshot1.png)
![SS2](https://raw.githubusercontent.com/segordon/zm-tattletale/master/screenshot2.png)

## License
*TODO*

## Thanks
thanks to [@pliablepixels](https://github.com/pliablepixels/) for teaching me how to use their [zmeventserver] (https://github.com/pliablepixels/zmeventserver)