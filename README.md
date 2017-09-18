# Scala Formatter for Sublime 3

Minimal Sublime Text 3 plugin to format Scala files using [Scalafmt](http://[scalameta.org/scalafmt) and [Nailgun](https://github.com/martylamb/nailgun).

## Installation

### Step 1: install this plugin

Clone this repository in `~/Library/Application Support/Sublime Text 3/Packages/`.

### Step 2: install Scalafmt and Nailgun

Run provided `setup.sh`, that will install for you both Scalafmt and Nailgun according to [recommended installation instructions](http://scalameta.org/scalafmt/#Installation).

### Step 3 (optional): add keybinding

Open `Preferences > Key Bindings` and add:

    {
      "keys": ["super+alt+l"],
      "command": "scafor_format_file",
    }

changing `keys` to any sequence of keys you'd like.

## Usage

Open a Scala file, then open the `Command Palette` and select `ScaFor: Format current file`.

## Scalafmt configuration

The plugin uses (and creates, if missing) `~/.scalafmt.conf` so that file can be used to configure `scalafmt`.

## Caveats

Very early stages of development, only tested on OSX El Capitan.
