import os
import socket
import cmd

root_dir = os.path.dirname(os.path.abspath(__file__))

# Config and defaults
config = {
    'VLC_SOCKET': "/tmp/vlc.sock" if 'VLC_SOCKET' not in os.environ else os.environ['VLC_SOCKET'],
    'PLAYLIST_DIR': f"{root_dir}/playlists" if 'PLAYLIST_DIR' not in os.environ else os.environ['PLAYLIST_DIR'],
}

# Minimal dotenv loader
env_file = os.path.join(root_dir, ".env")

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            config[key] = value

# Prepare connection to VLC
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

class MyREPL(cmd.Cmd):
    intro = 'Welcome to PlayBack2. Type help or ? to list commands.\n'
    prompt = '🎥 '

    # Connect to VLC socket before starting the loop
    def preloop(self):
        try:
            client.connect(config['VLC_SOCKET'])
            client.settimeout(0.2)  # Set socket timeout to 1 second
            print("Connected to VLC")
        except Exception as e:
            print(f"Failed to connect to VLC socket: {e}")
            exit(1)
        return super().preloop()
        
    def do_list(self, arg):
        '''List available playlists in the default folder'''
        playlist_dir = config['PLAYLIST_DIR']
        try:
            files = os.listdir(playlist_dir)
            playlists = [f[:-4] for f in files if f.endswith('.m3u')]
            print("Available playlists:")
            for pl in playlists:
                print(" -", pl)
        except Exception as e:
            print(f"Error listing playlists: {e}")

    def do_load(self, arg):
        '''Load playlist from default folder by name (without .m3u extension)'''
        playlist_path = f"{config['PLAYLIST_DIR']}/{arg}.m3u"
        if not os.path.exists(playlist_path):
            print(f"Playlist not found: {playlist_path}")
            return
        print("Loading playlist:", playlist_path)
        client.send(b"clear\n")
        client.send(f"add {playlist_path}\n".encode())
        client.send(b"stop\n")

    def do_run(self, arg):
        '''Load and run the specified playlist'''
        self.do_load(arg)
        self.default("play")
    
    def do_restart(self, arg):
        '''Restart the current track from the beginning'''
        client.send(b"seek 0\n")

    def do_cue(self, arg):
        '''Cue to the beginning of the current track and stop'''
        client.send(b"seek 0\n")
        client.send(b"pause\n")

    def do_help(self, arg):
        '''Display help from help.txt'''
        help_file = os.path.join(root_dir, "help.txt")
        if not os.path.exists(help_file):
            print(f"Help file not found: {help_file}")
            return
        try:
            with open(help_file) as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading help file: {e}")
    
    def default(self, line):
        '''Send unknown commands directly to VLC'''
        client.send(f"{line}\n".encode())
        
    def do_exit(self, arg):
        '''Exit the REPL'''
        client.close()
        print("Closing down")
        return True  # Returning True exits the loop
                
    def postcmd(self, stop, line):
        if stop:  # Exit was called
            return True
        self.get_response()
        print("")
        return stop
    
    def do_reboot(self, arg):
        '''Reboot the computer'''
        print("Rebooting the computer...")
        os.system("sudo reboot")

    def do_shutdown(self, arg):
        '''Shutdown the computer'''
        print("Shutting down the computer...")
        os.system("sudo shutdown now")

    def get_response(self):
        buffer = bytearray()
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                buffer.extend(data)
        except socket.timeout:
            pass  # Timeout is expected when no more data is available
        
        result = buffer.decode().strip()
        print(result)
    
    # Aliases
    do_start = do_run
    do_quit = do_exit
    do_EOF = do_exit  # Handle Ctrl+D
   
    # 1 Char
    def do_p(self, arg):
        '''Pause the current track'''
        client.send(b"pause\n")
    def do_s(self, arg):
        '''Stop playback'''
        client.send(b"stop\n")

    do_l = do_load
    do_c = do_cue
    do_r = do_run
    do_q = do_exit

if __name__ == '__main__':
    MyREPL().cmdloop()