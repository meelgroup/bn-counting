#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"

echo "Building ApproxASP..."
cd "$ROOT_DIR/ApproxASP"
mkdir -p build && cd build
cmake -DCLINGO_BUILD_SHARED=ON ..
make -j$(nproc)
cp approxasp "$ROOT_DIR/script"

echo "Done. Copied binaries to:"
echo "  $ROOT_DIR/script/approxasp"

echo "Installing fASP..."
cd "$ROOT_DIR/fASP"
pip install .

echo "Installing tsconj..."
cd "$ROOT_DIR/tsconj"
pip install .