export const formatDeadline = (time: number): string => {
  let unit: "second" | "minute" | "hour" = "second";
  let timeLeft = (time - Date.now()) / 1000;
  if (timeLeft >= 60) {
    timeLeft /= 60;
    unit = "minute";
  }
  if (timeLeft >= 60) {
    timeLeft /= 60;
    unit = "hour";
  }
  const isLastMinute = unit === "minute" && timeLeft < 2;
  const formattedTimeLeft = new Intl.NumberFormat(LOCALE, {
    style: "unit",
    unitDisplay: "long",
    minimumFractionDigits: isLastMinute ? 1 : 0,
    maximumFractionDigits: isLastMinute ? 1 : 0,
    unit,
  }).format(Math.max(0, timeLeft));
  return `in ${formattedTimeLeft}`;
};

const getCountdownDelay = (deadline: number): number =>
  deadline - Date.now() > 120000 ? 60000 : 1000;

export const setCountdown = (
  selector: JQuery,
  deadline: number
): (() => void) => {
  const delay = getCountdownDelay(deadline);
  let disposer: () => void;
  const interval = setInterval(() => {
    const isVisible = selector.is(":visible");
    if (!isVisible) {
      return disposer();
    }
    selector.text(formatDeadline(deadline));
    const nextDelay = getCountdownDelay(deadline);
    if (nextDelay !== delay) {
      disposer();
      disposer = setCountdown(selector, deadline); // reset with new interval
    }
  }, delay);
  disposer = () => clearInterval(interval);
  return disposer;
};
