#!/bin/bash

# Get token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/sms/send \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","code_type":"register"}' > /dev/null && \
curl -s -X POST http://localhost:8000/api/v1/auth/login/sms \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","code":"123456","device_type":"web"}' | python -c "import sys,json; print(json.load(sys.stdin)['data']['tokens']['access_token'])")

echo "TOKEN: ${TOKEN:0:50}..."
echo ""

echo "========== USER API TESTS =========="
echo ""

echo "=== Test: Get Profile ==="
curl -s http://localhost:8000/api/v1/user/profile -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Update Profile ==="
curl -s -X PATCH http://localhost:8000/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nickname":"Test User","email":"test@example.com"}'
echo -e "\n"

echo "=== Test: Get User Quota ==="
curl -s http://localhost:8000/api/v1/user/quota -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "========== WALLET API TESTS =========="
echo ""

echo "=== Test: Get Wallet Info ==="
curl -s http://localhost:8000/api/v1/wallet/info -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Get Wallet Transactions ==="
curl -s http://localhost:8000/api/v1/wallet/transactions -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "========== DIGITAL HUMAN API TESTS =========="
echo ""

echo "=== Test: Get Digital Humans List ==="
curl -s http://localhost:8000/api/v1/digital-humans -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Create Digital Human ==="
curl -s -X POST http://localhost:8000/api/v1/digital-humans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test DH","gender":"male","source":"photo","photo_url":"http://example.com/photo.jpg"}'
echo -e "\n"

echo "========== SCRIPT API TESTS =========="
echo ""

echo "=== Test: Get Scripts List ==="
curl -s http://localhost:8000/api/v1/scripts -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Create Script ==="
curl -s -X POST http://localhost:8000/api/v1/scripts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Script","content":"Hello World"}'
echo -e "\n"

echo "========== VIDEO API TESTS =========="
echo ""

echo "=== Test: Get Video Projects ==="
curl -s http://localhost:8000/api/v1/video-projects -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Create Video Project ==="
curl -s -X POST http://localhost:8000/api/v1/video-projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_name":"Test Video","script_id":1,"digital_human_id":1}'
echo -e "\n"

echo "========== MESSAGE API TESTS =========="
echo ""

echo "=== Test: Get Messages ==="
curl -s http://localhost:8000/api/v1/messages -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Get Unread Count ==="
curl -s http://localhost:8000/api/v1/messages/unread-count -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "========== STATISTICS API TESTS =========="
echo ""

echo "=== Test: Get User Statistics ==="
curl -s http://localhost:8000/api/v1/user/statistics -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Test: Get Quota ==="
curl -s http://localhost:8000/api/v1/user/statistics/quota -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "========== ALL TESTS COMPLETED =========="
