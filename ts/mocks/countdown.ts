export const disposerMock = jest.fn();
export const countdownMock = jest.fn(() => disposerMock);
export const deadlineMock = jest.fn();

jest.mock("../helpers/countdown", () => ({
  setCountdown: countdownMock,
  formatDeadline: deadlineMock,
}));
