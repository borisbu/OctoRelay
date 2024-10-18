import { vi } from "vitest";

export const lodashMock = {
  memoize: vi.fn((fn: () => unknown) => fn),
};
