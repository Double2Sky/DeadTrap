![alt tag](https://media.discordapp.net/attachments/671809375807209472/722385841414078484/image-removebg-preview1.png?width=381&height=396) 

### An OSINT tool to track down footprints of a phone number

 <a href="https://chr0m0s0m3s.github.io/DeadTrap/">Official Website</a>
 
## Snapshot
Couldnt show the full scan cuz it was too long to capture it in one screen hence only showed the part which i thought was important
![alt tag](https://media.discordapp.net/attachments/671809375807209472/722377731182034994/Screenshot_20200616_144711.png?width=794&height=396)

## How it works
![alt tag](https://img.wonderhowto.com/img/original/09/23/63728168197692/0/637281681976920923.jpg)

## Installation
Type the following commands in your terminal if you are on Linux
```
git clone https://github.com/Chr0m0s0m3s/DeadTrap.git
cd DeadTrap
python3 setup.py
```
If you are on Windows then you have to setup geckodriver first ( Download the latest Version Only )
Geckodriver download link : https://github.com/mozilla/geckodriver/releases

### Numverify API
DeadTrap relies on the [numverify api](https://numverify.com/documentation) to discover
some details about phone numbers. A default API key is included with DeadTrap for
convenience, but it allows a limited number of API calls each month and may be
exhausted by other DeadTrap users. It is recommended that you get your own free
numverify API key by going to the [numverify product page](https://numverify.com/product).

Once you have your numverify API key, you can copy it into `./deadtrap.conf`. Then,
perform the following steps:

```
mkdir -p $HOME/.config/deadtrap
cp ./deadtrap.conf $HOME/.config/deadtrap/deadtrap.conf
```

DeadTrap will now use your numverify API key to access the numverify API.

## Useage
type the following commands in your terminal
```
python3 main.py
```

then enter the phone number along with the country prefix and you are ready to go

### Lincense
[![license](https://img.shields.io/github/license/Chr0m0s0m3s/DeadTrap.svg?style=flat-square)](https://github.com/Chr0m0s0m3s/DeadTrap/blob/master/LICENSE)

