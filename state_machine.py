from event_to_string import event_to_string


class StateMachine:
    def __init__(self,start_state,rules):
        self.current_state = start_state
        self.current_state.enter(('start',0))
        self.rules = rules

    def update(self):
        self.current_state.do()

    def draw(self):
        self.current_state.draw()

    def handle_state_events(self,state_event):
        for check_event in self.rules[self.current_state].keys():
            if check_event(state_event):
                self.next_state = self.rules[self.current_state][check_event]
                self.current_state.exit(state_event)
                self.next_state.enter(state_event)
                print(f'{self.current_state.__class__.__name__} == {event_to_string(state_event)} ==> {self.next_state.__class__.__name__}')
                self.current_state = self.next_state
        print(f'처리되지 않은 이벤트 {event_to_string(state_event)} 가 발생')
