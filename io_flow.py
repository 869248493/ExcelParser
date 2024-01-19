from errors import io_not_found


class IOFlow:
    def __init__(self):
        self.io_flow_l = []
        self.current_io_idx = 0
        self.previous_state = []

    def reg(self, io):
        self.io_flow_l.append(io)

    def current(self):
        return self.io_flow_l[self.current_io_idx]

    def set_next(self):
        self.previous_state.append(self.current_io_idx)
        self.current_io_idx = (1 + self.current_io_idx) % len(self.io_flow_l)

    def set_previous(self):
        # self.current_io_idx = (self.current_io_idx - 1) % len(self.io_flow_l)
        p_s = self.previous_state.pop()
        self.current_io_idx = p_s

    def go_to(self, name):
        self.previous_state.append(self.current_io_idx)
        for i in range(len(self.io_flow_l)):
            if self.io_flow_l[i].name == name:
                self.current_io_idx = i
                # return self.current()
                return
        io_not_found()

