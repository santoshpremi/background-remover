#!/bin/bash

echo "🚀 Building multi-architecture Docker images..."
echo "=============================================="

# Check if buildx is available and create a new builder if needed
if ! docker buildx inspect multiarch-builder >/dev/null 2>&1; then
    echo "📦 Creating new multi-architecture builder..."
    docker buildx create --name multiarch-builder --use
fi

# Use the multi-architecture builder
docker buildx use multiarch-builder

# Build for both AMD64 and ARM64
echo "🔨 Building for AMD64 (x86_64) and ARM64 (aarch64)..."
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag santoshpremi/bg-remover-01:latest \
    --tag santoshpremi/bg-remover-01:multiarch \
    --push \
    .

echo ""
echo "✅ Multi-architecture build completed successfully!"
echo ""
echo "📊 Available images:"
docker images santoshpremi/bg-remover-01
echo ""
echo "🌐 To run on your current architecture:"
echo "docker run -p 8000:8000 santoshpremi/bg-remover-01:latest"
echo ""
echo "📋 To see all platforms available:"
echo "docker buildx imagetools inspect santoshpremi/bg-remover-01:latest"
