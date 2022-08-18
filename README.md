# Launpach2KB

A linux CLI tool to map keyboard hotkeys with the Novation Launchpad device.

> **Important:** I have only tested this implementation with the first Novation Launchpad, model `NOVLPD01`.

### Usage

```
python src/main.py
```

This will ask for the MIDI port, and will default the config file to `config/config.yml`. You can also pass the port number and the config file, as follows:

```
python src/main.py --port=1 --config=config/config.yml
```

Or

```
python src/main.py -p 1 -c config/config.yml
```

For some reason sometimes it won't start detecting the device presses. When this happens pressing the `mixer` button on the top-right is enough for it to start working.

### Configuration

The configuration file must be a `.yaml` or `.yml` format.
There is an example config file at `config/config.yml`
For each cell you will require to set it as follows:

Example:

```
- cell: 112
  keys:
  - 'ctrl'
  - 'shift'
  - 'e'
  color: 120
```

This will bind the cell 112 to trigger `CTRL+SHIFT+E` when pressed.

- `cell` indicates the cell number [See image below](#cells).
- `keys` are the keyboard keys to be pressed. [Keys reference](assets/key_names_reference.json).
- `color` is a number ranging from 0 to 127. 



Example of multiple cells:

```
- cell: 112
  keys:
  - 'ctrl'
  - 'shift'
  - 'e'
  color: 120
- cell: 113
  keys:
  - 'ctrl'
  - 'shift'
  - 'f'
  color: 80
- cell: 113
  keys:
  - 'f'
  color: 60
```

### Run from source

- Create virtual enviroment & install dependencies 
```
virtualenv env
source env/bin/activate
pìp install -r requirements.txt
```

- Tkinter is also required:

**Arch linux**
```
sudo pacman -S tk
```
**Debian & Ubuntu**
```
sudo apt-get install python3-tk
```
**Fedora**
```
sudo dnf install python3-tkinter
```

Then run as shown [previously](#usage).

Haven't tested in Windows/MacOS.

* * *

### Cells

![Cells reference image](assets/cells.png)
