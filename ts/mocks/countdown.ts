export const disposerMock = jest.fn();
export const countdownMock = jest.fn(() => disposerMock);

jest.mock("../helpers/countdown", () => ({
  setCountdown: countdownMock,
}));
