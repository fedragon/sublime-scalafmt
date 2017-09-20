# Scala Formatter for Sublime Text 3

Minimal Sublime Text 3 plugin to format Scala files. Powered by [Scalafmt](http://[scalameta.org/scalafmt) and [Nailgun](https://github.com/martylamb/nailgun).

## Installation

### Step 1: Install this plugin

#### ... with [Package Control](https://packagecontrol.io/)

- open the Command Palette
- select `Package Control: Install Package`
- select `ScaFor`

#### ... or manually

Clone this repository in `~/Library/Application Support/Sublime Text 3/Packages/`.

### Step 2: Install Scalafmt and Nailgun

Run provided `setup.sh`, that will install for you both Scalafmt and Nailgun according to [recommended installation instructions](http://scalameta.org/scalafmt/#Installation).

### Optional: Add keybinding

Open `Preferences > Key Bindings` and add:

    {
      "keys": ["super+alt+l"],
      "command": "scala_formatter_format_file",
    }

changing `keys` to any sequence of keys you'd like.

## Usage

Open a Scala file, then open the `Command Palette` and select `ScalaFormatter: Format current file`.

## Scalafmt configuration

The plugin uses (and creates, if missing) `~/.scalafmt.conf`: this file can be used to configure `Scalafmt`.

## Caveats

Very early stages of development, only tested on OSX El Capitan / macOS Sierra.
