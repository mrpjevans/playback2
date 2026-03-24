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
- Abbreviations for fast actions (e.g. just 'p' to pause playback)

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
```

- **VLC_SOCKET**: Path to the VLC Unix socket (must match VLC's configuration)
- **PLAYLIST_DIR**: Directory containing `.m3u` playlist files

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

#### PlayBack2 Built-in Commands

| Command | Alias | Arguments | Description |
|---------|-------|-----------|-------------|
| `list` | - | - | List available playlists in the configured directory |
| `load` | `l` | `<name>` | Load a playlist by name (without `.m3u` extension). Clears the current playlist and adds the new one. |
| `run` | `r`, `start` | `<name>` | Load a playlist and immediately start playback |
| `cue` | `c` | - | Seek to the beginning of the current track and pause (ready to play) |
| `restart` | - | - | Restart the current track from the beginning |
| `exit` | `q`, `quit` | - | Exit PlayBack2 (also responds to Ctrl+D) |
| `reboot` | - | - | Reboot the computer |
| `shutdown` | - | - | Shut down the computer |
| `help` | - | Some very basic help |

#### Quick Single-Key Commands

| Key | Alias For | Description |
|-----|-----------|-------------|
| `p` | `pause` | Pause/resume playback |
| `s` | `stop` | Stop playback |

#### VLC Pass-through Commands

Any command not recognized as a built-in PlayBack2 command is automatically sent to VLC. The VLC RC interface supports many commands, including:

| Command | Arguments | Description |
|---------|-----------|-------------|
| `play` | - | Start playback |
| `pause` | - | Pause/resume playback |
| `stop` | - | Stop playback |
| `seek` | `<position>` | Seek to a specific position (in seconds) |
| `clear` | - | Clear the current playlist |
| `add` | `<path>` | Add a file or playlist to the queue (absolute path) |
| `next` | - | Skip to the next item in the playlist |
| `prev` | - | Go to the previous item in the playlist |
| `vol` | `[value]` | Get or set volume level (0-320, where 256 is normal) |
| `atrack` | `[number]` | Get or set the audio track |
| `vtrack` | `[number]` | Get or set the video track |
| `achan` | `[number]` | Get or set the audio channels |
| `info` | - | Display information about the current track |

### Example Session

```
🎥 list
Available playlists:
 - my_playlist
 - another_playlist

🎥 load my_playlist
Loading playlist: /path/to/playlists/my_playlist.m3u
Sending to VLC: clear
OK
Sending to VLC: add /path/to/playlists/my_playlist.m3u
OK
Sending to VLC: stop
OK

🎥 run my_playlist
Loading playlist: /path/to/playlists/my_playlist.m3u
Sending to VLC: play
OK

🎥 vol 200
Sending to VLC: vol 200
OK

🎥 info
Sending to VLC: info
[track information output]

🎥 p
Sending to VLC: pause
OK

🎥 cue
Sending to VLC: seek 0
OK
Sending to VLC: pause
OK

🎥 exit
Closing down
```

### How PlayBack2 Works

PlayBack2 provides a simple command interface that:
1. **Built-in commands** like `list`, `load`, and `run` provide high-level playlist management
2. **Direct VLC commands** can be sent by typing them at the prompt (e.g., `play`, `pause`, `seek 100`, etc.)
3. **Responses from VLC** are displayed after each command

When you load a playlist with `load` or `run`:
- It first clears any existing playlist (`clear`)
- Adds your playlist file (`add /path/to/file.m3u`)
- Stops playback (`stop`)
- For `run`, it immediately starts playback (`play`)

## Troubleshooting

**"Failed to connect to VLC socket"**
- Ensure VLC is running with the RC interface enabled
- Ensure this script has read/write permissions to the socket
- Check that `VLC_SOCKET` in `.env` matches VLC's configuration
- Verify the socket file exists: `ls -la /tmp/vlc.sock`

**"Error listing playlists"**
- Verify `PLAYLIST_DIR` in `.env` is correct
- Check directory permissions: `ls -la <PLAYLIST_DIR>`

## VLC RC Interface Documentation

PlayBack2 communicates with VLC through its RC (Remote Control) interface over a Unix socket. Common VLC commands include:

- **Playback**: `play`, `pause`, `stop`, `next`, `prev`, `seek <seconds>`
- **Volume**: `vol <0-320>` (256 is normal volume)
- **Tracks**: `atrack [number]`, `vtrack [number]`, `strack [number]`
- **Playlist**: `clear`, `add <path>`, `playlist`, `loop`
- **Info**: `info`, `is_playing`, `get_time`, `get_length`

For the complete list of VLC RC commands, consult:
- [VLC RC Interface Documentation](https://www.videolan.org/doc/vlc/latest/html/group__vlc__rc.html)
- [VLC Official Documentation](https://www.videolan.org/doc/)
- Type `help` in the PlayBack2 prompt to see VLC's built-in help

