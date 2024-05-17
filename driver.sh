# This driver grabs the file path from Automator and passes it to Fixie.

#!/bin/bash

# Check if a directory path is provided
if [ "$#" -ne 1 ]; then
    echo "Missing argument: $0 <directory-path>"
    exit 1
fi

# confirm before launching:
# osascript <<EOD
# tell application "System Events"
#     display dialog "Launch Fixie?"
# end tell
# EOD

# Display dialog before launching fixie:
osascript <<EOD
tell application "System Events"
    display dialog "Fixie is working..." giving up after 1
end tell
EOD

FILE_PATH=$1

source venv/bin/activate

python3 app.py "$FILE_PATH"

# if app.py script fails will exit with a non-zero status
STATUS=$?

deactivate

if [ $STATUS -ne 0 ]; then
    case $STATUS in 
    1)
        osascript -e 'tell app "System Events" to display dialog "crop failed at summary section"'
        exit 1
        ;;
    2)
        osascript -e 'tell app "System Events" to display dialog "Crop failed at dividends section"'
        exit 2
        ;;
    3)
        osascript -e 'tell app "System Events" to display dialog "failed extracting broker transactions table"'
        exit 3
        ;;
    4)
        osascript -e 'tell app "System Events" to display dialog "failed extracting dividends table"'
        exit 4
        ;;
    5)
        osascript -e 'tell app "System Events" to display dialog "failed creating csv files"'
        exit 5
        ;;
    6)
        osascript -e 'tell app "System Events" to display dialog "failed extracting interest table"'
        exit 6
        ;;
    *)
        osascript -e 'tell app "System Events" to display dialog "unknown error with status '$STATUS'"'
        exit $STATUS
        ;;
    esac
fi

open './output'