import type { Hint, PopoverItem } from "../types/Hints";
import { closeBtnHTML, closeBtnId } from "./const";
import { formatDeadline, setCountdown } from "./countdown";
import { hasUpcomingTask } from "./narrowing";
import { cancelTask } from "./actions";

interface AddPopoverProps {
  target: JQuery;
  title: string;
  content: string[];
  navbar: JQuery;
  items: PopoverItem[];
  originalSubject: string;
}

export const clearHints = (btn: JQuery) =>
  btn.tooltip("destroy").popover("destroy");

const addTooltip = (btn: JQuery, text: string) =>
  btn.tooltip({ placement: "bottom", title: text });

const addPopover = ({
  target,
  title,
  content,
  navbar,
  items,
  originalSubject,
}: AddPopoverProps) => {
  target
    .popover({
      title,
      html: true,
      animation: false,
      placement: "bottom",
      trigger: "manual",
      content: content.join(""),
    })
    .popover("show");
  const closeBtn = navbar.find(`#${closeBtnId}`);
  const countdownDisposers = items.map(
    ({ cancelId, timeTagId, deadline, cancel }) => {
      const cancelBtn = navbar.find(`#${cancelId}`);
      cancelBtn.on("click", cancel);
      const timeTag = navbar.find(`#${timeTagId}`);
      return setCountdown(timeTag, deadline);
    }
  );
  closeBtn.on("click", () => {
    for (const disposer of countdownDisposers) {
      disposer();
    }
    closeBtn.off("click");
    addTooltip(clearHints(target), originalSubject);
  });
};

const compareDeadlines = (a: Hint, b: Hint): number =>
  (a.relay.upcoming?.deadline || 0) - (b.relay.upcoming?.deadline || 0);

export const showHints = ({
  hints,
  navbar,
}: {
  hints: Hint[];
  navbar: JQuery;
}) => {
  const hasMultipleTasks =
    hints.filter(({ relay }) => hasUpcomingTask(relay)).length > 1;
  hints.sort(compareDeadlines);
  let title = "";
  let content: string[] = [];
  let target: JQuery | undefined = undefined;
  let originalSubject = "";
  const items: PopoverItem[] = [];
  for (const { key, relay, control } of hints) {
    const isRelayHavingTask = hasUpcomingTask(relay);
    if (!isRelayHavingTask || target) {
      addTooltip(control, relay.label_text);
    }
    if (!isRelayHavingTask) {
      continue;
    }
    const { upcoming, label_text: subject } = relay;
    const dateObj = new Date(upcoming.deadline);
    const dateISO = dateObj.toISOString();
    const dateLocalized = dateObj.toLocaleString();
    const timeLeft = formatDeadline(upcoming.deadline);
    const targetState = upcoming.target ? "ON" : "OFF";
    const [cancelId, timeTagId] = ["cancel-btn", "time-tag"].map(
      (prefix) => `${prefix}-${key}`
    );
    items.push({
      cancelId,
      timeTagId,
      deadline: upcoming.deadline,
      cancel: () => cancelTask(key, upcoming),
    });
    target = target || control;
    originalSubject = originalSubject || subject;
    const upcomingHTML = `${subject} goes <span class="label">${targetState}</span>`;
    const timeHTML = `<time id="${timeTagId}" datetime="${dateISO}" title="${dateLocalized}">${timeLeft}</time>`;
    const cancelHTML = `<button id="${cancelId}" class="btn btn-mini" type="button">Cancel</button>`;
    title = hasMultipleTasks
      ? `<span>Several relay switches ahead</span>${closeBtnHTML}`
      : `<span>${upcomingHTML}</span>${closeBtnHTML}`;
    content.push(
      hasMultipleTasks
        ? `<div><span>${upcomingHTML} ${timeHTML}</span>${cancelHTML}</div>`
        : `<div>${timeHTML}${cancelHTML}</div>`
    );
  }
  if (target) {
    addPopover({
      target,
      navbar,
      originalSubject,
      title,
      content,
      items,
    });
  }
};
