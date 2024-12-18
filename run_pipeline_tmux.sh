#!/bin/bash

# Name of the tmux session
SESSION_NAME="pipeline"

# Check if tmux is installed
if ! command -v tmux >/dev/null 2>&1; then
    echo "tmux is not installed. Please install it first."
    exit 1
fi

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new tmux session
tmux new-session -d -s $SESSION_NAME

# Send commands to the tmux session
tmux send-keys -t $SESSION_NAME "cd $(pwd)" C-m
tmux send-keys -t $SESSION_NAME "./pipeline.sh" C-m

echo "Pipeline started in tmux session '$SESSION_NAME'"
echo "To attach to the session: tmux attach -t $SESSION_NAME"
echo "To detach from session: Press Ctrl+b, then d"
echo "To kill the session: tmux kill-session -t $SESSION_NAME"

# Optionally attach to the session immediately
# Comment out the next line if you don't want to attach automatically
tmux attach -t $SESSION_NAME 