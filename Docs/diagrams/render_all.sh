#!/usr/bin/env bash
# Render all Mermaid diagrams to PNG for LaTeX inclusion.
# Requires: npm install -g @mermaid-js/mermaid-cli
# Usage: cd Docs/diagrams && bash render_all.sh
set -euo pipefail

OUTPUT_DIR="../images/diagrams"
mkdir -p "$OUTPUT_DIR"

DIAGRAMS=(
  "d0_kerangka:kerangka_berpikir"
  "d1_ai_flow:alur_ai"
  "d2_c4_context:c4_context"
  "d3_c4_container:c4_container"
  "d4_c4_component:c4_component"
  "d5_usecase:usecase"
  "d6_sequence_ai:sequence_ai"
  "d7_class:class_diagram"
  "d8_onnx_export:onnx_pipeline"
)

for entry in "${DIAGRAMS[@]}"; do
  src="${entry%%:*}"
  dst="${entry##*:}"
  echo "Rendering $src.mmd → $OUTPUT_DIR/$dst.png ..."
  mmdc \
    --input  "${src}.mmd" \
    --output "${OUTPUT_DIR}/${dst}.png" \
    --width  1600 \
    --backgroundColor white
done

echo "Done. All diagrams rendered to $OUTPUT_DIR/"
