# Thông tin Triển khai — Day 12 Agent Production

## 🌐 URL Công khai
**https://day12-ai-agent-production.up.railway.app/**

## 🏗️ Nền tảng (Platform)
**Railway** (Triển khai thông qua Dockerfile & GitHub integration)

## 🧪 Các lệnh kiểm tra (Test Commands)

### 1. Kiểm tra sức khỏe (Health Check)
```bash
curl https://day12-ai-agent-production.up.railway.app/health
```
**Kết quả mong đợi:** `{"status": "ok", "version": "1.0.0", ...}`

### 2. Kiểm tra API (Có xác thực & Lịch sử)
```bash
$headers = @{ "X-API-Key" = "lab-secret-2026" }
$body = @{ 
    user_id = "test_user_01"
    question = "Xin chao Agent, ten toi la Dung" 
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://day12-ai-agent-production.up.railway.app/ask" -Method Post -ContentType "application/json" -Headers $headers -Body $body
```

## 🔐 Các biến môi trường đã thiết lập
- `PORT`: 8000
- `AGENT_API_KEY`: lab-secret-2026
- `ENVIRONMENT`: production
- `APP_NAME`: AI-Agent-Full-Stack

## 📸 Minh chứng (Screenshots)
Các ảnh chụp màn hình được lưu trữ tại thư mục `/images` trong repository này.

---
**Ghi chú:** Đây là bản Agent hoàn chỉnh bao gồm đầy đủ Auth, Rate Limit và Cost Guard.
