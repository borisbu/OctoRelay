import type { Relay, RelayHavingTask } from "../types/Relay";

export const hasUpcomingTask = (relay: Relay): relay is RelayHavingTask =>
  relay.upcoming ? relay.upcoming.target !== relay.relay_state : false;
