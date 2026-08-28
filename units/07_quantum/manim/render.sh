#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# render.sh — Render Manim scenes for Unit 07: Quantum Physics.
#
# Usage:
#   ./render.sh                         # render all six scenes
#   ./render.sh energy_levels           # render a specific scene
#   ./render.sh photoelectric
#   ./render.sh wavefunction_probability
#   ./render.sh rutherford_scattering
#   ./render.sh hydrogen_spectra
#   ./render.sh superposition_state
#
# Quality:
#   Pass -q <flag> as the second argument, e.g.:
#     ./render.sh all -qh      # high quality (default)
#     ./render.sh all -ql      # low quality (fast preview)
#     ./render.sh all -qk      # 4K quality
#
# Output lands in units/07_quantum/manim/output/ (gitignored).
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SCENES_DIR="$SCRIPT_DIR/scenes"
OUTPUT_DIR="$SCRIPT_DIR/output"
SCENE_NAMES=("energy_levels" "photoelectric" "wavefunction_probability"
             "rutherford_scattering" "hydrogen_spectra" "superposition_state")

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
    SCENE_FILE="$SCENES_DIR/${scene}.py"

    if [ ! -f "$SCENE_FILE" ]; then
        echo "ERROR: Scene file not found: $SCENE_FILE"
        exit 1
    fi

    # Path relative to repo root (inside Docker container)
    REL_PATH="units/07_quantum/manim/scenes/${scene}.py"

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  Rendering:  ${scene}"
    echo "  Quality:    ${QUALITY}"
    echo "  File:       ${SCENE_FILE}"
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    docker run --rm \
        -v "$REPO_ROOT":/work \
        -w /work \
        -e PYTHONPATH=/work/src \
        --user "$(id -u):$(id -g)" \
        "$IMAGE" \
        manim \
            "$REL_PATH" \
            "$QUALITY" \
            --disable_caching \
            --format mp4 \
            --media_dir "/work/units/07_quantum/manim/output"

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
