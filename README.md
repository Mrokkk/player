# player
Branch | Build | Coverage
------ | ----- | --------
master | [![Build Status](https://travis-ci.org/Mrokkk/player.svg?branch=master)](https://travis-ci.org/Mrokkk/player) | [![codecov](https://codecov.io/gh/Mrokkk/player/branch/master/graph/badge.svg)](https://codecov.io/gh/Mrokkk/player)
devel | [![Build Status](https://travis-ci.org/Mrokkk/player.svg?branch=devel)](https://travis-ci.org/Mrokkk/player) | [![codecov](https://codecov.io/gh/Mrokkk/player/branch/devel/graph/badge.svg)](https://codecov.io/gh/Mrokkk/player)

## Usage
### Commands list
command                      | action
---------------------------  | ----------------------------------
:add\_bookmark \<path\>      | create a bookmark for a \<path\>
:add\_to\_playlist \<path\>  | add file(s) from \<path\>
:change\_dir \<path\>        | change dir in the file browser dir to \<path\>
:clear\_playlist             | clear the playlist
:e                           | alias for add\_to\_playlist
:error \<string\>            | print an error
:get \<key\>                 | read the value for the \<key\>
:info \<string\>             | print an info
:load\_playlist \<path\>     | load playlist file from \<path\>
:next                        | play next track
:pause                       | toggle pause
:prev                        | play previous track
:quit / qa / q               | exit the program
:replace\_playlist \<path\>  | replace playlist with the file(s) from the \<path\>
:save\_playlist \<path\>     | save current playlist to the \<path\>
:seek \<time\>               |
:set \<key\> \<value\>       | set \<key\> to \<value\>
:stop                        | stop current track
:switch\_panes               | switch between file browser and playlist
:toggle\_pane\_view          | show alterative view

### Key mapping
key                         | command called
--------------------------- | ----------------------------------
h                           | :seek -10
l                           | :seek +10
H                           | :seek -60
L                           | :seek +60
space                       | :pause
\[                          | :set volume -10
\]                          | :set volume +10

### Config
Configuration file should be located in the one of the following locations: `~/.config/player/config.json` or `~/.config/player/config.yml`. See https://github.com/Mrokkk/player/blob/master/example_config.json or https://github.com/Mrokkk/player/blob/master/example_config.yml for examples.
