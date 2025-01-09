#!/bin/bash

# Email details
TO="your@email.com"
CURRENT_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')
CURRENT_DATE=$(date '+%Y/%m/%d')
SUBJECT="Motion Detected: Video Alert at $CURRENT_DATETIME"

# Extract the relative path from the full file path
VIDEO_FILE_PATH="$1"
RELATIVE_PATH="${VIDEO_FILE_PATH#/var/www/html/}"

# Construct the URL
VIDEO_URL="http://server.local/${RELATIVE_PATH}"
VIDEO_URL_ONLINE="https://server/${RELATIVE_PATH}"

# HTML body
BODY=$(cat <<EOF
<html>
<head>
  <title>Motion Detected</title>
</head>
<body>
  <p>Motion has been detected. You can view the video at: <a href="$VIDEO_URL">$VIDEO_URL</a></p>
  <p>Access the local server: <a href="http://server.local/motion/$CURRENT_DATE">http://server.local/</a></p>
  <p>Access today's recordings: <a href="https://server/motion/$CURRENT_DATE/">https://server/motion/$CURRENT_DATE/</a></p>
  <p>Access video online: <a href="$VIDEO_URL_ONLINE">$VIDEO_URL_ONLINE</a></p>
</body>
</html>
EOF
)

# Send email using msmtp
echo -e "To: $TO\nSubject: $SUBJECT\nMIME-Version: 1.0\nContent-Type: text/html\n\n$BODY" | msmtp --from=mail@mailserver.com -- $TO

