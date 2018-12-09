# Scalafmt for Sublime Text 3

Minimal Sublime Text 3 package to format Scala files, powered by [Scalafmt](http://[scalameta.org/scalafmt) and [Nailgun](https://github.com/martylamb/nailgun).

## Installation

### Step 1: Install this package

#### ... with [Package Control](https://packagecontrol.io/)

- open the Command Palette
- select `Package Control: Install Package`
- select `Scalafmt`

#### ... or manually

Clone this repository in `~/Library/Application Support/Sublime Text 3/Packages/`.

### Step 2: Install Scalafmt and Nailgun

Run provided `setup.sh`, that will install for you both Scalafmt and Nailgun according to [recommended installation instructions](http://scalameta.org/scalafmt/#Installation).

### Optional: Add keybinding

Open `Preferences > Key Bindings` and add:

    {
      "keys": ["super+alt+l"],
      "command": "scalafmt_format_file",
    }

changing `keys` to any sequence of keys you'd like.

## Usage

Open a Scala file, then open the `Command Palette` and select `Scalafmt: Format current file`.

## Customize format style

This package uses (and creates, if missing) `~/.scalafmt.conf`: this file can be used to influence how `scalafmt` formats your code.

## Caveats

Only developed and tested on macOS.
