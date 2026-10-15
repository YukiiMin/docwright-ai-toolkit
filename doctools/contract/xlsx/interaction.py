"""
doctools.contract.xlsx.interaction — Hợp đồng đặc tả tương tác hàng loạt (BatchInteractionSpec).
Tuân thủ Quyết định 28.4 và kiến trúc Transactional Atomicity (All-or-Nothing):
- Data Validation Rules (Dropdown lists, numeric ranges, date limits).
- Conditional Formatting Rules (Cell value comparisons, formula triggers).
- Sheet Protection Rules.
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class DataValidationRule(BaseModel):
    """Quy tắc kiểm thực dữ liệu (Data Validation) trên một dải ô."""
    model_config = ConfigDict(extra="ignore")

    sheet: str = Field(..., description="Tên worksheet áp dụng")
    cell_range: str = Field(..., description="Dải ô áp dụng, ví dụ: 'B2:B50'")
    type: Literal["list", "whole", "decimal", "date", "time", "textLength", "custom"] = Field(
        default="list", description="Loại kiểm thực"
    )
    formula1: str = Field(..., description="Giá trị hoặc công thức điều kiện 1 (ví dụ '\"ACTIVE,INACTIVE\"')")
    formula2: Optional[str] = Field(default=None, description="Điều kiện 2 (nếu có)")
    allow_blank: bool = Field(default=True, description="Cho phép để trống")
    error_title: Optional[str] = Field(default=None, description="Tiêu đề thông báo lỗi")
    error_message: Optional[str] = Field(default=None, description="Nội dung thông báo lỗi")


class ConditionalFormatRule(BaseModel):
    """Quy tắc định dạng có điều kiện (Conditional Formatting) trên một dải ô."""
    model_config = ConfigDict(extra="ignore")

    sheet: str = Field(..., description="Tên worksheet áp dụng")
    cell_range: str = Field(..., description="Dải ô áp dụng, ví dụ: 'C2:C50'")
    operator: Literal[
        "equal", "notEqual", "greaterThan", "lessThan", "between", "notBetween"
    ] = Field(default="equal", description="Toán tử so sánh")
    formula: List[str] = Field(
        default_factory=lambda: ['"FAIL"'],
        description="Giá trị hoặc công thức so sánh"
    )
    fill_color: str = Field(
        default="FFFFCCCC", description="Mã màu nền hex ARGB (ví dụ 'FFFFCCCC' cho đỏ nhạt)"
    )
    font_color: Optional[str] = Field(default=None, description="Mã màu chữ hex ARGB")


class SheetProtectionRule(BaseModel):
    """Quy tắc bảo vệ bảng tính (Sheet Protection)."""
    model_config = ConfigDict(extra="ignore")

    sheet: str = Field(..., description="Tên worksheet áp dụng")
    password: Optional[str] = Field(default=None, description="Mật khẩu bảo vệ (nếu có)")
    select_locked_cells: bool = Field(default=True, description="Cho phép chọn ô bị khóa")
    select_unlocked_cells: bool = Field(default=True, description="Cho phép chọn ô mở khóa")


class BatchInteractionSpec(BaseModel):
    """
    Quy cách tổng hợp cập nhật tương tác hàng loạt trong một giao dịch nguyên tử.
    All-or-Nothing Staging Transaction.
    """
    model_config = ConfigDict(extra="ignore")

    validations: List[DataValidationRule] = Field(
        default_factory=list, description="Danh sách quy tắc Data Validation"
    )
    conditional_formats: List[ConditionalFormatRule] = Field(
        default_factory=list, description="Danh sách quy tắc Conditional Formatting"
    )
    protections: List[SheetProtectionRule] = Field(
        default_factory=list, description="Danh sách quy tắc Sheet Protection"
    )
