#!/bin/bash
set +e

echo "---PULPCORE---"
systemctl status pulpcore
journalctl -xeu pulpcore
echo "---PULPCORE-API---"
systemctl status pulpcore-api
journalctl -xeu pulpcore-api
echo "---PULPCORE-CONTENT---"
systemctl status pulpcore-content
journalctl -xeu pulpcore-content
echo "---PULPCORE-WORKER@1---"
systemctl status pulpcore-worker@1
journalctl -xeu pulpcore-worker@1
echo "---PULPCORE-WORKER@2---"
systemctl status pulpcore-worker@2
journalctl -xeu pulpcore-worker@2
