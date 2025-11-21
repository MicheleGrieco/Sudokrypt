#!/bin/bash

# Sudoku Solver Docker Build and Run Script

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="sudoku-solver"
CONTAINER_NAME="sudoku-solver-container"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  build           Build the Docker image"
    echo "  run [args]      Run the container (pass args to sudoku_solver.py)"
    echo "  help            Show sudoku_solver.py help"
    echo "  shell           Open a shell inside the container"
    echo "  clean           Remove the Docker image"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 run puzzle.txt"
    echo "  $0 help"
}

# Function to build the image
build_image() {
    echo -e "${YELLOW}Building Docker image: $IMAGE_NAME${NC}"
    docker build -t $IMAGE_NAME .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Image built successfully${NC}"
    else
        echo -e "${RED}✗ Build failed${NC}"
        exit 1
    fi
}

# Function to run the container
run_container() {
    echo -e "${YELLOW}Running Sudoku Solver...${NC}"
    docker run --rm -v "$(pwd):/data" -w /data $IMAGE_NAME "$@"
}

# Function to show help
show_help() {
    docker run --rm $IMAGE_NAME -h
}

# Function to open shell
open_shell() {
    echo -e "${YELLOW}Opening shell in container...${NC}"
    docker run --rm -it -v "$(pwd):/data" -w /data $IMAGE_NAME --time /bin/bash
}

# Function to clean up
clean_image() {
    echo -e "${YELLOW}Removing Docker image: $IMAGE_NAME${NC}"
    docker rmi $IMAGE_NAME
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Image removed${NC}"
    else
        echo -e "${RED}✗ Failed to remove image${NC}"
        exit 1
    fi
}

# Main script logic
case "$1" in
    build)
        build_image
        ;;
    run)
        shift
        run_container "$@"
        ;;
    help)
        show_help
        ;;
    shell)
        open_shell
        ;;
    clean)
        clean_image
        ;;
    *)
        usage
        exit 1
        ;;
esac