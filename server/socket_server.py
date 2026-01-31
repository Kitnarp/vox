import socket
import threading
import json

from config.logger_config import server_logger
from config.config import SERVER_HOST, SERVER_PORT, MODEL_PATH

from voicecore.voice_manager import VoiceManager



# Initialize VoiceManager
vm = VoiceManager(MODEL_PATH)

# --- Command Dispatcher ---
def dispatch_command(command: dict) -> str:
    """Dispatch a parsed command dict to VoiceManager."""
    action = command.get("action")
    args = command.get("args", {})
    server_logger.debug(f"dispatching_command with action:{action} and args: {args}")
    try:
        if action == "load":
            server_logger.debug("Executing action: \"load\"")
            vm.load_model()
        elif action == "unload":
            server_logger.debug("Executing action: \"unload\"")
            vm.unload_model()
        elif action == "start":
            server_logger.debug("Executing action: \"start\"")
            vm.start_listening()
        elif action == "stop":
            server_logger.debug("Executing action: \"stop\"")
            vm.stop_listening()
        elif action == "device":
            server_logger.debug("Executing action: \"device\"")
            vm.set_device(int(args.get("id")))
        elif action == "reload":
            server_logger.debug("Executing action: \"reload\"")
            vm.reload_commands()
        elif action == "hello":
            server_logger.debug("Executing action: \"hello\"")
            return "Hello from VoiceServer!"
        else:
            server_logger.info(f"Unknown action: {action}")
            return f"Unknown action: {action}"
        return "OK"
    except Exception as e:
        server_logger.error(f"Error executing action:'{action}': {e}")
        return f"ERROR: {e}"

# --- Client Handler ---
def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode().strip()
        if not data:
            return

        server_logger.info(f"Received from {addr}: {data}")

        # Expect JSON messages for clarity
        try:
            command = json.loads(data)
        except json.JSONDecodeError:
            server_logger.error("Invalid JSON")
            conn.sendall(b"ERROR: Invalid JSON")
            return

        response = dispatch_command(command)
        conn.sendall(response.encode())
    finally:
        conn.close()

# --- Server Loop ---
def server_loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    server_logger.info(f"VoiceManager server running on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    server_loop()