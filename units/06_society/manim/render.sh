#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# render.sh — Render Manim scenes for Unit 06: Physics & Society.
#
# Usage:
#   ./render.sh                         # render all three scenes
#   ./render.sh radioactive_decay       # render a specific scene
#   ./render.sh radiation_penetration
#   ./render.sh chain_reaction
#
# Quality:
#   Pass -q <flag> as the second argument, e.g.:
#     ./render.sh all -qh      # high quality (default)
#     ./render.sh all -ql      # low quality (fast preview)
#     ./render.sh all -qk      # 4K quality
#
# Output lands in units/06_society/manim/output/ (gitignored).
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SCENES_DIR="$SCRIPT_DIR/scenes"
OUTPUT_DIR="$SCRIPT_DIR/output"
SCENE_NAMES=("radioactive_decay" "radiation_penetration" "chain_reaction")

# ── Quality flag ─────────────────────────────────────────────────────
QUALITY="${2:--qh}"

# ── Docker image ─────────────────────────────────────────────────────
IMAGE="manimcommunity/manim:stable"

# ── Ensure output directory exists ───────────────────────────────────
mkdir -p "$OUTPUT_DIR"

# ── Resolve which scenes to render ───────────────────────────────────
if [ $# -ge 1 ] && [ "$1" != "all" ] && [ "$1" != "-q" ]; then
    TARGETS=("$1")
else
    TARGETS=("${SCENE_NAMES[@]}")
fi

# ── Render each scene ────────────────────────────────────────────────
for scene in "${TARGETS[@]}"; do
    HOST_SCENE_FILE="$SCENES_DIR/${scene}.py"
    DOCKER_SCENE_FILE="/work/units/06_society/manim/scenes/${scene}.py"

    if [ ! -f "$HOST_SCENE_FILE" ]; then
        echo "ERROR: Scene file not found: $HOST_SCENE_FILE"
        exit 1
    fi

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  Rendering:  ${scene}"
    echo "  Quality:    ${QUALITY}"
    echo "  File:       ${HOST_SCENE_FILE}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    docker run --rm \
        -v "$REPO_ROOT":/work \
        -w /work \
        -e PYTHONPATH=/work/src \
        --user "$(id -u):$(id -g)" \
        "$IMAGE" \
        manim \
            "$DOCKER_SCENE_FILE" \
            "$QUALITY" \
            --disable_caching \
            --format mp4 \
            --media_dir "/work/units/06_society/manim/output"

    echo ""
    echo "── Render exit code: $?"
done

# ── Summary ──────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Render complete!"
echo "  Output directory: $OUTPUT_DIR"
echo "═══════════════════════════════════════════════════════════"

# ── Flatten: copy rendered MP4s from nested media_dir -> flat dir ──
echo ""
echo "  Flattening output..."
find "$OUTPUT_DIR" -path "*/videos/*" -name "*.mp4" ! -path "*/partial_movie_files/*" -type f \
    -exec cp {} "$OUTPUT_DIR/" \;
echo ""

echo "  Final files:"
ls -la "$OUTPUT_DIR"/*.mp4 2>/dev/null || echo "(no .mp4 files found)"
echo ""