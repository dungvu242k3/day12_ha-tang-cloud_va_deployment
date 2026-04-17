# PLAN: Chi Tiết Bước 3 - Thực Hành Chi Tiết (Code Lab)

Tài liệu này chi tiết hóa lộ trình thực hành trọng tâm của khóa học: **CODE_LAB.md**. Đây là phần tốn nhiều thời gian nhất (3-4 giờ) nhưng sẽ giúp bạn trở thành một chuyên gia Deployment thực thụ.

## 🗺️ Lộ Trình 6 Phần (6 Parts)

### 🔴 Part 1: Localhost vs Production (30 Phút)
*   **Mục tiêu**: Hiểu tại sao code chạy trên máy mình lại lỗi khi đưa lên server.
*   **Kiến thức chính**:
    *   Học nguyên tắc **12-Factor App**.
    *   Thay thế các giá trị "Hardcoded" (như API Key, Port) bằng Biến môi trường (`Environment Variables`).
    *   Thêm `Health Check endpoint` để hệ thống tự giám sát sức khỏe.
*   **Thực hành**: So sánh bản `develop` và `production` trong thư mục `01-localhost-vs-production`.

### 🔴 Part 2: Docker Containerization (45 Phút)
*   **Mục tiêu**: Đóng gói ứng dụng để "Chạy ở đâu cũng giống nhau".
*   **Kiến thức chính**:
    *   Viết `Dockerfile`.
    *   Sử dụng `Multi-stage builds` để giảm dung lượng Image (ví dụ từ 1GB xuống còn 150MB).
    *   Dùng `Docker Compose` để chạy cùng lúc nhiều dịch vụ (Agent + Redis + Nginx).
*   **Thực hành**: Build và tối ưu hóa Image trong thư mục `02-docker`.

### 🔴 Part 3: Cloud Deployment (45 Phút)
*   **Mục tiêu**: Đưa ứng dụng lên Internet để mọi người truy cập.
*   **Kiến thức chính**:
    *   Cách sử dụng Railway/Render CLI.
    *   Cấu hình Biến môi trường trên Cloud Dashboard.
    *   Thiết lập CI/CD (tự động cập nhật khi bạn sửa code).
*   **Thực hành**: Tự tay đưa Agent lên một địa chỉ URL thực tế.

### 🔴 Part 4: API Security (40 Phút)
*   **Mục tiêu**: Bảo mật và kiểm soát chi phí.
*   **Kiến thức chính**:
    *   Xác thực người dùng bằng API Key hoặc JWT.
    *   **Rate Limiting**: Ngăn chặn spam request.
    *   **Cost Guard**: Theo dõi và giới hạn ngân sách sử dụng LLM.
*   **Thực hành**: Cài đặt lớp bảo mật trong thư mục `04-api-gateway`.

### 🔴 Part 5: Scaling & Reliability (40 Phút)
*   **Mục tiêu**: Hệ thống chạy ổn định và chịu tải tốt.
*   **Kiến thức chính**:
    *   Thiết kế **Stateless**: Tuyệt đối không lưu dữ liệu trong RAM của máy chủ, mà chuyển sang Redis/Database.
    *   **Graceful Shutdown**: Tắt máy chủ một cách "nhẹ nhàng", không làm đứt request đang xử lý của người dùng.
    *   **Load Balancing**: Chia đều người dùng cho nhiều máy chủ Agent.

### 🔴 Part 6: Final Project (60 Phút)
*   **Nhiệm vụ**: Xây dựng một Agent hoàn chỉnh từ con số 0, kết hợp TẤT CẢ các kỹ năng trên.
*   **Yêu cầu nộp bài**: Agent phải chạy ổn định, có bảo mật, có container và đã được Deploy lên Cloud thành công.

---

## 💡 Ghi Chú Quan Trọng
Trong suốt quá trình làm `CODE_LAB.md`, nếu gặp lỗi, bạn hãy mở ngay file **`TROUBLESHOOTING.md`** để tìm cách khắc phục.

---

## Bước Tiếp Theo:
Bạn muốn tôi đi sâu vào chi tiết kỹ thuật của **Part nào trong 6 Part trên** không? Nếu không, tôi sẽ tiếp tục tóm tắt **Bước 4 (Hỗ trợ & Tra cứu)** cho bạn.
