# PLAN: Chi Tiết Bước 4 & 5 - Hỗ Trợ, Hoàn Thiện & Nộp Bài

Tài liệu này chi tiết hóa giai đoạn cuối cùng của lộ trình thực hành, giúp bạn giải quyết các rắc rối kỹ thuật và đảm bảo bài nộp đạt điểm tối đa.

## 🛠️ Bước 4: Hỗ Trợ Kỹ Thuật (Support)

Giai đoạn này giúp bạn không bị "kẹt" khi gặp lỗi. Có hai file chính bạn cần để bên cạnh:

### 1. QUICK_REFERENCE.md (Bạn đường kỹ thuật)
Đây là bản "phao thi" (Cheat Sheet) chứa tất cả các câu lệnh quan trọng:
*   **Docker**: Lệnh build, run, debug, cleanup (dọn dẹp bộ nhớ).
*   **Railway/Render**: Lệnh triển khai và quản lý dịch vụ cloud.
*   **Python Code**: Các đoạn code mẫu cho Health check, API Auth, Rate limiting...
*   **Environment**: Cách thiết lập file `.env` chuẩn.

### 2. TROUBLESHOOTING.md (Bác sĩ cấp cứu)
Khi code hoặc deployment của bạn bị lỗi, hãy tìm kiếm thông báo lỗi trong này.
*   **Lỗi Docker**: "Port already in use", "Daemon not running"...
*   **Lỗi Cloud**: "Build failed", "Application crashes"...
*   **Lỗi Bảo mật**: "401 Unauthorized" dù đã nhập đúng key...
*   **Lỗi Khác**: Kết nối Redis thất bại, RAM bị tràn...

---

## ✅ Bước 5: Hoàn Thiện & Nộp Bài (Delivery)

Trước khi gửi Repo cho giảng viên, hãy đối chiếu với file **`DAY12_DELIVERY_CHECKLIST.md`** để không mất điểm oan.

### Những file bắt buộc phải có:
1.  **`MISSION_ANSWERS.md`**: Chứa câu trả lời cho các bài tập nhỏ từ Part 1 đến Part 5.
2.  **`DEPLOYMENT.md`**: Chứa địa chỉ URL đang chạy Service của bạn và các lệnh để giảng viên test thử.
3.  **`app/`**: Thư mục chứa source code hoàn chỉnh của Part 6.
4.  **`Dockerfile` & `docker-compose.yml`**: Phải đúng chuẩn và chạy được.
5.  **`.env.example`**: Để giảng viên biết cần cài đặt những biến môi trường nào.

### Các tiêu chí chấm điểm (Rubric):
*   **Kỹ thuật (60đ)**: Agent chạy đúng, Docker tối ưu (size < 500MB), Bảo mật (Auth/Rate Limit/Cost Guard), Tin cậy (Health check/Graceful shutdown).
*   **Triển khai (10đ)**: Link URL trên Cloud phải truy cập được.
*   **Bài tập phụ (40đ)**: Hoàn thành các Exercise trong 5 phần đầu.

---

## 👨‍🏫 Dành Cho Giảng Viên: INSTRUCTOR_GUIDE.md
Nếu bạn là người hướng dẫn, file này cung cấp các script tự động để chấm điểm bài làm của sinh viên một cách nhanh chóng và công bằng.

---

## 🎉 Tổng Kết Lộ Trình
Đến đây, bạn đã nắm được toàn bộ quy trình từ lúc bắt đầu đọc lý thuyết đến lúc nộp bài thực hành Deployment Agent lên Cloud.

Bạn có muốn tôi hỗ trợ thực hiện trực tiếp bước nào đầu tiên không? Chẳng hạn như chạy thử **Bước 2: Quick Start**?
