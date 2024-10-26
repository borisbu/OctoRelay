import type { Mock } from "vitest";

export const elementMock: Record<
  | "toggle"
  | "html"
  | "off"
  | "on"
  | "find"
  | "text"
  | "modal"
  | "is"
  | "popover"
  | "tooltip",
  Mock
> = {
  toggle: vi.fn(() => elementMock),
  html: vi.fn(() => elementMock),
  off: vi.fn(() => elementMock),
  on: vi.fn(() => elementMock),
  find: vi.fn(() => elementMock),
  text: vi.fn(() => elementMock),
  modal: vi.fn(() => elementMock),
  is: vi.fn(() => elementMock),
  tooltip: vi.fn(() => elementMock),
  popover: vi.fn(() => elementMock),
};

export const jQueryMock = vi.fn((subject: string | (() => void)) => {
  if (typeof subject === "function") {
    return subject();
  }
  return elementMock;
});
