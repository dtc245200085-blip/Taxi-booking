# Hệ Thống Đặt Xe Taxi Online (Taxi Booking System)

- **Môn học:** Triển khai và Quản trị Hệ thống Phần mềm
- **Sinh viên thực hiện:** Hoàng Ngọc Huy
- **Lớp:** CNTT K23C
- **Đề tài:** Đề 22 - Hệ thống Đặt xe / Taxi Booking

---

## ARCHITECTURE & STACK
Hệ thống được đóng gói và triển khai hoàn toàn bằng **Docker Compose** bao gồm 8 dịch vụ:
1. **taxi-web**: Flask Web Application (Python 3.10)
2. **taxi-db**: PostgreSQL Database v15
3. **taxi-pgadmin**: pgAdmin 4 - Công cụ quản lý PostgreSQL
4. **taxi-nginx**: Nginx Reverse Proxy
5. **taxi-prometheus**: Prometheus Metrics Server
6. **taxi-grafana**: Grafana Visualization Dashboard
7. **taxi-loki**: Grafana Loki Centralized Log Store
8. **taxi-promtail**: Promtail Log Collector Agent

---

## HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG

### 1. Khởi động tất cả các dịch vụ
docker compose up -d --build

### 2. Truy cập các dịch vụ
- **Web App Đặt Xe:** http://localhost hoặc [http://192.168.133.128](http://192.168.133.128)
- **pgAdmin (CSDL):** [http://192.168.133.128:5050](http://192.168.133.128:5050) (admin@taxi.com / adminpass123)
- **Prometheus:** [http://192.168.133.128:9090](http://192.168.133.128:9090)
- **Grafana:** [http://192.168.133.128:3000](http://192.168.133.128:3000) (admin / adminpass123)
- **Loki:** [http://192.168.133.128:3100](http://192.168.133.128:3100)

---

## HARDENING & BẢO MẬT
- **Isolation:** Tách biệt hai mạng backend và frontend trong Docker.
- **Proxying:** Che giấu ứng dụng backend Flask phía sau Nginx Reverse Proxy.
- **Authentication:** Thiết lập mật khẩu quản trị cho PostgreSQL, pgAdmin và Grafana.
