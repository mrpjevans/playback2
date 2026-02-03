import os
import socket
import cmd

root_dir = os.path.dirname(os.path.abspath(__file__))

# Config and defaults
config = {
    'VLC_SOCKET': "/tmp/vlc.sock" if 'VLC_SOCKET' not in os.environ else os.environ['VLC_SOCKET'],
    'PLAYLIST_DIR': f"{root_dir}/playlists" if 'PLAYLIST_DIR' not in os.environ else os.environ['PLAYLIST_DIR'],
    'DEBUG': '0' if 'DEBUG' not in os.environ else os.environ['DEBUG'],
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
            result = client.connect(config['VLC_SOCKET'])
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
        print()

    def do_add(self, arg):
        '''Add a file to play. Specify absolute path.'''
        print("Adding file:", arg)
        client.send(f"add {arg}\n".encode())
        client.send(b"stop\n")

    def do_load(self, arg):
        '''Load playlist from default folder by name (without .m3u extension)'''
        playlist_path = f"{config['PLAYLIST_DIR']}/{arg}.m3u"
        print("Loading playlist:", playlist_path)
        client.send(b"clear\n")
        client.send(f"add {playlist_path}\n".encode())
        client.send(b"stop\n")

    def do_run(self, arg):
        '''Load and run the specified playlist'''
        self.do_load(arg)
        self.do_play(arg)
    
    def do_restart(self, arg):
        '''Restart the current track from the beginning'''
        client.send(b"seek 0\n")

    def do_cue(self, arg):
        '''Cue to the beginning of the current track and stop'''
        client.send(b"stop\n")
        client.send(b"seek 0\n")
                
    def do_play(self, arg):
        '''Play the current track'''
        self.match("play")
        
    def do_pause(self, arg):
        '''Toggle pause/play'''
        self.match("pause")

    def do_stop(self, arg):
        '''Stop playback'''
        self.match("stop")

    def do_next(self, arg):
        '''Next track'''
        self.match("next")

    def do_prev(self, arg):
        '''Previous track'''
        self.match("prev")

    def do_clear(self, arg):
        '''Clear the current playlist'''
        self.match("clear")

    def do_ff(self, arg):
        '''Fast forward the current track'''
        self.match("fastforward")
                   
    def do_rw(self, arg):
        '''Rewind the current track'''
        self.match("rewind")
    
    def do_info(self, arg):
        '''Get info about the current track'''
        self.match("info")
        print(client.recv(4096)) 
    
    def do_vol(self, arg):
        '''Get or set volume. Usage: vol [value]'''
        if arg == '':
            self.match(b"volume\n")
        else:
            client.send(f"volume {arg}\n".encode())
        print(client.recv(4096)) 

    def do_atrack(self, arg):
        '''Get or set audio track. Usage: atrack [value]'''
        if arg == '':
            self.match("atrack")
        else:
            client.send(f"atrack {arg}\n".encode())
        print(client.recv(4096))

    def do_vtrack(self, arg):
        '''Get or set video track. Usage: vtrack [value]'''
        if arg == '':
            self.match("vtrack")
        else:
            client.send(f"vtrack {arg}\n".encode())
        print(client.recv(4096))
    
    def do_pass(self, arg):
        '''Send a raw command to VLC'''
        client.send(f"{arg}\n".encode())  
        print(client.recv(4096)) 

    def do_exit(self, arg):
        '''Exit the REPL'''
        client.close()
        print("Closing down")
        return True  # Returning True exits the loop
    
    def match(self,cmd):
        client.send(f"{cmd}\n".encode())
        if config['DEBUG'] == '1':
            print(client.recv(4096))

    def postcmd(self, stop, line):
        print("OK\n")
        return stop

    # Aliases
    do_start = do_run
    do_quit = do_exit
    do_EOF = do_exit  # Handle Ctrl+D

    # Abbreviations
    do_loa = do_load
    do_res = do_restart
    do_pla = do_play
    do_pau = do_pause
    do_sto = do_stop
    do_nex = do_next
    do_pre = do_prev
    do_cle = do_clear
    do_inf = do_info
    do_atr = do_atrack
    do_vtr = do_vtrack
    do_pas = do_pass
    do_exi = do_exit
    do_qui = do_exit
    do_sta = do_run
    
    # 1 Char
    do_l = do_load
    do_c = do_cue
    do_r = do_run
    do_p = do_pause
    do_s = do_stop
    do_q = do_exit

if __name__ == '__main__':
    MyREPL().cmdloop()