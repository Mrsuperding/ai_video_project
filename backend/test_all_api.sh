#!/bin/bash

echo "=============================================="
echo "         BACKEND API COMPREHENSIVE TEST      "
echo "=============================================="
echo ""

# Step 1: Register/SMS Login
echo ">>> Step 1: Register/Login via SMS"
RESP=$(curl -s -X POST http://localhost:8000/api/v1/auth/sms/send \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138888","code_type":"register"}')
echo "Send SMS: $RESP"

RESP=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/sms \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138888","code":"123456","device_type":"web"}')
echo "Login: $RESP" | python -c "import sys,json; d=json.load(sys.stdin); print('code:', d.get('code'), 'message:', d.get('message'))"

# Extract token
TOKEN=$(echo $RESP | python -c "import sys,json; print(json.load(sys.stdin)['data']['tokens']['access_token'])" 2>/dev/null)
echo "TOKEN: ${TOKEN:0:50}..."
echo ""

# Helper function
test_api() {
    local method=$1
    local path=$2
    local data=$3
    local desc=$4
    
    echo ">>> $desc"
    if [ "$method" = "GET" ]; then
        RESP=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$path" -H "Authorization: Bearer $TOKEN")
        BODY=$(echo "$RESP" | sed '$d')
        CODE=$(echo "$RESP" | tail -1 | cut -d: -f2)
        echo "Status: $CODE"
        echo "Response: ${BODY:0:200}..."
    else
        RESP=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X $method "$path" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data")
        BODY=$(echo "$RESP" | sed '$d')
        CODE=$(echo "$RESP" | tail -1 | cut -d: -f2)
        echo "Status: $CODE"
        echo "Response: ${BODY:0:300}..."
    fi
    echo ""
}

# USER APIs
echo "=============================================="
echo "              USER APIs                       "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/user/profile" "" "Get User Profile"
test_api PATCH "http://localhost:8000/api/v1/user/profile" '{"nickname":"TestUser","email":"test@test.com"}' "Update User Profile"

# WALLET APIs
echo "=============================================="
echo "              WALLET APIs                    "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/wallet/info" "" "Get Wallet Info"
test_api GET "http://localhost:8000/api/v1/wallet/transactions" "" "Get Wallet Transactions"

# DIGITAL HUMAN APIs
echo "=============================================="
echo "           DIGITAL HUMAN APIs                "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/digital-humans" "" "Get Digital Humans List"
test_api POST "http://localhost:8000/api/v1/digital-humans" '{"name":"My DH","gender":"male","source_type":"photo","source_photos":["http://x.jpg"]}' "Create Digital Human"

# SCRIPT APIs
echo "=============================================="
echo "              SCRIPT APIs                     "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/scripts" "" "Get Scripts List"
test_api POST "http://localhost:8000/api/v1/scripts" '{"title":"My Script","content":"Hello world"}' "Create Script"

# VIDEO APIs
echo "=============================================="
echo "              VIDEO APIs                     "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/video-projects" "" "Get Video Projects"
test_api POST "http://localhost:8000/api/v1/video-projects" '{"project_name":"My Video","script_id":1,"digital_human_id":1}' "Create Video Project"

# MESSAGE APIs
echo "=============================================="
echo "              MESSAGE APIs                   "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/messages" "" "Get Messages"
test_api GET "http://localhost:8000/api/v1/messages/unread-count" "" "Get Unread Count"

# STATISTICS APIs
echo "=============================================="
echo "            STATISTICS APIs                  "
echo "=============================================="
test_api GET "http://localhost:8000/api/v1/user/statistics" "" "Get User Statistics"
test_api GET "http://localhost:8000/api/v1/user/statistics/quota" "" "Get User Quota"

echo "=============================================="
echo "         ALL API TESTS COMPLETED             "
echo "=============================================="
