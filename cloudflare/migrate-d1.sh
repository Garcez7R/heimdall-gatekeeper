#!/bin/bash
# D1 Migration Script for Heimdall Gatekeeper
# Migrates data from SQLite to Cloudflare D1

set -e

echo "🔄 Starting D1 Migration"

# Configuration
D1_DATABASE_NAME="heimdall-db"
SQLITE_DB="data/heimdall.db"
BACKUP_FILE="data/heimdall_backup_$(date +%Y%m%d_%H%M%S).db"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if SQLite database exists
if [ ! -f "$SQLITE_DB" ]; then
    echo -e "${RED}Error: SQLite database not found at $SQLITE_DB${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Creating backup...${NC}"
cp "$SQLITE_DB" "$BACKUP_FILE"
echo -e "${GREEN}Backup created: $BACKUP_FILE${NC}"

echo -e "${YELLOW}Step 2: Exporting data from SQLite...${NC}"

# Export events
sqlite3 "$SQLITE_DB" << 'EOF' > events.sql
.mode insert events
SELECT * FROM events;
EOF

# Export alerts
sqlite3 "$SQLITE_DB" << 'EOF' > alerts.sql
.mode insert alerts
SELECT * FROM alerts;
EOF

# Export webhooks
sqlite3 "$SQLITE_DB" << 'EOF' > webhooks.sql
.mode insert webhooks
SELECT * FROM webhooks;
EOF

# Export audit trail
sqlite3 "$SQLITE_DB" << 'EOF' > audit_trail.sql
.mode insert audit_trail
SELECT * FROM audit_trail;
EOF

# Export user dashboards
sqlite3 "$SQLITE_DB" << 'EOF' > user_dashboards.sql
.mode insert user_dashboards
SELECT * FROM user_dashboards;
EOF

echo -e "${GREEN}Data exported successfully${NC}"

echo -e "${YELLOW}Step 3: Importing to D1...${NC}"

# Import to D1
wrangler d1 execute $D1_DATABASE_NAME --remote --file=events.sql
wrangler d1 execute $D1_DATABASE_NAME --remote --file=alerts.sql
wrangler d1 execute $D1_DATABASE_NAME --remote --file=webhooks.sql
wrangler d1 execute $D1_DATABASE_NAME --remote --file=audit_trail.sql
wrangler d1 execute $D1_DATABASE_NAME --remote --file=user_dashboards.sql

echo -e "${GREEN}Data imported to D1 successfully${NC}"

echo -e "${YELLOW}Step 4: Validation...${NC}"

# Validate row counts
SQLITE_EVENTS=$(sqlite3 "$SQLITE_DB" "SELECT COUNT(*) FROM events;")
D1_EVENTS=$(wrangler d1 execute $D1_DATABASE_NAME --remote --command="SELECT COUNT(*) FROM events;" | tail -1 | awk '{print $1}')

if [ "$SQLITE_EVENTS" = "$D1_EVENTS" ]; then
    echo -e "${GREEN}✅ Events migration validated: $SQLITE_EVENTS rows${NC}"
else
    echo -e "${RED}❌ Events migration failed: SQLite=$SQLITE_EVENTS, D1=$D1_EVENTS${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 5: Cleanup...${NC}"
rm -f events.sql alerts.sql webhooks.sql audit_trail.sql user_dashboards.sql

echo -e "${GREEN}🎉 Migration completed successfully!${NC}"
echo ""
echo "📋 Summary:"
echo "  - Backup: $BACKUP_FILE"
echo "  - Events migrated: $SQLITE_EVENTS"
echo "  - Ready for production use"