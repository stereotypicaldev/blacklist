# Define variables
DATABASE="/etc/pihole/gravity.db"
OUTPUT_FILE="/root/Blacklist/Testing/Filters/Automated/Empty.txt"
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
ERROR_FILE="/root/Blacklist/Testing/Filters/Automated/Empty-Execution Error.txt"
DELETE_QUERY="DELETE FROM adlist WHERE adlist.number=0;"

# Function to check if the SQLite database is locked
check_db_lock() {
    local db_file="$1"
    local lock_file="${db_file}-journal"
    if [ -f "$lock_file" ]; then
        echo "1" > "$ERROR_FILE"
        return 1
    fi
    return 0
}

# Function to run an SQLite command and check success
run_sqlite_command() {
    local query="$1"
    sqlite3 "$DATABASE" "$query"
    return $?
}

# Check if the database file exists
if [ ! -f "$DATABASE" ]; then
    echo "2" > "$ERROR_FILE"
    exit 1
fi

# Check if the output directory exists, create if it does not
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    if [ $? -ne 0 ]; then
        echo "3" > "$ERROR_FILE"
        exit 1
    fi
fi

# Check if the output file exists and is writable
if [ -e "$OUTPUT_FILE" ]; then
    if [ ! -w "$OUTPUT_FILE" ]; then
        echo "4" > "$ERROR_FILE"
        exit 1
    fi
else
    # Create the file if it does not exist
    touch "$OUTPUT_FILE"
    if [ $? -ne 0 ]; then
        echo "5" > "$ERROR_FILE"
        exit 1
    fi
fi

# Check if the database is locked
check_db_lock "$DATABASE"
if [ $? -ne 0 ]; then
    exit 1
fi

# Run the SQLite query to select addresses and append to the file
run_sqlite_command "SELECT address FROM adlist WHERE adlist.number=0;" >> "$OUTPUT_FILE"
if [ $? -ne 0 ]; then
    echo "6" > "$ERROR_FILE"
    exit 1
fi

# Wait for 30 seconds to ensure some time has passed
sleep 30

# Execute the delete query and ensure it's successful
run_sqlite_command "$DELETE_QUERY"
if [ $? -ne 0 ]; then
    echo "7" > "$ERROR_FILE"
    exit 1
fi

