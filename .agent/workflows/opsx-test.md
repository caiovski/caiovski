---
description: Achieve 100% test coverage — Stmts, Branch, Funcs, Lines — without touching any UI or application code
---

# Absolute Rule: 100% Test Coverage — Zero Tolerance, Zero Exceptions

This workflow governs the AI agent's behavior during any test coverage task. The goal is to reach **100% across all four Jest coverage metrics** (`% Stmts`, `% Branch`, `% Funcs`, `% Lines`) through writing or fixing tests only. **No application code, no UI changes, no exceptions.**

---

## The Mandate

> **1. All tests MUST PASS.** A failing test is an immediate failure of the session. If tests fail, you must fix them.
> **2. Coverage must be 100% on all four axes.** This is not a goal. This is a hard constraint.

| Metric    | Required |
|-----------|----------|
| % Stmts   | 100%     |
| % Branch  | 100%     |
| % Funcs   | 100%     |
| % Lines   | 100%     |

If any metric is below 100%, the session is **not complete**. There is no partial success.

---

## The Absolute Prohibition

> ⛔ **IT IS STRICTLY AND UNCONDITIONALLY FORBIDDEN to modify any application or UI code.**

This includes, but is not limited to:

- Animations, transitions, or motion effects
- Component positions, sizes, margins, paddings, or layout
- Colors, themes, gradients, or visual tokens
- Button labels, icons, or placements
- Navigation structure or routing behavior
- State management logic or business rules
- Any `.tsx`, `.ts`, `.jsx`, `.js` file **outside** the `__tests__` directory or test-related configuration files

**The only files you are allowed to create or modify are:**
- Files inside `__tests__/` or `*.test.ts(x)` / `*.spec.ts(x)` patterns
- Jest configuration files (e.g., `jest.config.js`, `jest.setup.ts`)
- Test utility/helper files (e.g., `__mocks__/`, `testUtils.tsx`)

If achieving coverage of a line requires changing application code, **do not change it**. Instead, write a test that exercises the existing code path as-is.

---

## Steps

### 1. Run the Coverage Report

Always begin by running the full coverage command in the **active terminal**:

```bash
npm run test:coverage
```

Do NOT skip this step. Do NOT use cached results. Do NOT assume the current state of coverage.

Wait for the full output to appear. 

**CRITICAL STEP:** Before looking at the coverage table, check if any tests FAILED.
If any tests failed (`failed` in the test summary), you MUST fix the failing tests before attempting to improve coverage. A test suite that fails cannot have valid coverage.

If all tests passed, proceed to parse the coverage table printed in the terminal.

### 2. Parse the Terminal Output — Auto-Identify Uncovered Files

Read the coverage table carefully. Identify every file that has **any metric below 100%**.

Look for:
- Lines reported as `Uncovered Line #s` in the rightmost column
- Any cell marked in **yellow** or showing a number below `100`
- Files with partial branch coverage (e.g., `Branch: 80%`)

Build a **prioritized target list** of files to cover, ordered by:
1. Files with 0% coverage first (completely untested)
2. Files with branch gaps (most complex to cover)
3. Files with minor missing lines last

Report your findings before proceeding:

```
## Coverage Analysis

### Files Below 100%
| File | % Stmts | % Branch | % Funcs | % Lines | Uncovered Lines |
|------|---------|----------|---------|---------|-----------------|
| src/components/Foo.tsx | 85 | 60 | 100 | 85 | 34, 56-58 |
...

### Action Plan
- [ ] File A — cover uncovered lines: 34, 56–58
- [ ] File B — cover missing branch at line 22 (ternary/null check)
...
```

---

### 3. Write Tests — One File at a Time

For each file in the target list:

1. **Read the source file** — fully understand the logic before writing tests
2. **Identify the exact uncovered path** — look at the uncovered line numbers from the report
3. **Write a focused test** that exercises only that path
4. **Do NOT modify the source file** — adapt the test to fit the existing behavior

**Test writing principles:**
- Each test must have a clear, descriptive name using `it('should ...')` or `test('should ...')`
- Mock all external dependencies (navigation, APIs, stores, async calls) using `jest.mock()`
- For branch coverage: write separate `it()` blocks for each truthy/falsy/null path
- For function coverage: every exported and internal function must be called at least once
- For statement coverage: every line of code must be reachable by at least one test
- Use `@testing-library/react-native` for component rendering and interaction
- Use `fireEvent` or `userEvent` to simulate user interactions (press, change, scroll)
- Use `waitFor`, `act`, or `flushPromises` for async behavior

---

### 4. Re-run Coverage After Each File

After writing or updating tests for a file, re-run:

```bash
npm run test:coverage
```

Check the output:
- If the file is now at 100% across all metrics → mark it as done
- If gaps remain → return to step 3 for that file
- If new uncovered lines appeared in other files → add them to the target list

**Do NOT move on to the next file until the current file reaches 100%.**

---

### 5. Repeat Until All Files Are at 100%

Loop through all target files. After all files are addressed, run one final full coverage check:

```bash
npm run test:coverage
```

The final output must show `100 | 100 | 100 | 100` across all files and in the summary row.

If **any** file still shows below 100%:
- Do NOT declare success
- Return to step 2 and identify the remaining gaps
- Repeat until fully resolved

---

### 6. Final Verification Report

Once all metrics are 100%, produce a structured summary:

```
## ✅ Coverage Complete

All metrics are at 100%.

| Metric    | Before | After |
|-----------|--------|-------|
| % Stmts   | XX%    | 100%  |
| % Branch  | XX%    | 100%  |
| % Funcs   | XX%    | 100%  |
| % Lines   | XX%    | 100%  |

### Tests Written This Session
- src/__tests__/components/Foo.test.tsx — covered lines 34, 56–58 (null guard + else branch)
- src/__tests__/utils/bar.test.ts — covered all 3 exported functions + edge cases
...

### No Application Code Was Modified
✓ Zero changes to any UI, component, style, or logic files outside __tests__/
```

---

## Handling Common Coverage Gaps

| Situation | What To Do |
|-----------|-----------|
| Uncovered `if` branch | Write a test that makes the condition falsy/truthy as needed |
| Uncovered `catch` block | Mock the dependency to throw an error and assert the catch behavior |
| Uncovered `else` / `default` | Pass values that trigger the alternative path |
| Uncovered async path | Use `await waitFor(...)` and mock resolved/rejected promises |
| Uncovered early return | Pass invalid/boundary input that triggers the guard clause |
| Ternary expression not fully covered | Write two tests: one for each branch of the ternary |
| Optional chaining (`?.`) | Test both when the value is defined and when it's `undefined`/`null` |
| Dead code (truly unreachable) | Do NOT delete it. Write a comment noting it and report to the user |

---

## Guardrails

- **Never modify application code** — not even a single character, not even a comment
- **Never skip a file** — every file with gaps must be addressed
- **Never declare success with partial coverage** — 99% is a failure
- **Always re-run the full coverage command** after changes — never estimate
- **Never mock the module under test** — only mock its dependencies
- **Do not add `/* istanbul ignore */` or `/* c8 ignore */` annotations** — that is cheating and is forbidden
- **Do not use `any` type casts in tests to bypass TypeScript** — write proper typed tests
- **Read the terminal output literally** — trust the coverage numbers, not your assumptions
- **If a branch is impossible to cover without changing source code**, stop and report it clearly to the user before continuing

---

## Fluid Workflow Integration

This workflow can be invoked at any time:

- **After implementing features**: Run immediately after new code is written to prevent coverage debt
- **During debugging**: If tests are failing, use this workflow to fix the tests first, then re-check coverage
- **On CI failures**: Use this workflow to identify and eliminate all failing tests and coverage gaps before merging
- **As a standalone session**: Can be run on any project with Jest coverage configured

When invoked, always start from step 1 (run the command) — never assume you know the current state.
