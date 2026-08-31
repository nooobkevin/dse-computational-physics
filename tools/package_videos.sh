#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# package_videos.sh — collect all rendered Manim MP4s into dist/videos/
# and zip them for distribution.
#
# Usage:
#   bash tools/package_videos.sh
#
# Walks units/*/manim/output/ for *.mp4 (the flattened top-level files
# produced by each unit's render.sh; falls back to nested videos/ dirs,
# excluding partial_movie_files), mirrors them into
# dist/videos/<unit>/ preserving scene names, writes
# dist/videos/MANIFEST.txt (unit, scene, size, mtime), prints a summary
# with total size, and zips everything to
# dist/dse-computational-physics-videos.zip (the old zip is removed
# first).
# ──────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$REPO_ROOT/dist"
VIDEOS_DIR="$DIST_DIR/videos"
MANIFEST="$VIDEOS_DIR/MANIFEST.txt"
ZIP_FILE="$DIST_DIR/dse-computational-physics-videos.zip"

# ── Portable stat: GNU (-c) vs BSD (-f) ──────────────────────────────
# Field codes: s = size in bytes, Y = mtime as epoch seconds.
stat_field() {
    # usage: stat_field <field> <file>
    local field="$1" file="$2"
    if stat -c "%${field}" "$file" >/dev/null 2>&1; then
        stat -c "%${field}" "$file"
    else
        case "$field" in
            s) stat -f "%z" "$file" ;;
            Y) stat -f "%m" "$file" ;;
        esac
    fi
}

human_size() {
    # usage: human_size <bytes>  → "12.3 MB"
    awk -v b="$1" 'BEGIN {
        split("B KB MB GB", u, " ");
        i = 1;
        while (b >= 1024 && i < 4) { b /= 1024; i++ }
        printf "%.1f %s", b, u[i]
    }'
}

# ── Fresh start ──────────────────────────────────────────────────────
rm -rf "$VIDEOS_DIR"
rm -f "$ZIP_FILE"
mkdir -p "$VIDEOS_DIR"

total_bytes=0
total_files=0

# ── Walk each unit's output directory ────────────────────────────────
for output_dir in "$REPO_ROOT"/units/*/manim/output; do
    [ -d "$output_dir" ] || continue
    unit="$(basename "$(dirname "$(dirname "$output_dir")")")"
    dest="$VIDEOS_DIR/$unit"
    mkdir -p "$dest"

    # Top-level flattened MP4s first, then nested videos/ as fallback.
    mp4s=()
    while IFS= read -r mp4; do
        mp4s+=("$mp4")
    done < <(
        find "$output_dir" -maxdepth 1 -name '*.mp4' -type f -print
        find "$output_dir" -path '*/videos/*' -name '*.mp4' \
            ! -path '*/partial_movie_files/*' -type f -print
    )

    unit_files=0
    unit_bytes=0
    seen=""
    for mp4 in "${mp4s[@]}"; do
        scene="$(basename "$mp4")"
        # Deduplicate by scene name (top-level flatten wins).
        case " $seen " in
            *" $scene "*) continue ;;
        esac
        seen="$seen $scene"

        cp "$mp4" "$dest/$scene"
        size="$(stat_field s "$mp4")"
        mtime="$(stat_field Y "$mp4")"
        printf "%s, %s, %s, %s\n" "$unit" "$scene" "$size" "$mtime" >> "$MANIFEST"

        unit_files=$((unit_files + 1))
        unit_bytes=$((unit_bytes + size))
    done

    if [ "$unit_files" -gt 0 ]; then
        echo "  $unit: $unit_files file(s), $(human_size "$unit_bytes")"
    fi
    total_files=$((total_files + unit_files))
    total_bytes=$((total_bytes + unit_bytes))
done

# ── Summary ──────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
if [ "$total_files" -eq 0 ]; then
    echo "  No MP4s found under units/*/manim/output/ — nothing to package."
    echo "═══════════════════════════════════════════════════════════"
    exit 1
fi
echo "  Packaged: $total_files MP4(s) across $(find "$VIDEOS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ') unit(s)"
echo "  Total size: $(human_size "$total_bytes")"
echo "  Manifest: $MANIFEST"
echo "═══════════════════════════════════════════════════════════"

# ── Zip (from dist/ so entries are videos/<unit>/<scene>.mp4) ───────
(cd "$DIST_DIR" && zip -qr "$ZIP_FILE" videos)
echo ""
echo "  Zip: $ZIP_FILE ($(human_size "$(stat_field s "$ZIP_FILE")"))"
echo ""