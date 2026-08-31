#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# render.sh — Render Manim scenes for Unit 09: Scientific Inquiry.
#
# Usage:
#   ./render.sh                         # render all three scenes
#   ./render.sh linearisation           # render a specific scene
#   ./render.sh uncertainty
#   ./render.sh conclusion
#
# Quality:
#   Pass -q <flag> as the second argument, e.g.:
#     ./render.sh all -qh      # high quality (default)
#     ./render.sh all -ql      # low quality (fast preview)
#     ./render.sh all -qk      # 4K quality
#
# Output lands in units/09_inquiry/manim/output/ (gitignored).
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SCENES_DIR="$SCRIPT_DIR/scenes"
OUTPUT_DIR="$SCRIPT_DIR/output"
SCENE_NAMES=("linearisation" "linearisation_transforms" "uncertainty" "uncertainty_repeated" "conclusion" "epidemic" "engineering_design" "forest_fire" "crowd_control")

# Map scene name to scene file (some scenes share a file)
scene_file() {
    case "$1" in
        linearisation_transforms) echo "linearisation" ;;
        uncertainty_repeated)     echo "uncertainty" ;;
        *)                        echo "$1" ;;
    esac
}

# Map scene name to scene class name
scene_class() {
    case "$1" in
        linearisation) echo "Linearisation" ;;
        linearisation_transforms) echo "LinearisationTransforms" ;;
        uncertainty)   echo "Uncertainty" ;;
        uncertainty_repeated) echo "UncertaintyRepeated" ;;
        conclusion)    echo "Conclusion" ;;
        epidemic)      echo "EpidemicSpread" ;;
        engineering_design) echo "EngineeringDesign" ;;
        forest_fire)   echo "ForestFire" ;;
        crowd_control) echo "CrowdControl" ;;
        *)             echo "$1" ;;
    esac
}

# ── Quality flag ─────────────────────────────────────────────────────
QUALITY="${2:--qm}"

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
    SCENE_FILE="$SCENES_DIR/$(scene_file "$scene").py"

    if [ ! -f "$SCENE_FILE" ]; then
        echo "ERROR: Scene file not found: $SCENE_FILE"
        exit 1
    fi

    # Convert absolute host path to path relative to /work inside container
    SCENE_REL="${SCENE_FILE#$REPO_ROOT/}"

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  Rendering:  ${scene}"
    echo "  Quality:    ${QUALITY}"
    echo "  File:       ${SCENE_FILE}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    SCENE_CLASS="$(scene_class "$scene")"

    docker run --rm \
        -v "$REPO_ROOT":/work \
        -w /work \
        -e PYTHONPATH=/work/src \
        --user "$(id -u):$(id -g)" \
        "$IMAGE" \
        manim \
            "/work/$SCENE_REL" \
            "$SCENE_CLASS" \
            "$QUALITY" \
            --disable_caching \
            --format mp4 \
            --media_dir "/work/units/09_inquiry/manim/output"

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