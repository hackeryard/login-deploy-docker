#!/bin/bash

echo "stoping all..."

ps -ef | grep hydra | awk '{print $2}' | xargs kill -9
ps -ef | grep consent | awk '{print $2}' | xargs kill -9
ps -ef | grep manage | awk '{print $2}' | xargs kill -9

