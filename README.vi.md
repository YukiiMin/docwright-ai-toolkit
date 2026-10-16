<p align="center">
  <img src="https://raw.githubusercontent.com/YukiiMin/docwright-ai-toolkit/main/assets/docwright-ai-toolkit-icon.png" width="128" height="128" alt="Docwright AI Toolkits Icon" />
</p>

# Docwright AI Toolkits (`docwright-ai-toolkit`)

<p align="center">
  <strong>Bộ Công Cụ Kỹ Thuật Tài Liệu Word (DOCX) &amp; Bảng Tính Excel (XLSX) Chuẩn Xác Dành Cho AI Agents, Lập Trình Viên Python &amp; CLI.</strong><br>
  <em>Khởi tạo, trích xuất, chỉnh sửa và kiểm định tài liệu doanh nghiệp qua 51 công cụ chuẩn hóa — gọi trực tiếp qua MCP Server, import thư viện Python SDK, hoặc chạy CLI.</em>
</p>

<p align="center">
  <a href="https://docwright-ai-toolkit.vercel.app/vi/"><img src="https://img.shields.io/badge/docs-vercel_live-000000?style=for-the-badge&logo=vercel" alt="Tài liệu Trực tuyến" /></a>
  <a href="https://pypi.org/project/docwright-ai-toolkit/"><img src="https://img.shields.io/pypi/v/docwright-ai-toolkit?style=for-the-badge&color=38bdf8" alt="Phiên bản PyPI" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-BSL--1.1-blue?style=for-the-badge" alt="Giấy phép" /></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Hỗ trợ Python" />
</p>

<p align="center">
  <a href="https://docwright-ai-toolkit.vercel.app/vi/"><strong>📖 Cổng Tài Liệu Trực Tuyến Chính Thức</strong></a> &bull;
  <a href="#cài-đặt-nhanh">Cài đặt nhanh</a> &bull;
  <a href="#3-phương-thức-sử-dụng">3 Phương thức</a> &bull;
  <a href="#cài-đặt-1-click-cho-ai-ide">Cấu hình AI IDE</a> &bull;
  <a href="#danh-mục-đầy-đủ-51-công-cụ">51 Công cụ</a> &bull;
  <a href="#bản-quyền--điều-khoản-thương-mại">Bản quyền</a>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> | <a href="README.vi.md"><strong>Tiếng Việt</strong></a>
</p>

<div align="center">

```bash
pip install docwright-ai-toolkit
```

👉 **[Xem Hướng Dẫn Cài Đặt Môi Trường & Thiết Lập AI IDE](https://docwright-ai-toolkit.vercel.app/vi/getting-started/installation/)**

</div>

---

## Docwright Giải Quyết Bài Toán Gì?

**Docwright AI Toolkits** cung cấp nền tảng kỹ thuật chuyên sâu để khởi tạo, đọc dữ liệu, chỉnh sửa và kiểm định **tài liệu Word (`.docx`)** cùng **bảng tính Excel (`.xlsx`)**:

1. **Tự Động Bảo Vệ Bảng Biểu Nhiều Trang Trên Word**: Khóa hàng không bị cắt ngang khi sang trang mới, tự động lặp lại dòng tiêu đề bảng ở đầu mỗi trang và cố định dòng tiêu đề mục đi liền với dữ liệu bên dưới.
2. **Chuẩn Hóa Biểu Mẫu Jinja2 & Vá Văn Bản Giữ Nguyên Định Dạng**: Tự động hàn gắn các biến `{{ bien_so }}` bị trình soạn thảo Word tách rời và thay thế nội dung chữ mà vẫn bảo toàn phông chữ, cỡ chữ, màu sắc của biểu mẫu gốc.
3. **Tái Tạo Biểu Mẫu Word 1:1 Từ PDF Scan**: Đo đạc chính xác lưới bảng từ ảnh scan PDF bằng thị giác máy tính (`docx.measure_pdf_layout`), điền nội dung theo mã ô (`c0_0`, `c0_1`, ...) và xuất ra file `.docx` chỉnh sửa được.
4. **Đọc Excel Tiết Kiệm Token & Chèn Khối 2D Tự Động Dịch Công Thức**: Trích xuất bảng tính lớn thành mô hình 3 tầng để truy vấn từng phần không làm tràn ngữ cảnh AI, phát hiện nhiều bảng độc lập (**Table Islands**) trên cùng một sheet và chèn dòng mới đồng thời tự động mở rộng vùng công thức `=SUM(...)`.

---

## Tổng Quan Các Mô-đun (51 Công Cụ)

| Mô-đun | Số Lượng Tool | Năng Lực Cốt Lõi |
| :--- | :--- | :--- |
| **Mô-đun Word (`docx.*`)** | **19 Tools** | Khởi tạo tài liệu từ `DocSpec`, chuẩn hóa & điền biểu mẫu Jinja2, vá văn bản bảo toàn định dạng, trích xuất cấu trúc 2 tầng, tái tạo biểu mẫu từ PDF scan và kiểm định 8 tiêu chí chất lượng. |
| **Mô-đun Excel (`xlsx.*`)** | **31 Tools** | Trích xuất dữ liệu 3 tầng (`extract`/`query`), nhận diện đảo bảng 2D (`detect_tables`), chèn khối tự động dịch vùng công thức (`mutate_block`), tính toán lại qua LibreOffice (`recalc`) và kiểm định 13 tiêu chí chất lượng. |
| **Mô-đun Chung (`common.*`)** | **1 Tool** | Nén gọn JSON và trích xuất nhánh con (`common.compact_json`) giúp tiết kiệm tối đa lượng token tiêu thụ của AI. |

---

## Cài Đặt Nhanh

```bash
# 1. Cài đặt gói từ PyPI
pip install docwright-ai-toolkit

# 2. Liệt kê toàn bộ 51 công cụ đã đăng ký (19 docx.*, 31 xlsx.*, 1 common.*)
docwright list

# 3. Xem JSON schema đầu vào và ví dụ mẫu của bất kỳ công cụ nào
docwright schema docx.build_document
docwright schema xlsx.mutate_block
```

---

## 3 Phương Thức Sử Dụng

### Phương Thức 1: Gọi Trực Tiếp Qua MCP Server (`docwright-mcp`)
Kết nối `docwright-mcp` vào AI IDE (Claude Code, Cursor, Google Antigravity, Claude Desktop, Windsurf). AI Agent có thể gọi trực tiếp toàn bộ 51 công cụ qua tên chuẩn (`docx.build_document`) hoặc tên gạch dưới (`docx_build_document`).

### Phương Thức 2: Import Bộ Thư Viện Python SDK (`doctools.api` & `doctools.operations`)
Import trực tiếp vào mã nguồn Python, dịch vụ backend hoặc script tự động hóa của bạn:

```python
from doctools.api import (
    load_workbook_model,
    read_table,
    TableIslandDetector,
    xlsx_detect_tables,
    xlsx_mutate_block,
    compact_json,
)
from doctools.operations.docx import docx_build_document, docx_patch, docx_validate
from doctools.operations.xlsx import xlsx_recalc, xlsx_validate

# Ví dụ: Chèn 2 dòng mới vào bảng Excel và tự động mở rộng công thức =SUM(...)
res = xlsx_mutate_block(
    file_ref="data/ngan_sach_quy.xlsx",
    output_path="data/ngan_sach_quy_q4.xlsx",
    sheet_name="Summary",
    operation="insert_rows",
    start_row=5,
    count=2,
    data=[
        ["Cụm máy chủ AI", 14500, 16000],
        ["Hệ thống kiểm thử tự động", 3200, 3500],
    ],
)
print("Thành công:", res.success)
```

### Phương Thức 3: Chạy Lệnh CLI Nhanh (`docwright`)
Sử dụng trực tiếp trên Terminal hoặc tích hợp vào quy trình CI/CD:

```bash
# Chạy công cụ với file --spec hoặc chuỗi --json
docwright docx.build_document --spec report_spec.json
docwright docx.validate --json '{"file_ref": "output/report.docx"}'

# Lệnh tiện ích nén gọn JSON tiết kiệm token & khởi tạo Profile YAML
docwright compact-json extracted_model.json --path sheets.Summary --max-depth 3 -o compact.json
docwright profile-scaffold template.xlsx --output profile.yaml
```

---

## Cài Đặt 1-Click Cho AI IDE

### 1. Claude Code CLI (Anthropic)
```bash
claude mcp add docwright -- docwright-mcp
```

### 2. Cursor IDE (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp",
      "args": []
    }
  }
}
```

### 3. Google Antigravity IDE (`.agents/mcp_config.json`)
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp",
      "args": []
    }
  }
}
```

### 4. Claude Desktop (`claude_desktop_config.json`) & Windsurf (`~/.codeium/windsurf/mcp_config.json`)
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp",
      "args": []
    }
  }
}
```

Các file cấu hình mẫu cho mọi nền tảng (bao gồm **Continue.dev**, **Zed Editor**, **Cline / Roo Code**, và **Codex CLI**) có sẵn tại thư mục [`configs/`](configs/).

---

## Danh Mục Đầy Đủ 51 Công Cụ

### 1. Mô-đun Word (`docx.*` — 19 Công Cụ)
| # | Tên Công Cụ | Chức Năng Chính |
| :--- | :--- | :--- |
| 1 | `docx.inspect_structure` | Khảo sát đoạn văn, bảng biểu, kiểu dáng (styles) và thiết lập trang của tệp `.docx`. |
| 2 | `docx.validate` | Kiểm định 8 tiêu chí cấu trúc và chuẩn OpenXML cho tài liệu Word. |
| 3 | `docx.extract_media` | Trích xuất toàn bộ hình ảnh và tài nguyên đa phương tiện nhúng trong file Word. |
| 4 | `docx.to_markdown` | Chuyển đổi tài liệu Word sang Markdown sạch để đọc hiểu và tóm tắt nhanh. |
| 5 | `docx.render_template` | Điền dữ liệu JSON vào biểu mẫu Word Jinja2 giữ nguyên định dạng doanh nghiệp. |
| 6 | `docx.build_document` | Khởi tạo tài liệu `.docx` hoàn chỉnh từ đặc tả cấu trúc JSON `DocSpec`. |
| 7 | `docx.patch` | Vá và thay thế văn bản giữ nguyên phông chữ, màu sắc và định dạng đoạn văn. |
| 8 | `docx.merge` | Ghép nối nhiều tệp `.docx` thành một tài liệu thống nhất bảo toàn định dạng. |
| 9 | `docx.lint_template` | Kiểm tra lỗi cú pháp hoặc thẻ Jinja bị đứt gãy trên biểu mẫu `.docx`. |
| 10 | `docx.normalize_template` | Hàn gắn tự động các thẻ `{{ ... }}` bị trình soạn thảo Word cắt vụn. |
| 11 | `docx.register_template` | Đăng ký biểu mẫu `.docx` vào danh mục quản lý cục bộ. |
| 12 | `docx.list_templates` | Liệt kê danh sách các biểu mẫu Word đã đăng ký. |
| 13 | `docx.get_template_manifest` | Xem danh sách các biến cần điền của một biểu mẫu Word đã đăng ký. |
| 14 | `docx.update_fields` | Cập nhật các trường tự động trong Word (Mục lục, số trang). |
| 15 | `docx.extract` | Trích xuất mô hình cấu trúc 2 tầng của tài liệu Word vào bộ nhớ `FileStore`. |
| 16 | `docx.query` | Truy vấn nội dung theo mục, đoạn văn hoặc bảng từ mô hình đã trích xuất. |
| 17 | `docx.measure_pdf_layout` | Đo đạc hình học lưới bảng, tỷ lệ cột và tọa độ ô từ tài liệu PDF scan. |
| 18 | `docx.populate_layout_text` | Điền văn bản vào các ô trong `LayoutSpec` theo mã định danh `cell_id` (`c0_0`). |
| 19 | `docx.compile_layout_spec` | Biên dịch `LayoutSpec` đã điền chữ thành tệp `.docx` hoàn chỉnh theo tỷ lệ 1:1. |

### 2. Mô-đun Excel (`xlsx.*` — 31 Công Cụ)
| # | Tên Công Cụ | Chức Năng Chính |
| :--- | :--- | :--- |
| 20 | `xlsx.preflight` | Quét nhanh danh sách sheet, kích thước vùng dữ liệu, vùng gộp ô và số lượng công thức. |
| 21 | `xlsx.inspect` | Khảo sát chi tiết cấu trúc bảng, dòng tiêu đề và thông tin các sheet trong workbook. |
| 22 | `xlsx.coverage_report` | Tạo báo cáo mật độ dữ liệu và độ phủ công thức trên toàn bộ các sheet. |
| 23 | `xlsx.analyze_formulas` | Phân tích chuỗi phụ thuộc công thức, danh sách hàm sử dụng và tham chiếu chéo. |
| 24 | `xlsx.describe_formats` | Trích xuất mã màu, phông chữ, khung viền và định dạng số từ các ô mẫu. |
| 25 | `xlsx.function_catalog` | Tra cứu danh mục hàm Excel được hỗ trợ và quy tắc kiểm tra. |
| 26 | `xlsx.mutate` | Cập nhật giá trị và công thức từng ô bảo toàn định dạng mẫu và logo trang bìa. |
| 27 | `xlsx.recalc` | Tính toán lại giá trị công thức qua LibreOffice chạy ngầm và lưu vào bộ nhớ đệm XML (`<v>`). |
| 28 | `xlsx.validate` | Kiểm định toàn diện bảng tính qua 13 tiêu chí chất lượng tự động. |
| 29 | `xlsx.diff` | So sánh 2 bảng tính Excel và báo cáo chi tiết sự khác biệt về giá trị, công thức, cấu trúc. |
| 30 | `xlsx.export_legacy_xls` | Xuất hoặc chuyển đổi dữ liệu tương thích với định dạng `.xls` cũ. |
| 31 | `xlsx.build` | Khởi tạo mới bảng tính `.xlsx` nhiều sheet từ đặc tả JSON. |
| 32 | `xlsx.repair` | Tự động sửa các lỗi cấu trúc phổ biến như đứt nét khung viền vùng gộp ô. |
| 33 | `xlsx.register_template` | Đăng ký bảng tính mẫu `.xlsx` vào kho lưu trữ template. |
| 34 | `xlsx.lint_template` | Kiểm tra biểu mẫu Excel để phát hiện ô tổng hợp gõ số chết hoặc lỗi tham chiếu. |
| 35 | `xlsx.list_templates` | Liệt kê toàn bộ các biểu mẫu Excel đã đăng ký. |
| 36 | `xlsx.set_format` | Áp dụng phông chữ, màu nền, khung viền và định dạng số cho vùng ô mục tiêu. |
| 37 | `xlsx.set_validation` | Thiết lập danh sách chọn (dropdown) và ràng buộc dữ liệu đầu vào trên Excel. |
| 38 | `xlsx.set_conditional_format` | Thiết lập định dạng có điều kiện (Conditional Formatting) cho vùng dữ liệu. |
| 39 | `xlsx.copy_sheet` | Sao chép nguyên vẹn một trang tính (sheet) giữ nguyên định dạng và vùng in. |
| 40 | `xlsx.extract` | Trích xuất bảng tính thành mô hình trung thực 3 tầng lưu trong `FileStore`. |
| 41 | `xlsx.query` | Truy vấn lát cắt dữ liệu theo vùng ô hoặc bảng từ mô hình đã trích xuất. |
| 42 | `xlsx.verify_extract` | Đối chiếu độ chính xác của dữ liệu trích xuất qua mã băm cột tốc độ cao. |
| 43 | `xlsx.classify_layout` | Tự động phân loại kiểu bố cục trang tính (bảng ma trận, biểu mẫu key-value, đa bảng). |
| 44 | `xlsx.profile_scaffold` | Sinh tự động cấu hình trích xuất YAML/JSON từ bảng tính mẫu. |
| 45 | `xlsx.semantic_extract` | Trích xuất ngữ nghĩa tự động các bảng dữ liệu và cặp nhãn - giá trị. |
| 46 | `xlsx.detect_tables` | Phát hiện tọa độ các Đảo Bảng 2D (Table Islands) độc lập nằm trên cùng một sheet. |
| 47 | `xlsx.mutate_block` | Chèn hoặc cập nhật khối dòng/cột 2D kèm tự động dịch chuyển vùng công thức AST. |
| 48 | `xlsx.shift_block` | Dịch chuyển khối ô chữ nhật theo phương ngang/dọc và cập nhật công thức phụ thuộc. |
| 49 | `xlsx.batch_interact` | Thực thi chuỗi nhiều thao tác biến đổi bảng tính trong một giao dịch duy nhất. |
| 50 | `xlsx.bulk_ingest` | Nạp luồng dữ liệu lớn tốc độ cao vào biểu mẫu Excel. |

### 3. Mô-đun Tiện Ích Chung (`common.*` — 1 Công Cụ)
| # | Tên Công Cụ | Chức Năng Chính |
| :--- | :--- | :--- |
| 51 | `common.compact_json` | Nén gọn chuỗi/file JSON và trích xuất nhánh con giúp tiết kiệm token cho AI. |

---

## Bản Quyền & Điều Khoản Thương Mại

Docwright AI Toolkits được phát hành theo giấy phép **Business Source License 1.1 (BSL 1.1)**.
- **Miễn phí cho Cá nhân & Phát triển Nội bộ**: Miễn phí hoàn toàn cho lập trình viên cá nhân, quy trình tự động hóa nội bộ doanh nghiệp, nghiên cứu học thuật, dự án mã nguồn mở và tích hợp trực tiếp với các AI IDE/Agent.
- **Điều khoản Thương mại SaaS**: Việc đóng gói động cơ lõi để kinh doanh dưới dạng dịch vụ đám mây thu phí (Hosted Multi-tenant SaaS) cho bên thứ ba yêu cầu giấy phép thương mại riêng từ tác giả.
