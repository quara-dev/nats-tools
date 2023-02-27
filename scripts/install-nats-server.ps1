# Define nats-server version
$natsVersion = "2.9.14"

# Check if this is the latest URL and update the URL if that's not the case
$NatsServerDownloadUrl = "https://github.com/nats-io/nats-server/releases/download/v$natsVersion/nats-server-v$natsVersion-windows-amd64.zip"

# Download archive
Invoke-WebRequest -Uri "$NatsServerDownloadUrl" -OutFile "nats-server-v$natsVersion-windows-amd64.zip"
# Uncompress archive
Expand-Archive "nats-server-v$natsVersion-windows-amd64.zip"
# Remove archive
Remove-Item -Force "nats-server-v$natsVersion-windows-amd64.zip"

# Where to put NATS by default on Windows ?
Move-Item "nats-server-v$natsVersion-windows-amd64/nats-server-v$natsVersion-windows-amd64/nats-server.exe" "./nats-server.exe"
# Remove downloaded directory
Remove-Item -Recurse -Force "nats-server-v$natsVersion-windows-amd64"
