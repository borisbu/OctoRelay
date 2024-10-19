export const lodashMock = {
  memoize: vi.fn(
    (fn: () => unknown, resolver: () => unknown) => resolver() && fn,
  ),
};
