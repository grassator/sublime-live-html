# Sublime Live HTML

Complimentary plugin for [Live HTML](http://kubyshkin.ru/live-html/). Allows for live updates to browser DOM after each keystroke when editing HTML or CSS inside Sublime Text 2 and 3.

## Installation

1. Open Sublime Text
2. Inside applicatin menu go to:
  * on Windows: `Preferences -> Browse Packages`
  * on Mac: `Sublime Text -> Preferences -> Browse Packages`
3. Download and unzip this repository into a folder inside or
   use `git clone` functionality.

## Usage

To enable live editing mode when working on a CSS or HTML file that is a part
of active Live HTML project you can press `Ctrl+Alt+Shift+L`
(`Cmd+Alt+Shift+L` on a Mac) or use `Toggle Live HTML` from command pallete.

If plugin was able to connect to Live HTML server than you will see text
`<LH>` appear in the bottom left corner of Sublime Text window. After that
any change you make will be sent to Live HTML without a need to save the file.

Live editing mode is enabled on per-file basis and can be disabled by using
the same shortcut or command.

## Known Issues

* It's not possible to specify connection port just yet, so it's only possible
to use this plugin with default Live HTML port (55555)
* There is no error when you try to enable live editing mode for file
that is not a part of any Live HTML project
