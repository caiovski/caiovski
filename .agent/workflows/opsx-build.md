---
description: Build and refactoring rules for creating screens, interfaces, and code components.
---

# Build & Refactor Doctrine (opsx-build)

When building new features, screens, interfaces, buttons, or functions—or when refactoring existing ones—you MUST strictly follow these rules to ensure the codebase remains scalable, clean, and easy to maintain.

## 1. Strict File Size Limits
- **Target Maximum:** 250 lines per file.
- **Absolute Tolerance:** 300 lines per file.
- **Action:** If a file is approaching or exceeding 250 lines, it MUST be refactored and split immediately. Do not ask for permission to split if it violates this rule; just do it.

## 2. Directory-Based Screen Architecture
Never create a monolithic `[ScreenName]Screen.tsx` file. Every screen MUST be organized into its own dedicated directory following the separation of concerns model ("The Great Refactoring" model).

### Required Structure:
```text
src/presentation/screens/FeatureName/ScreenName/
├── ScreenNameScreen.tsx       # View layer: pure UI, layout, and rendering only.
├── ScreenNameScreen.styles.ts # Styles layer: StyleSheet definitions.
├── useScreenNameScreen.ts     # Controller layer: state, hooks, effects, and business logic.
└── index.ts                   # Export layer: simple re-export of the screen component.
```

### Separation Rules:
- **`ScreenNameScreen.tsx`**: Must import `useScreenNameScreen` to get state and handlers. It should contain minimal to no `useState` or `useEffect` hooks directly.
- **`useScreenNameScreen.ts`**: Returns an object containing all the state variables and functions needed by the View. It handles Supabase calls, navigation logic, and complex state derivations.

## 3. SVG & Asset Handling
- Do not inline massive SVG XML strings directly inside screen files.
- Use the `SvgAsset` component approach (e.g., `<SvgAsset xml={MY_ICON_XML} />`).
- If an SVG XML string is long, extract it into a separate constants/assets file or a dedicated UI component file to keep the main view clean.

## 4. Reusable Components
- If a UI element (button, card, header) is used more than once or is complex enough to bloat the screen file, extract it into a separate component within the screen's directory (e.g., `components/MyCustomButton.tsx`) or into the global `presentation/components` folder if shared.

## 5. Unbreakable Dogma: Zero Alteration During Refactor
> ⛔ **IT IS STRICTLY FORBIDDEN to alter the interface during refactoring.**
- When moving code, extracting components, or changing the directory structure, you MUST keep the UI **100% original**.
- This includes buttons, sizes, margins, positions, padding, colors, functions, animations, and the general interface layout. It is not just about being "visually identical"—all properties and attributes must remain exactly as they were.
- This is not a proposal; it is an **unbreakable dogma**.
- If a refactoring step breaks or alters any aspect of the screen, you MUST immediately fix it and return it **100% to its original state** while keeping the code refactored.

## 6. Post-Refactor Test Verification
- Whenever you refactor a file or component, you MUST automatically run the tests to verify that they are at least passing.
- Structural refactoring often breaks test imports or mocks. It is your responsibility to fix the tests so they pass after your refactoring is complete.

## 7. Execution Stance
- **Language:** This rulebook is written in English.
- **Enforcement:** You must follow these structural and visual rules rigorously. Maintainability and UI integrity are the highest priorities.
