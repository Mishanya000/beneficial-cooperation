from threading import Lock


class DialogState:
    def __init__(self):
        self._states: dict[tuple[int, int], dict] = {}
        self._lock = Lock()

    def set(self, chat_id: int, user_id: int, state: dict) -> None:
        with self._lock:
            self._states[(chat_id, user_id)] = state

    def get(self, chat_id: int, user_id: int) -> dict | None:
        with self._lock:
            return self._states.get((chat_id, user_id))

    def clear(self, chat_id: int, user_id: int) -> None:
        with self._lock:
            self._states.pop((chat_id, user_id), None)


dialog_state = DialogState()