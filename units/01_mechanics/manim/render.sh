#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# render.sh — Render Manim scenes for Unit 01: Mechanics (M4).
#
# Usage:
#   ./render.sh                         # render all three scenes
#   ./render.sh shm_projection          # render a specific scene
#   ./render.sh integrator_convergence
#   ./render.sh projectile_dt
#
# Quality:
#   Pass -q <flag> as the second argument, e.g.:
#     ./render.sh all -qh      # high quality (default)
#     ./render.sh all -ql      # low quality (fast preview)
#     ./render.sh all -qk      # 4K quality
#
# Output lands in units/01_mechanics/manim/output/ (gitignored).
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SCENES_DIR="$SCRIPT_DIR/scenes"
OUTPUT_DIR="$SCRIPT_DIR/output"
SCENE_NAMES=("shm_projection" "integrator_convergence" "projectile_dt" "damped_shm" "planet_freefall" "projectile_drag")

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
    SCENE_FILE="$SCENES_DIR/${scene}.py"

    if [ ! -f "$SCENE_FILE" ]; then
        echo "ERROR: Scene file not found: $SCENE_FILE"
        exit 1
    fi

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  Rendering:  ${scene}"
    echo "  Quality:    ${QUALITY}"
    echo "  File:       ${SCENE_FILE}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    # Convert host path to Docker-internal path (/work-relative)
    SCENE_REL="${SCENE_FILE#$REPO_ROOT/}"

    docker run --rm \
        -v "$REPO_ROOT":/work \
        -w /work \
        -e PYTHONPATH=/work/src \
        --user "$(id -u):$(id -g)" \
        "$IMAGE" \
        manim \
            "/work/$SCENE_REL" \
            "$QUALITY" \
            --disable_caching \
            --format mp4 \
            --media_dir "/work/units/01_mechanics/manim/output"

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