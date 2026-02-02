# PlayBack2

This is a simplified command line interface for VLC. It is intended to be used over SSH for fast control of a video playback
system. I created this as for my use case a web UI or touch-screen interface was not prefereable to learning a few simple commands.

## Features

- Load and manage playlists
- Control playback (play, pause, stop, seek)
- Manage audio and video tracks
- Volume control
- Fast forward/rewind
- Send raw commands to VLC
- Debug mode for troubleshooting
- Lots of abbreviations for fast actions (e.g. just 'p' to pause playback)

## Setup

### 1. Configure VLC to Use Unix Socket Interface

VLC must be configured with the RC (remote control) interface enabled over a Unix socket.

**macOS:**
```bash
# Create VLC configuration directory
mkdir -p ~/Library/Application\ Support/VLC

# Edit VLC's lua interface configuration
# Add or modify ~/.config/vlc/lua/rc.lua to enable the socket interface
```

**Linux:**
```bash
# Edit VLC's lua interface configuration
# Add or modify ~/.config/vlc/lua/rc.lua
```

Add the following to your VLC configuration (or use VLC's preferences UI):
- Go to **Tools > Preferences > Interface > Control interfaces**
- Enable **RC interface**
- Set the socket path to `/tmp/vlc.sock` (or your preferred location)
- Set Fake TTY to true

Alternatively, start VLC from command line with:
```bash
vlc --extraintf=luarc --lua-config='rc={socket="/tmp/vlc.sock"}'
```

### 2. Install Dependencies

Ensure Python 3.6+ is installed. No external dependencies are required.

### 3. Configure PlayBack2

Copy the example environment file and customize it:
```bash
cp repl/.env.example repl/.env
```

Edit `repl/.env` with your settings:
```
VLC_SOCKET=/tmp/vlc.sock
PLAYLIST_DIR=/path/to/your/playlists
DEBUG=0
```

- **VLC_SOCKET**: Path to the VLC Unix socket (must match VLC's configuration)
- **PLAYLIST_DIR**: Directory containing `.m3u` playlist files
- **DEBUG**: Set to `1` to see VLC responses, `0` to hide them

### 4. Create Playlists

Add M3U playlists to your `PLAYLIST_DIR`:
```
playlists/
  - my_playlist.m3u
  - another_playlist.m3u
```

## Usage

Start the REPL:
```bash
python3 repl/pb2repl.py
```

You'll see the prompt `🎥 ` ready for commands.

### Available Commands

| Command | Short | Description |
|---------|-------|-------------|
| `load <name>` | `l` | Load playlist by name (without .m3u) |
| `list` | | List available playlists |
| `run <name> / start <name>` | `r` | Load and play a playlist |
| `play` | `p` | Play current track |
| `pause` | | Toggle pause/play |
| `stop` | `s` | Stop playback |
| `cue` | `c` | Seek to start and stop |
| `restart` | | Restart current track |
| `clear` | | Clear current playlist |
| `ff` | | Fast forward |
| `rw` | | Rewind |
| `vol [value]` | | Get or set volume (0-320) |
| `atrack [value]` | | Get or set audio track |
| `vtrack [value]` | | Get or set video track |
| `info` | | Show current track info |
| `add <path>` | | Add file to playlist (absolute path) |
| `pass <cmd>` | | Send raw command to VLC |
| `exit / quit` | `q` | Exit the REPL |
| `help [cmd]` | `?` | Show help |

All commands can be invoked using just the first three letters (e.g. `res` for `restart`).

### Example Session

```
🎥 list
Available playlists:
 - my_playlist
 - another_playlist

🎥 load my_playlist
Loading playlist: /path/to/playlists/my_playlist.m3u
OK

🎥 play
OK

🎥 vol 200
OK

🎥 info
[track information output]

🎥 pause
OK

🎥 exit
Closing down
```

## Troubleshooting

**"Failed to connect to VLC socket"**
- Ensure VLC is running with the RC interface enabled
- Ensure this script has read/write permissions to the socket
- Check that `VLC_SOCKET` in `.env` matches VLC's configuration
- Verify the socket file exists: `ls -la /tmp/vlc.sock`

**"Error listing playlists"**
- Verify `PLAYLIST_DIR` in `.env` is correct
- Check directory permissions: `ls -la <PLAYLIST_DIR>`

**Enable Debug Mode**
- Set `DEBUG=1` in `.env` to see VLC's raw responses
- Useful for understanding VLC command syntax

## VLC RC Interface Documentation

For more information on VLC RC commands, see:
- [VLC Documentation](https://www.videolan.org/doc/)
- VLC embedded help: Type `help` in the RC interface
