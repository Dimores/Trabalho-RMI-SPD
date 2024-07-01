import Pyro4
import uuid

def main():
    client_id = str(uuid.uuid4())
    video_server = Pyro4.Proxy("PYRONAME:example.videoserver")
    
    while True:
        print("Options: play, pause, resume, stop, exit")
        command = input("Enter command: ").strip().lower()
        
        if command == "play":
            video_path = input("Enter video path: ").strip()
            response = video_server.play_video(video_path, client_id)
            print(response)
        elif command == "pause":
            response = video_server.pause_video(client_id)
            print(response)
        elif command == "resume":
            response = video_server.resume_video(client_id)
            print(response)
        elif command == "stop":
            response = video_server.stop_video(client_id)
            print(response)
        elif command == "exit":
            response = video_server.stop_video(client_id)
            print(response)
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
