# Press Kit เว็บ — วิธีใช้

เปิด `index.html` ในเบราว์เซอร์ได้เลย หน้าเว็บเป็นเอกสารพื้นขาว สลับ English/ไทยได้

## โครงสร้างไฟล์
- `index.html` — หน้า Press Kit
- `assets/screenshots/` — ภาพหน้าจอ 1920×1080 (12 ภาพ)
- `assets/store/` — Capsule หน้าร้าน Steam + Key Art ไม่มีโลโก้ + แบนเนอร์ Lineup
- `assets/cards/` — การ์ด 26 ใบ PNG พื้นโปร่งใส 1600×2240 (ไม่รวมการ์ด Money ที่ยังเป็น placeholder)
- `assets/logo/` — โลโก้ 2 ขนาด + ไอคอน 1024/512
- `assets/thumbs/` — ภาพย่อสำหรับแสดงในหน้า (ไม่ต้องแก้)
- `downloads/` — ZIP แยกหมวด + `ChaosTable_PressKit_All.zip` + `ChaosTable_Factsheet.txt`
- `build_presskit_page.py` — สคริปต์สร้าง `index.html` ใหม่ (`python build_presskit_page.py index.html`)

## แก้ข้อมูล
- วันวางขาย/ราคา: บล็อก `CONFIG` ท้าย `index.html` (หรือใน build_presskit_page.py)
- ข้อความ Factsheet ในไฟล์ดาวน์โหลด: แก้ `downloads/ChaosTable_Factsheet.txt` แล้วสร้าง ZIP ใหม่
- ถ้าเปลี่ยนภาพ ต้องสร้าง ZIP และภาพย่อใหม่ด้วย (บอก Claude ให้ทำได้)

## ขึ้นเว็บ (GitHub Pages)
สร้าง repo ใหม่ (เช่น `chaostable-presskit`) อัปโหลดทุกอย่างในโฟลเดอร์ `web/` ไว้ที่ราก (~90 MB, ทุกไฟล์ต่ำกว่า 100 MB) แล้วเปิด Settings → Pages → Deploy from branch → `main` / root
ลิงก์จะเป็น `https://tanadol-mounoom.github.io/chaostable-presskit/`
