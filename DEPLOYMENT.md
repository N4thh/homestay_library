# Hướng dẫn Deploy Horin Library lên Vercel

## Vấn đề CSS đã được khắc phục

### Các thay đổi đã thực hiện:

1. **Cập nhật vercel.json**:
   - Thêm MIME type cho CSS files
   - Cấu hình cache headers phù hợp
   - Tối ưu hóa routing cho static files

2. **Cải thiện app.py**:
   - Thêm MIME type detection cho static files
   - Cấu hình cache headers động
   - Fallback cho missing images

3. **Tối ưu hóa base.html**:
   - Thêm CSS loading fallback
   - Preload critical CSS
   - JavaScript để kiểm tra CSS loading

4. **Cập nhật dependencies**:
   - Thêm gunicorn cho production
   - Cập nhật Python version lên 3.11

### Cách test CSS:

1. Deploy lên Vercel
2. Truy cập `/test-css` để kiểm tra CSS loading
3. Nếu thấy nền xanh lá = CSS hoạt động
4. Nếu thấy nền đỏ = CSS chưa load được

### Troubleshooting:

1. **CSS không load**:
   - Kiểm tra console browser
   - Xem network tab trong DevTools
   - Đảm bảo file CSS tồn tại trong static/css/

2. **Cache issues**:
   - Hard refresh (Ctrl+F5)
   - Clear browser cache
   - Kiểm tra Vercel cache settings

3. **MIME type issues**:
   - Kiểm tra response headers
   - Đảm bảo Content-Type: text/css

### Deploy commands:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### File structure quan trọng:

```
homestay_library/
├── api/
│   └── index.py          # Vercel entry point
├── static/
│   ├── css/
│   │   ├── style.css     # CSS file 1
│   │   └── style-v2.css  # CSS file 2 (main)
│   ├── js/
│   └── images/
├── templates/
├── vercel.json           # Vercel config
├── requirements.txt      # Python dependencies
└── runtime.txt          # Python version
```

### Monitoring:

- Kiểm tra Vercel logs
- Monitor performance metrics
- Test trên nhiều browsers
- Kiểm tra mobile responsiveness 