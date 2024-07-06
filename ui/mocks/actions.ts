import { vi } from "vitest";

export const cancelMock = vi.fn();
export const toggleMock = vi.fn();

vi.mock("../helpers/actions", () => ({
  cancelTask: cancelMock,
  toggleRelay: toggleMock,
}));
