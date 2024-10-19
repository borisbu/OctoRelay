export const disposerMock = vi.fn();
export const countdownMock = vi.fn(() => disposerMock);
export const deadlineMock = vi.fn(() => "sample deadline");

vi.mock("../helpers/countdown", () => ({
  setCountdown: countdownMock,
  formatDeadline: deadlineMock,
}));
