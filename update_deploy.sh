#!/bin/bash

# Define the path to the Git repository
# REPO_PATH="homeautomation/"
REMOTE_BRANCH="main"
LOCAL_BRANCH="main"
MAX_RETRIES=20  # Timeout in seconds (5 minutes)

COUNTER=0

# Change to the Git repository directory
# cd "$REPO_PATH" || exit

# Function to check for updates and pull if necessary
check_updates() {
    git fetch origin $REMOTE_BRANCH
    REMOTE_HASH=$(git rev-parse "origin/$REMOTE_BRANCH")
    LOCAL_HASH=$(git rev-parse "$LOCAL_BRANCH")

    if [ "$REMOTE_HASH" != "$LOCAL_HASH" ]; then
        echo "Local repository is outdated. Remote repository has new commits. Pulling changes..."
        git pull origin $REMOTE_BRANCH
        return 1
    else
        echo "Local repository is up to date."
        return 0
    fi
}

# Check for updates initially
check_updates

# While loop with timeout
while [ $? -ne 0 ]; do
    check_updates
    
    # Increment retry count
    ((retry_count++))

    if [ $retry_count -ge $MAX_RETRIES ]; then
        echo "Maximum number of retries ($MAX_RETRIES) reached. Exiting loop."
        break
    fi

    sleep TIMEOUT # Check every 10 seconds
done

cd "dashboard/" || exit
echo "Building and running Docker container..."
sudo docker compose up -d

echo "Docker container build complete."