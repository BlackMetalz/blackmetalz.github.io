# Nhét 1 app tĩnh vào path con của github.io

Mục tiêu: có URL kiểu `https://blackmetalz.github.io/bcm-simulator/`
(giống `https://kyle-law.github.io/bcm-simulator/`).

Có 2 cách, chọn 1.

---

## Cách 1 — Repo riêng (recommend)

GitHub tự serve mọi repo bật Pages tại `https://<user>.github.io/<tên-repo>/`.
Tên repo = tên path, nên repo phải tên đúng `bcm-simulator`.

```bash
gh repo create BlackMetalz/bcm-simulator --public --clone
cd bcm-simulator
# copy app vào, BẮT BUỘC có index.html ở root repo
touch .nojekyll          # chặn Jekyll, nếu không folder/file có _ sẽ bị bỏ
git add . && git commit -m "init" && git push
```

Settings → Pages → Source: **Deploy from a branch** → branch `master` (hoặc `main`) → folder `/ (root)` → Save.
Đợi ~1 phút, vào `https://blackmetalz.github.io/bcm-simulator/`.

Ưu: tách hẳn khỏi blog, build blog không đụng tới, sửa app không rebuild cả site.
Nhược: thêm 1 repo phải quản.

---

## Cách 2 — Nhét vào repo blog này (Pelican)

### Lưu ý trước khi làm
`publishconf.py` có `DELETE_OUTPUT_DIRECTORY = True` → thả file trực tiếp vào `output/`
là **mất sạch** mỗi lần build. Phải đi qua `content/`.

### Các bước

1. Bỏ app vào `content/bcm-simulator/`, có `index.html` ở trong đó:

```
content/
  bcm-simulator/
    index.html
    app.js
    style.css
```

2. Khai báo nó là static path trong `pelicanconf.py`:

```python
STATIC_PATHS = ['static', 'images', 'bcm-simulator']
```

Pelican copy static path giữ nguyên cấu trúc thư mục →
`content/bcm-simulator/index.html` ra `output/bcm-simulator/index.html`.

3. Build local kiểm tra:

```bash
source venv/bin/activate
pelican content && pelican --listen
# mở http://localhost:8000/bcm-simulator/
```

4. Push lên `master`. GitHub Action (`.github/workflows/`) build rồi deploy `output/`
sang branch `gh-pages`, action tự tạo `.nojekyll` nên path con không bị Jekyll ăn.

Ưu: 1 repo, 1 pipeline.
Nhược: sửa app = rebuild cả blog; code app lẫn với content bài viết.

---

## Troubleshoot nhanh

| Lỗi | Nguyên nhân thường gặp |
|---|---|
| 404 ở path con | thiếu `index.html` ngay tại folder đó, hoặc Pages chưa bật / chọn sai branch |
| CSS/JS 404, HTML load được | app dùng đường dẫn tuyệt đối `/app.js`. Phải đổi sang relative `./app.js` vì app nằm ở subpath |
| File/folder có dấu `_` bị mất | thiếu `.nojekyll` ở root của branch được serve |
| Sửa rồi mà web chưa đổi | Action chưa xong, hoặc cache browser — thử hard reload |
