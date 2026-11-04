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

    def process_queue_items(self, max_batch_size: int = 50) -> int:
        """
        Processes pending command packets in bulk batches to reduce lock 
        contention and improve throughput on the game thread.
        """
        batch = []
        
        # Drain items up to the batch limit efficiently
        try:
            while len(batch) < max_batch_size:
                cmd = self.command_queue.get_nowait()
                batch.append(cmd)
        except queue.Empty:
            pass

        if not batch:
            return 0

        # Process the batched commands
        for cmd in batch:
            try:
                self._execute_command(cmd)
            except Exception as e:
                logger.error(f"Failed to execute command ID {cmd.get('id')}: {e}")
            finally:
                self.command_queue.task_done()
                
        return len(batch)

    def _execute_command(self, cmd: dict):
        # Internal execution stub
        logger.debug(f"Executing command ID: {cmd.get('id')}")
