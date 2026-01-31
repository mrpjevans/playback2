import socket
import cmd

# Hardcodes
vlc_socket = "/Users/pj/vlc.sock"
playlists_dir = "/Users/pj/Code/playback2/playlists"

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

class MyREPL(cmd.Cmd):
    intro = 'Welcome to PlayBack2. Type help or ? to list commands.\n'
    prompt = '🎥 '

    def preloop(self):
        try:
            result = client.connect(vlc_socket)
            print("Connected to VLC")
        except Exception as e:
            print(f"Failed to connect to VLC socket: {e}")
            exit(1)
        return super().preloop()
    
    def do_add(self, arg):
        '''Add a file to play. Specify absolute path.'''
        print("Adding file:", arg)
        client.send(f"add {arg}\n".encode())
        client.send(b"stop\n")
        self.ok()

    def do_pl(self, arg):
        '''Load playlist from default folder by name (without .m3u extension)'''
        playlist_path = f"{playlists_dir}/{arg}.m3u"
        print("Loading playlist:", playlist_path)
        client.send(b"clear\n")
        client.send(f"add {playlist_path}\n".encode())
        client.send(b"stop\n")
        self.ok()

    def do_run(self, arg):
        '''Run the current playlist'''
        self.do_pl(arg)
        self.do_play(arg)
    
    def do_restart(self, arg):
        '''Restart the current track from the beginning'''
        client.send(b"seek 0\n")

    def do_cue(self, arg):
        '''Cue to the beginning of the current track and stop'''
        client.send(b"seek 0\n")
        client.send(b"stop\n")
        
    def do_play(self, arg):
        '''Play the current track'''
        self.match("play")
        
    def do_pause(self, arg):
        '''Toggle pause/play'''
        self.match("pause")

    def do_stop(self, arg):
        '''Stop playback'''
        self.match("stop")

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
        self.ok()

    def do_exit(self, arg):
        '''Exit the REPL'''
        client.close()
        print("Closing down")
        return True  # Returning True exits the loop
    
    def match(self,cmd):
        client.send(f"{cmd}\n".encode())
        self.ok()

    def ok(self):
        print("OK\n")

    # Aliases
    do_pau = do_pause
    do_p = do_pause
    do_quit = do_exit
    do_EOF = do_exit  # Handle Ctrl+D

if __name__ == '__main__':
    MyREPL().cmdloop()