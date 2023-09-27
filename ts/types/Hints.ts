import type { Relay } from "./Relay";

export interface Hint {
  control: JQuery;
  key: string;
  relay: Relay;
}

export interface PopoverItem {
  cancelId: string;
  timeTagId: string;
  deadline: number;
  cancel: () => JQuery.Promise<any>;
}

export interface AddPopoverProps {
  target: JQuery;
  title: string;
  content: string[];
  navbar: JQuery;
  closerId: string;
  items: PopoverItem[];
  originalSubject: string;
}
