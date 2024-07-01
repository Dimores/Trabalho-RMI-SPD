import Pyro4

def main():
    video_server = Pyro4.Proxy("PYRONAME:example.videoserver")
    
    while True:
        print("Options: play <remote_id>, pause <remote_id>, resume <remote_id>, stop <remote_id>, exit")
        command = input("Enter command: ").strip().lower().split()
        
        if len(command) < 2:
            print("Invalid command")
            continue
        
        action, remote_id = command[0], command[1]

        remote_name = f"example.{remote_id}"
        
        if action == "play":
            response = video_server.play_video(remote_name)
            print(response)
        elif action == "pause":
            response = video_server.pause_video(remote_name)
            print(response)
        elif action == "resume":
            response = video_server.resume_video(remote_name)
            print(response)
        elif action == "stop":
            response = video_server.stop_video(remote_name)
            print(response)
        elif action == "exit":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
