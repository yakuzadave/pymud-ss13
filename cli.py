import argparse
import logging
import sys
from mudpy_interface import MudpyInterface
import integration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cli")

def main():
    parser = argparse.ArgumentParser(description="PyMUD-SS13 text client")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    interface = MudpyInterface(args.config)
    engine_integration = integration.create_integration(interface)

    client_id = "cli_user"
    interface.connect_client(client_id)

    print("Welcome to PyMUD-SS13 CLI. Type 'quit' to exit.")

    try:
        while True:
            try:
                command = input("> ")
            except EOFError:
                break
            if not command:
                continue
            if command.lower() in {"quit", "exit"}:
                break
            response = engine_integration.process_command(client_id, command)
            print(response)
    finally:
        interface.disconnect_client(client_id)
        interface.shutdown()

if __name__ == "__main__":
    main()
