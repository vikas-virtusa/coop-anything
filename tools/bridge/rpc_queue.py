import queue
import logging

logger = logging.getLogger("CoopBridge")

class RpcQueueHandler:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.is_running = False

    def enqueue_command(self, command: dict):
        """Adds an incoming RPC packet to the processing queue."""
        self.command_queue.put(command)

    def process_queue_items(self) -> int:
        """Processes pending command packets sequentially from the queue."""
        processed_count = 0
        
        # Clean, functional implementation processing one item at a time
        while not self.command_queue.empty():
            try:
                cmd = self.command_queue.get_nowait()
                self._execute_command(cmd)
                processed_count += 1
                self.command_queue.task_done()
            except queue.Empty:
                break
                
        return processed_count

    def _execute_command(self, cmd: dict):
        # Internal execution stub
        logger.debug(f"Executing command ID: {cmd.get('id')}")
