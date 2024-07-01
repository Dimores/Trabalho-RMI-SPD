import Pyro4

# Obter a URI do VideoPlayer registrado no servidor de nomes
def get_video_player_uri(machine_name):
    ns = Pyro4.locateNS(host='192.168.0.5', port=9090)  # Atualize com o IP do seu servidor de nomes
    uri = ns.lookup(f"example.videoplayer.{machine_name}")
    return uri

# Conectar-se ao VideoPlayer remoto e enviar comandos
def control_video_player(uri):
    player = Pyro4.Proxy(uri)
    print(f"Conectado ao VideoPlayer em {uri}")

    while True:
        command = input(f"Digite o comando para {uri} (play, pause, stop, exit): ").strip().lower()
        if command == "exit":
            break
        elif command in ["play", "pause", "stop"]:
            getattr(player, command + "_video")()
        else:
            print("Comando inválido.")

if __name__ == "__main__":
    # Selecionar a máquina para controlar
    machine_name = "machine1"  # Altere para o nome da máquina que você quer controlar

    # Obter a URI do VideoPlayer na máquina selecionada
    uri = get_video_player_uri(machine_name)

    if uri:
        control_video_player(uri)
    else:
        print(f"URI para {machine_name} não encontrada no servidor de nomes.")
