---
name: visual-layout-qa
description: Use when encountering responsive design issues, layout bugs across device breakpoints, or when diagnosing and fixing component overlap, text overflow, and grid wrapping on different screen sizes.
---

# Visual Layout QA

## Overview

Visual Layout QA is a systematic two-phase approach (Analysis then Correction) for evolutionary web projects. It relies entirely on visual evidence to find true layout breaks across all viewports, followed by a structured phase of targeted, verified code fixes.

## When to Use

- Verifying and fixing responsive behavior of a newly built page or component
- Finding and correcting the exact breakpoint where a layout transition fails
- Resolving horizontal scrolling, component overlap, or text overflow
- Ensuring UI consistency from small mobile (320px) to ultra-wide (2560px)

## Phase 1: Detailed Analysis

### The 8-Point Layout Check Matrix

For every viewport, verify these specific failure points:

1. **Horizontal Scrolling:** Is there unintended horizontal scrolling?
2. **Text Overflow:** Is text breaking out of its container or overlapping?
3. **Click Targets:** Are buttons/links too small or overlapping, making them unclickable?
4. **Image Distortion:** Are images losing their aspect ratio, stretched, or squashed?
5. **Grid/Flex Wrapping:** Do columns and cards stack properly on smaller screens without breaking the container?
6. **Component Overlap:** Are distinct UI elements bleeding into or covering each other?
7. **Spacing Issues:** Are padding/margins causing content to be squeezed unreadably tight on small screens?
8. **Excessive Whitespace:** Are there huge, unintended empty gaps on ultra-wide screens?

### Execution Process

Follow this exact sequence for the provided URL. Do not skip breakpoints.

1. Open the URL in a single browser session (initial height: 900px).
2. Iterate through all 8 breakpoints sequentially:
   - 320px | Small phone (iPhone SE)
   - 375px | Standard phone (iPhone 14)
   - 768px | Tablet portrait (iPad)
   - 1024px | Tablet landscape / small laptop
   - 1280px | Laptop
   - 1440px | Desktop
   - 1920px | Full HD
   - 2560px | Ultra-wide / 4K
3. **For each breakpoint:**
   - **Resize** the viewport to the target width.
   - **Wait** exactly 2 seconds for CSS reflows and layout transitions to complete.
   - **Screenshot** the above-fold area.
   - **Scroll and screenshot** the below-fold content. _(Ignore visual glitches caused by sticky/fixed navigation bars or floating elements during the scroll)._
   - **Run** the "8-Point Layout Check Matrix" against the visual evidence.
4. **Compile a concise summary `.md` report** of all findings BEFORE writing any code. Group issues by specific breakpoints or severity. Do not clutter the report with tests that passed.

## Phase 2: Systematic Correction

Do NOT start fixing until Phase 1 is fully complete and documented.

1. **Prioritize:** Address issues starting from the smallest screen size (mobile-first approach) and moving upwards, as mobile layouts often dictate the foundation.
2. **Isolate & Plan:** For each broken component, identify the exact CSS classes, structural markup, or Tailwind utilities causing the issue.
3. **Implement:** Apply the minimal necessary fix to the codebase. Avoid overarching global changes if a scoped fix is sufficient.
4. **Verify:** Re-test the fixed component at the broken breakpoint AND the adjacent breakpoints to ensure no regressions were introduced.
5. **Update:** Mark the issue as resolved in your summary `.md` report.

## Component Description Rule

**CRITICAL:** During analysis, do NOT use DOM class names, tags, or code-level selectors to describe elements.

Use clear, visual, and positional descriptions.

- ✅ _Good:_ "Sağ üst köşedeki dil değiştirme menüsü" (Top right language switcher menu)
- ✅ _Good:_ "Header'ın altındaki 3D makine modeli sunum alanı" (3D machine model presentation area below the header)
- ❌ _Bad:_ "The div with class .nav-wrapper"
- ❌ _Bad:_ "The ul element inside the header"

## Common Mistakes

| Mistake                                     | Fix                                                                          |
| ------------------------------------------- | ---------------------------------------------------------------------------- |
| Fixing issues immediately as they are found | Complete the entire Phase 1 analysis first to understand the full scope.     |
| Using DOM selectors for bug reports         | Use visual/positional descriptions (Component Description Rule).             |
| Skipping breakpoints                        | Test all 8 breakpoints to catch subtle CSS transition failures.              |
| Not verifying fixes                         | Always re-test the breakpoint after applying a fix to ensure no regressions. |

## Red Flags - STOP and Start Over

- Writing code/fixes before completing the Phase 1 analysis report
- Relying on DOM inspection instead of screenshots for QA
- Skipping the 2-second reflow wait time
- Listing breakpoints in the report that passed without issues
- "I'll just fix this one thing real quick" before finishing the analysis

**All of these mean: Discard current work. Start over following the two-phase process.**
