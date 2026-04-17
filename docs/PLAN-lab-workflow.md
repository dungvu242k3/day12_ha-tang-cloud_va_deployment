# PLAN: Quy Trình Thực Hành Day 12 Lab

Tài liệu này hệ thống lại quy trình làm bài Lab "Day 12 — Deployment: Đưa Agent Lên Cloud" một cách khoa học nhất, dựa trên cấu trúc các tài liệu đi kèm.

## 🔴 Mục Tiêu
Giúp sinh viên nắm rõ thứ tự đọc tài liệu và thực hiện các bước thực hành để hoàn thành Lab một cách hiệu quả nhất.

## 🗺️ Lộ Trình Đọc & Làm (Step-by-Step)

### Bước 0: Tổng Quan (10 phút)
*   **File cần đọc**: [README.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/README.md)
*   **Mục tiêu**: Nắm được cấu trúc thư mục, yêu cầu hệ thống và các section chính của khóa học.

### Bước 1: Tư Duy & Lộ Trình (15 phút)
*   **File cần đọc**: [LEARNING_PATH.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/LEARNING_PATH.md)
*   **Mục tiêu**: Hiểu tại sao cần Deployment, sự khác biệt giữa Localhost và Production, và những kỹ năng sẽ đạt được sau Lab.

### Bước 2: Thử Nghiệm Nhanh (Tùy chọn - 30 phút)
*   **File cần đọc**: [QUICK_START.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/QUICK_START.md)
*   **Mục tiêu**: Chạy thử một Agent cơ bản, Dockerize và Deploy lên Cloud (Railway) trong thời gian ngắn nhất để lấy cảm hứng.

### Bước 3: Thực Hành Chi Tiết (3-4 giờ)
*   **File trọng tâm**: [CODE_LAB.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/CODE_LAB.md)
*   **Quy trình thực hiện**:
    1.  **Part 1: Localhost vs Production**: Học cách dùng Environment Variables và Health checks.
    2.  **Part 2: Docker Containerization**: Đóng gói Agent, học Multi-stage build để tối ưu dung lượng.
    3.  **Part 3: Cloud Deployment**: Đưa Agent lên Railway hoặc Render.
    4.  **Part 4: API Security**: Thêm Authentication (API Key/JWT), Rate Limiting và Cost Guard.
    5.  **Part 5: Scaling & Reliability**: Thiết kế Stateless, Health check nâng cao và Load Balancing.
    6.  **Part 6: Final Project**: Tự xây dựng một Production Agent hoàn chỉnh từ đầu.

### Bước 4: Hoàn Thiện & Nộp Bài (30 phút)
*   **File đối chiếu**: [DAY12_DELIVERY_CHECKLIST.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/DAY12_DELIVERY_CHECKLIST.md)
*   **Mục tiêu**: Kiểm tra lại các file cần nộp (`MISSION_ANSWERS.md`, `DEPLOYMENT.md`, source code) và các tiêu chí kỹ thuật (image size < 500MB, auth, rate limit...).

## 🛠️ Công Cụ Hỗ Trợ Trong Khi Làm
*   **Tra cứu lệnh**: [QUICK_REFERENCE.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/QUICK_REFERENCE.md) (Cheat sheet cho Docker, Railway, Python...).
*   **Giải quyết lỗi**: [TROUBLESHOOTING.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/TROUBLESHOOTING.md) (Khi gặp lỗi Docker, Cloud, Auth...).

## 👨‍🏫 Dành Cho Giảng Viên (Nếu cần)
*   **Cách chấm điểm**: [INSTRUCTOR_GUIDE.md](file:///c:/Users/dungv/day12_ha-tang-cloud_va_deployment/INSTRUCTOR_GUIDE.md)

---

## Sau khi xem kế hoạch này:
- Bạn có muốn tôi đi sâu vào chi tiết nội dung của bất kỳ "Part" nào trong `CODE_LAB.md` không?
- Bạn có cần tôi hướng dẫn cách thiết lập môi trường (Python, Docker) trước khi bắt đầu không?
