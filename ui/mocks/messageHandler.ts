import { vi } from "vitest";

export const handlerMock = vi.fn();

vi.mock("../model/messageHandler", () => ({
  makeMessageHandler: vi.fn(() => handlerMock),
}));
