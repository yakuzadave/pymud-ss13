class AIPlayer:
    """Simple AI player that executes a list of commands."""

    def __init__(self, engine, client_id):
        self.engine = engine
        self.client_id = client_id
        self.outputs = []

    def run(self, commands):
        from engine import action_queue

        for cmd in commands:
            action_queue.next_time.clear()
            out = self.engine.process_command(self.client_id, cmd)
            self.outputs.append((cmd, out))
        return self.outputs
