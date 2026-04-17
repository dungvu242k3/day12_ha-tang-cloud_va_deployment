# PLAN: Triển Khai Lên Cloud Qua GitHub (Vượt Rào Security)

Kế hoạch này giúp bạn đưa Agent lên Railway mà không cần dùng lệnh `railway up` (vốn đang bị Security trên máy bạn chặn). Chúng ta sẽ dùng GitHub làm cầu nối.

## 🔴 Mục Tiêu
Triển khai thành công Agent lên Railway bằng cách kết nối trực tiếp GitHub với Railway. Cách này giúp bạn **vượt qua hoàn toàn** thông báo lỗi Security khi dùng lệnh `railway up` trên máy tính cá nhân.

## 🗺️ Lịch sử nghiên cứu (Section 3 README)
Theo `03-cloud-deployment/README.md`, Railway hỗ trợ chế độ **"Kết nối GitHub → Auto deploy"**. Điều này cực kỳ hữu ích khi môi trường local (máy của bạn) bị chặn kết nối CLI. Chúng ta sẽ tận dụng cấu hình sẵn có trong folder `03-cloud-deployment/railway` (có file `railway.toml` chuẩn).

## 🛠️ Bước 1: Chuẩn bị Code trên máy cá nhân
Chúng ta sẽ chuẩn bị để đẩy toàn bộ dự án lên GitHub, nhưng Railway sẽ được cấu hình để chạy vào thư mục `03-cloud-deployment/railway`.

### Thao tác:
1.  Mở Terminal tại thư mục gốc của dự án.
2.  Kiểm tra xem file `.gitignore` đã có chưa (để tránh đẩy các file rác hoặc `.env` lên mạng).
3.  Thực hiện commit các thay đổi (nếu có):
    ```bash
    git add .
    git commit -m "Prepare for Railway deployment via GitHub"
    ```

## 🌐 Bước 2: Tạo Repository trên GitHub
Bạn cần thực hiện thao tác này trên trình duyệt:
1.  Truy cập [github.com](https://github.com) và đăng nhập.
2.  Tạo một **New Repository** (đặt tên là `day12-ai-agent`). Bạn có thể để chế độ **Private** cho an toàn.
3.  Copy địa chỉ của Repo đó (dạng `https://github.com/v-user/day12-ai-agent.git`).

## 🚀 Bước 3: Đẩy Code lên GitHub
Quay lại Terminal và chạy các lệnh sau (thay URL bằng link của bạn):
```bash
git remote add origin-deploy <URL_CỦA_BẠN>
git push -u origin-deploy main
```

## 🚉 Bước 4: Kết nối Railway với GitHub
Thực hiện trên trình duyệt tại [railway.app](https://railway.app):
1.  Đăng nhập vào Railway bằng tài khoản GitHub.
2.  Nhấn **New Project** -> **Deploy from GitHub repo**.
3.  Chọn Repo `day12-ai-agent` bạn vừa tạo.
4.  Railway sẽ hỏi về thư mục gốc, bạn có thể chọn **Root** hoặc cấu hình trong phần Variables.

## ⚙️ Bước 5: Cấu hình Biến Môi Trường & Security (Bypass CLI)
Vì Security của máy bạn chặn lệnh `railway variables set`, chúng ta sẽ cấu hình **trực tiếp trên Web Dashboard** của Railway:
1.  Vào dự án của bạn trên Railway web.
2.  Chọn Tab **Variables**.
3.  Thêm biến `PORT` = `8000`.
4.  Thêm biến `AGENT_API_KEY` (mật mã của bạn).
5.  Railway sẽ tự động Re-deploy. Do có file `railway.toml` trong code, Railway sẽ biết cách chạy lệnh `uvicorn app:app --host 0.0.0.0 --port $PORT` mà không cần bạn phải can thiệp từ máy local.

## ✅ Kiểm Tra
Sau khi Railway báo thành công, bạn lấy URL công khai và kiểm tra bằng trình duyệt hoặc `curl`.

---

**Bạn có muốn tôi bắt đầu thực hiện Bước 1 (Commit code) cho bạn không?**
