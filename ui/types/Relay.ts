export interface Task {
  deadline: number;
  owner: string;
  target: boolean;
}

export interface Relay<U extends null | Task = null | Task> {
  active: boolean;
  confirm_off: boolean;
  icon_html: string;
  label_text: string;
  relay_pin: number;
  inverted_output: boolean;
  relay_state: boolean;
  upcoming: U;
}

export type RelayHavingTask = Relay<Task>;
