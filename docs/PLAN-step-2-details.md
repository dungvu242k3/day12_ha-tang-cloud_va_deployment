# PLAN: Chi Tiết Bước 2 - Thử Nghiệm Nhanh (Quick Start)

Tài liệu này chi tiết hóa nội dung của **Bước 2**, tập trung vào file `QUICK_START.md`. Đây là giai đoạn "mì ăn liền" giúp bạn thấy ngay kết quả thực tế chỉ trong vòng 30 phút.

## 🎯 Mục Tiêu
Triển khai AI Agent đầu tiên của bạn lên Cloud trong chưa đầy 30 phút.

## ✅ Kiểm Tra Điều Kiện Tiên Quyết (Prerequisites)
Trước khi bắt đầu, hãy đảm bảo máy bạn đã cài đặt:
- **Python 3.11+** (`python --version`)
- **Docker & Docker Compose** (`docker --version`)
- **Git** (`git --version`)

## 🚀 Lộ Trình Cấp Tốc (30 Phút)

### 1. Cài Đặt (2 Phút)
Di chuyển vào thư mục dự án và kiểm tra cấu trúc file.
```bash
cd day12_ha-tang-cloud_va_deployment
ls
```

### 2. Chạy Agent Cơ Bản (3 Phút)
Chạy Agent trực tiếp trên máy tính (localhost) để hiểu cách nó hoạt động.
- Đường dẫn: `01-localhost-vs-production/develop`
- Lệnh:
  ```bash
  pip install -r requirements.txt
  python app.py
  ```
- Kiểm tra bằng lệnh `curl` (trong terminal khác) để xem Agent trả lời.

### 3. Đưa Vào Docker (5 Phút)
Đóng gói Agent vào container để có thể mang đi mọi nơi.
- Đường dẫn: `02-docker/develop`
- Lệnh:
  ```bash
  docker build -t my-agent .
  docker run -p 8000:8000 my-agent
  ```
- Kết quả: Agent chạy trong Docker, truy cập qua port 8000.

### 4. Triển Khai Lên Cloud (10 Phút)
Sử dụng Railway để đưa Agent lên internet.
- Đường dẫn: `03-cloud-deployment/railway`
- Lệnh chính:
  ```bash
  railway login
  railway init
  railway up
  ```
- Kết quả: Bạn nhận được một URL công khai (ví dụ: `your-agent.railway.app`) có thể truy cập từ bất cứ đâu.

### 5. Thêm Bảo Mật (10 Phút)
Thẻ API Key để ngăn chặn người lạ sử dụng Agent của bạn.
- Đường dẫn: `04-api-gateway/develop`
- Lệnh: Thiết lập `AGENT_API_KEY="secret"` và chạy app.
- Kết quả: Truy cập vào Agent sẽ bị lỗi `401 Unauthorized` nếu không kèm theo Header chứa API Key.

---

## 🎯 Danh Sách Kiểm Tra Thành Công
Sau bước này, bạn phải nắm được:
- [ ] Cách chạy Python app cục bộ.
- [ ] Cách Build và Run Docker container.
- [ ] Cách Deploy lên Railway.
- [ ] Cách gửi yêu cầu kèm API Key qua `curl`.

---

## Bước Tiếp Theo:
Nếu bạn đã hoàn thành việc thử nghiệm nhanh này và thấy "ma thuật" của Deployment, chúng ta sẽ chuyển sang **Bước 3: Thực hành chi tiết (CODE_LAB.md)**. Bước 3 sẽ giải thích sâu hơn về Code và các cấu trúc Production thực thụ.

Bạn muốn tôi tiếp tục chi tiết **Bước 3** không?
