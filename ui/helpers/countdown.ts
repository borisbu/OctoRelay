/** @desc Creating Intl.NumberFormat is relatively slow, therefore using memoize() per set of arguments */
const createNumberFormat = _.memoize(
  (
    ...[requested, options]: Parameters<typeof Intl.NumberFormat>
  ): Pick<Intl.NumberFormat, "format"> => {
    const locales = [requested];
    if (typeof requested === "string" && requested.includes("_")) {
      locales.push(requested.replaceAll("_", "-"));
    }
    locales.push(undefined);
    for (const locale of locales) {
      try {
        return new Intl.NumberFormat(locale, options);
      } catch (error) {
        console.warn(`Failed to format time using ${locale} locale`, error);
      }
    }
    const format = (value: number) =>
      `${value} ${options?.unit}${value === 1 ? "" : "s"}`;
    return { format };
  },
  (...[locale, options]: Parameters<typeof Intl.NumberFormat>) =>
    [locale, options?.unit, options?.maximumFractionDigits].join("|"),
);

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
  const formattedTimeLeft = createNumberFormat(LOCALE, {
    style: "unit",
    unitDisplay: "long",
    minimumFractionDigits: isLastMinute ? 1 : 0,
    maximumFractionDigits: isLastMinute ? 1 : 0,
    unit,
  }).format(Math.max(0, timeLeft));
  return `in ${formattedTimeLeft}`;
};

export const getCountdownDelay = (deadline: number): number =>
  deadline - Date.now() > 120000 ? 60000 : 1000;

export const setCountdown = (
  selector: JQuery,
  deadline: number,
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
