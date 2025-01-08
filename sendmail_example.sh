#!/bin/bash

# Email details
TO=""
CURRENT_DATETIME=$(date '+%Y-%m-%d %H:%M:%S')
CURRENT_DATE=$(date '+%Y/%m/%d')
SUBJECT="Motion Detected: Video Alert at $CURRENT_DATETIME"

# HTML body
BODY=$(cat <<EOF
<html>
<head>
  <title>Motion Detected</title>
</head>
<body>
  <p>Motion has been detected. You can view the video at: <a href="$1">$1</a></p>
  <p>Access the local server: <a href="http://server.local/motion/$CURRENT_DATE">http://server.local/</a></p>
  <p>Access today's recordings: <a href="https://server/motion/$CURRENT_DATE/">https://server/motion/$CURRENT_DATE/</a></p>
</body>
</html>
EOF
)

# Send email using msmtp
echo -e "To: $TO\nSubject: $SUBJECT\nMIME-Version: 1.0\nContent-Type: text/html\n\n$BODY" | msmtp --from=yourserver@email.com -- $TO

