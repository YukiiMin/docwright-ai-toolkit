# Docwright AI Toolkits (`docwright-ai-toolkit`)

<p align="center">
  <strong>Bộ Plugin & MCP Server Văn Phòng & Biểu Đồ AI-Native Dành Cho Các AI Agents.</strong><br>
  <em>Bảo đảm toàn vẹn cấu trúc OpenXML, giữ nguyên định dạng mẫu và triệt tiêu lỗi hỏng file cho Word, Excel và Sơ đồ kỹ thuật.</em>
</p>

<p align="center">
  <a href="#tính-năng-cốt-lõi">Tính năng cốt lõi</a> &bull;
  <a href="#cài-đặt-nhanh">Cài đặt nhanh</a> &bull;
  <a href="#cấu-hình-ai-ide">Cấu hình AI IDE</a> &bull;
  <a href="#kiến-trúc-hệ-thống">Kiến trúc hệ thống</a> &bull;
  <a href="#danh-mục-công-cụ-mcp">Danh mục công cụ</a> &bull;
  <a href="#bản-quyền--giấy-phép">Bản quyền</a>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> | <a href="README.vi.md"><strong>Tiếng Việt</strong></a>
</p>

---

## Thực Trạng: Vì Sao AI Thường Làm Hỏng Tài Liệu Văn Phòng?

Khi các mô hình ngôn ngữ lớn (LLM) hiện nay tự sinh hoặc chỉnh sửa tài liệu văn phòng bằng các thư viện Python thông thường (`python-docx`, `openpyxl`), chúng liên tục gặp phải các lỗi nghiêm trọng:

- **Hỏng cấu trúc Word (DOCX Corruption)**: Việc thiếu thẻ đoạn văn `<w:p>` ở ô bảng rỗng vi phạm quy tắc lược đồ ECMA-376, khiến Microsoft Word hiện hộp thoại cảnh báo lỗi: *"Word found unreadable content"* và bắt buộc chạy chế độ phục hồi (Repair).
- **Rách bảng qua trang**: Bảng dài nhiều trang bị cắt ngang dòng chữ ngẫu nhiên do code AI không biết cách chèn thuộc tính cấm chẻ hàng `<w:cantSplit/>` và lặp lại dòng tiêu đề `<w:tblHeader/>`.
- **Hỏng công thức và mất đồ họa Excel**: Việc ghi đè dữ liệu trực tiếp làm đứt gãy đồ thị phụ thuộc công thức, biến công thức sống thành số tĩnh, và làm mất sạch hình ảnh, logo DrawingML hay biểu đồ có sẵn trong mẫu.
- **Băm nát kiểu dáng chữ**: Khi sửa một từ trong câu, việc gán lại văn bản làm mất toàn bộ các phân đoạn định dạng (Run styling), font chữ doanh nghiệp, màu sắc và thụt lề ban đầu.

**Docwright AI Toolkits** được xây dựng để giải quyết triệt để vấn đề này bằng cách thiết lập một tầng biên dịch tất định, có chốt chặn kiểm soát chuẩn OpenXML đặt giữa mô hình AI và định dạng nhị phân của tài liệu.

---

## Tính Năng Cốt Lõi

| Phân hệ | Tính năng nổi bật | Cam kết kỹ thuật & Chuẩn hóa |
|---|---|---|
| **Văn bản Word (DOCX)** | Trình biên dịch 2 luồng (Luồng A Jinja và Luồng B DocSpec DSL), cơ chế vá vi phẫu từng đoạn chữ (Surgical Run Splicer), module thị giác đo đạc lưới hình học (Document Vision). | Cưỡng chế trật tự thẻ chuẩn ECMA-376, cấm xé rách hàng bảng qua trang, bảo đảm 100% ô bảng kết thúc bằng đoạn văn hợp lệ. |
| **Bảng tính Excel (XLSX)** | Trình biến đổi khối 2D (2D Block Mutator), nhận diện đảo bảng độc lập (Table Island Detector), dịch chuyển công thức theo cây cú pháp trừu tượng (AST), mô hình trích xuất không mất mát L1/L2/L3. | 13 Cổng kiểm định phổ quát (`UG-01..13`), bảo tồn 100% công thức động, bảo vệ neo ảnh và hình vẽ DrawingML không bị đè lấp. |
| **Sơ đồ Kỹ thuật (Diagram)** | Sinh mã XML `mxGraphModel` chuẩn cho Draw.io, tự động định tuyến đường nối vuông góc (Orthogonal Routing), co giãn kích thước hình học động. | Cấu trúc phân cấp XML tự nhiên, không dùng định dạng chắp vá, kết xuất ảnh độ nét cao (high-DPI) không cần mở trình duyệt. |
| **Tích hợp Tác nhân AI** | Máy chủ giao thức ngữ cảnh mô hình (MCP STDIO Server), bộ điều phối dòng lệnh CLI hợp nhất, hợp đồng dữ liệu chuẩn Pydantic. | Tự động tương thích và chuẩn hóa tham số, lọc bỏ đối số bất hợp lệ, hệ thống báo cáo chẩn đoán nghiêm ngặt (Fail-Closed). |

---

## Bảng So Sánh Kỹ Thuật Trực Diện

| Tiêu chuẩn Đánh giá | Script AI Tự Viết (`python-docx` / `openpyxl`) | Các MCP Server Tài Liệu Thông Thường | Docwright AI Toolkits |
|---|---|---|---|
| **Tuân thủ chuẩn OpenXML ECMA-376** | Không (sinh thẻ tùy tiện) | Một phần (bọc thư viện thô) | **100% Cưỡng chế trật tự Canonical** |
| **Bảo vệ bảng biểu nhiều trang** | Cắt đôi hàng chữ khi sang trang | Thường không hỗ trợ | **Bảo đảm chuẩn (`cantSplit` & `tblHeader`)** |
| **Dịch chuyển công thức Excel** | Gán cứng thành số chết | Thay thế chuỗi cơ bản | **Phân tích cây AST & Dời khối 2D** |
| **Bảo toàn Logo & Khối vẽ DrawingML** | Thường bị xóa khi lưu lại | Chỉ giữ được nếu không đụng tới | **Bộ đệm bảo vệ neo ảnh DrawingML** |
| **Số hóa bảng từ PDF scan nhiều cột** | Đoán mò cấu trúc, sai lệch | Thất bại với bố cục phức tạp | **Lưới đo đạc hình thái học OpenCV** |
| **Hệ thống cổng kiểm định chất lượng** | Không có (hỏng file ngầm) | Bọc `try...except` đơn giản | **13 Cổng chất lượng phổ quát (UG-01..13)** |

---

## Cài Đặt Nhanh

### Cài đặt qua `pip` hoặc `uv`

Cài đặt gói chính thức từ PyPI:

```bash
pip install docwright-ai-toolkit
```

Kiểm tra trạng thái cài đặt:

```bash
docwright --version
```

### Tra cứu Danh mục Công cụ

Liệt kê toàn bộ các công cụ MCP đã đăng ký và năng lực xử lý:

```bash
docwright list
```

Xem cấu trúc tham số (schema) chi tiết của bất kỳ công cụ nào:

```bash
docwright schema docx.build_document
```

---

## Cấu Hình Tích Hợp Toàn Diện Cho Các AI Agent & IDE

Docwright giao tiếp tự nhiên qua chuẩn giao thức **Model Context Protocol (MCP)** sử dụng luồng nhập xuất chuẩn (`stdio`), đồng thời cung cấp giao diện dòng lệnh **CLI Engine** xác định tuyệt đối dành cho các AI Agent tương tác qua terminal hoặc hệ thống tự động hóa CI/CD.

### 1. Claude Code CLI (Anthropic)
Kích hoạt tích hợp MCP chỉ với 1 dòng lệnh:
```bash
claude mcp add docwright -- docwright-mcp
```
Hoặc thêm vào tệp `.claude.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 2. Cursor IDE
Thêm vào `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 3. Google Antigravity IDE
Thêm vào `.agents/mcp_config.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 4. Claude Desktop
Thêm vào `%APPDATA%\Claude\claude_desktop_config.json` (Windows) hoặc `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 5. Windsurf / Codeium
Thêm vào `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 6. OpenAI Codex CLI & Các AI Agent Dòng Lệnh
Đối với các AI Agent hoạt động trên môi trường shell (Codex CLI, Aider, CI/CD runner), gọi trực tiếp các công cụ một cách xác định qua CLI:
```bash
# Khám phá danh mục toàn bộ 51 tools
docwright list

# Xem chi tiết hợp đồng dữ liệu và tham số của tool
docwright schema docx.build_document

# Thực thi tác vụ với tệp đặc tả JSON
docwright docx.build_document --spec payload.json
```

### 7. Các Client Hỗ Trợ Chuẩn MCP (Cline, Roo Code, Continue.dev, Zed)
Bất kỳ AI Client nào tuân thủ chuẩn Model Context Protocol đều có thể kết nối thông qua lệnh `docwright-mcp`. Các tệp cấu hình mẫu đã được chuẩn bị sẵn tại thư mục [`configs/`](configs/):
- **Continue.dev**: [`configs/continue_mcp.json`](configs/continue_mcp.json)
- **Zed Editor**: [`configs/zed_settings.json`](configs/zed_settings.json)
- **Roo Code / Cline**: [`configs/universal_mcp.json`](configs/universal_mcp.json)

---

## Kiến Trúc Hệ Thống

Docwright vận hành dựa trên kiến trúc 5 tầng phân định trách nhiệm rõ ràng:

```
[ Mô hình AI / IDE (Cursor, Claude, Antigravity) ]
                       |
                 (MCP JSON-RPC)
                       v
[ Tầng 5: Giao diện   ] ──> Bộ điều phối CLI & Máy chủ MCP STDIO
                       |
[ Tầng 4: Nghiệp vụ   ] ──> ToolRegistry trung tâm (Điều phối & lọc tham số)
                       |
[ Tầng 3: Hợp đồng    ] ──> Lược đồ Pydantic mở (DocSpec, LayoutSpec, Envelope)
                       |
[ Tầng 2: Kiểm định   ] ──> 13 Cổng kiểm định phổ quát (UG-01..13) & Chẩn đoán
                       |
[ Tầng 1: Động cơ lõi ] ──> TagOrderRegistry, 2D BlockMutator, OpenCV Measurer
```

- **Hợp đồng công khai (`contracts/`)**: Các mô hình Pydantic mở giúp AI đọc hiểu đầy đủ cấu trúc dữ liệu, gợi ý kiểu (type-hints) và tài liệu tham số.
- **Động cơ bảo vệ (`core/`, `gates/`)**: Các mô-đun nhị phân hiệu năng cao, cưỡng chế ngữ pháp XML, hình học bảng và tính toán công thức.

---

## Danh Mục Công Cụ Tiêu Biểu

Docwright cung cấp 51 công cụ chuyên biệt được phân nhóm theo nghiệp vụ:

### Phân hệ Xử lý Văn bản Word (`docx.*`)
- `docx.build_document`: Biên dịch lược đồ JSON `DocSpec` thành tài liệu Word hoàn chỉnh có rào chắn bảo vệ cấu trúc OpenXML.
- `docx.measure_pdf_layout`: Đo đạc hình học bảng, tỷ lệ các cột và góc nghiêng của tài liệu scan bằng thuật toán xử lý ảnh.
- `docx.populate_layout_text`: Ánh xạ nội dung văn bản vào các ô bảng đã được đo đạc mà không cần tính toán tọa độ thủ công.
- `docx.compile_layout_spec`: Biên dịch kết quả đo đạc hình học thành đặc tả cấu trúc `DocSpec` chuẩn mực.
- `docx.patch`: Thay thế nội dung văn bản chính xác tại vị trí cần sửa mà không làm mất định dạng xung quanh.
- `docx.validate`: Kiểm toán tính hợp lệ của tài liệu dựa trên các quy chuẩn cấu trúc OpenXML.

### Phân hệ Xử lý Bảng tính Excel (`xlsx.*`)
- `xlsx.mutate_block`: Biến đổi khối ô chữ nhật 2D với cơ chế tự động tịnh tiến công thức theo chiều ngang và dọc.
- `xlsx.detect_tables`: Tự động phát hiện biên giới các bảng độc lập, hành lang khoảng trắng và ma trận viền trên cùng một trang tính.
- `xlsx.extract`: Trích xuất dữ liệu bảng tính trung thực và lưu vào kho lưu trữ nội bộ nhằm chống tràn bộ nhớ ngữ cảnh (context window) của AI.
- `xlsx.query`: Truy vấn dữ liệu theo phân trang và lát cắt ô mục tiêu từ kết quả trích xuất.
- `xlsx.validate`: Kiểm định toàn diện bảng tính qua 13 Cổng kiểm định phổ quát (`UG-01..13`).
- `xlsx.recalc`: Tính toán lại giá trị công thức và tiêm giá trị bộ nhớ đệm (cache) vào cấu trúc OpenXML.

### Phân hệ Sơ đồ Kỹ thuật (`diagram.*`)
- `diagram.build`: Khởi tạo cấu trúc XML `mxGraphModel` chuẩn cho Draw.io từ bản mô tả quan hệ tô-pô.
- `diagram.render_raster`: Kết xuất sơ đồ ra định dạng ảnh PNG độ phân giải cao không cần mở trình duyệt.
- `diagram.render_svg`: Xuất sơ đồ dạng vector sắc nét phục vụ in ấn và hiển thị web.

---

## Bản Đóng Gói Nhị Phân Độc Lập (Standalone Binary)

Đối với các môi trường làm việc văn phòng không cài sẵn Python, bản thực thi độc lập (Standalone Executable) được cung cấp sẵn tại mục [GitHub Releases](https://github.com/YukiiMin/docwright-ai-toolkit/releases):

- Tải tệp `docwright-windows-amd64.exe`.
- Cấu hình ứng dụng AI trỏ trực tiếp vào tệp thực thi này:
  ```json
  {
    "mcpServers": {
      "docwright": {
        "command": "C:\\duong-dan\\toi\\docwright.exe",
        "args": ["mcp"]
      }
    }
  }
  ```

---

## Bản Quyền & Điều Khoản Thương Mại

Docwright AI Toolkits được phát hành theo giấy phép **Business Source License 1.1 (BSL 1.1)**.

- **Sử dụng Phi Thương mại & Phát triển Phần mềm**: Hoàn toàn miễn phí cho mục đích cá nhân, học tập, quy trình làm việc nội bộ doanh nghiệp, dự án mã nguồn mở và tích hợp với các AI IDE.
- **Hạn chế Thương mại**: Nghiêm cấm các bên thứ ba sử dụng Docwright AI Toolkits để đóng gói thành dịch vụ điện toán đám mây (Hosted Service), API thương mại hoặc sản phẩm SaaS có thu phí mà không có văn bản cấp phép của tác giả.
- **Liên hệ Cấp phép Doanh nghiệp**: Quý doanh nghiệp có nhu cầu cấp phép thương mại hoặc tích hợp sâu, vui lòng liên hệ nhóm phát triển.
