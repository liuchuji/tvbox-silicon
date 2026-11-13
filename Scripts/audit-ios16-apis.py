#!/usr/bin/env python3
"""Report likely iOS 17+ SwiftUI/API references for the iOS 16 compatibility pass.

This is a review aid, not a compiler or a proof that every call is guarded.
It scans Swift source under App/ and Sources/ and prints the matching line plus
nearby availability annotations so the macOS CI log can be triaged.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = (
    "scrollPosition", "contentMargins", "sensoryFeedback", "symbolEffect",
    "defaultScrollAnchor", "scrollClipDisabled", "safeAreaPadding",
    "containerRelativeFrame", "scrollTargetBehavior", "scrollTargetLayout",
    "contentTransition", "phaseAnimator", "keyframeAnimator", "visualEffect",
    "scrollTransition", "toolbarTitleDisplayMode", "onGeometryChange",
    "navigationTransition", "matchedTransitionSource", "tabViewBottomAccessory",
    "glassEffect", "safeAreaBar", "toolbarRole",
)

def main():
    files = sorted(
        p for root in (ROOT / "App", ROOT / "Sources")
        if root.exists() for p in root.rglob("*.swift")
    )
    count = 0
    for path in files:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for index, line in enumerate(lines):
            found = [token for token in TOKENS if token in line]
            if not found:
                continue
            start = max(0, index - 5)
            context = " | ".join(
                f"{n + 1}:{lines[n].strip()}" for n in range(start, index + 1)
                if "#available" in lines[n] or n == index
            )
            print(f"{path.relative_to(ROOT)}:{index + 1}: {','.join(found)}: {context}")
            count += 1
    print(f"Scanned {len(files)} Swift files; found {count} candidate API references.")
    print("Review each match: nearby #available text is a clue, not a complete guard analysis.")

if __name__ == "__main__":
    main()
