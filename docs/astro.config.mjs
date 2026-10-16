// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://docwright-ai-toolkit.vercel.app',
	integrations: [
		starlight({
			title: 'Docwright AI Toolkits',
			description: 'Deterministic Word (DOCX) and Excel (XLSX) Engineering Toolkit for AI Agents, Python SDK, and CLI',
			logo: {
				src: './src/assets/logo.png',
			},
			favicon: '/images/docwright-ai-toolkit-icon.png',
			defaultLocale: 'root',
			locales: {
				root: {
					label: 'English',
					lang: 'en',
				},
				vi: {
					label: 'Tiếng Việt',
					lang: 'vi',
				},
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/YukiiMin/docwright-ai-toolkit' },
			],
			sidebar: [
				{
					label: 'Getting Started',
					translations: { vi: 'Bắt Đầu Nhanh' },
					items: [
						{ label: 'Quickstart Guide', translations: { vi: 'Hướng Dẫn Nhanh' }, slug: 'getting-started' },
						{ label: 'Installation & Setup', translations: { vi: 'Cài Đặt Môi Trường' }, slug: 'getting-started/installation' },
						{ label: '1-Click AI IDE Setup', translations: { vi: 'Cài Đặt 1-Click AI IDE' }, slug: 'getting-started/ai-ide-setup' },
						{ label: '3 Usage Modes (MCP / SDK / CLI)', translations: { vi: '3 Phương Thức Sử Dụng' }, slug: 'getting-started/usage-modes' },
						{ label: 'Architecture & Modules', translations: { vi: 'Kiến Trúc & Mô-đun' }, slug: 'getting-started/architecture' },
					],
				},
				{
					label: 'Core Modules',
					translations: { vi: 'Mô-đun Cốt Lõi' },
					items: [
						{ label: 'Word (docx.* — 19 Tools)', translations: { vi: 'Mô-đun Word (docx.*)' }, slug: 'domain-guides/word-docx' },
						{ label: 'Excel (xlsx.* — 31 Tools)', translations: { vi: 'Mô-đun Excel (xlsx.*)' }, slug: 'domain-guides/excel-xlsx' },
					],
				},
				{
					label: 'Tool & SDK Reference (51 Tools)',
					translations: { vi: 'Tham Chiếu 51 Công Cụ & SDK' },
					items: [
						{ label: 'Complete 51-Tool Catalog', translations: { vi: 'Tổng Quan 51 Công Cụ' }, slug: 'reference' },
						{ label: 'Word Tools (docx.*)', translations: { vi: 'Công Cụ Word (docx.*)' }, slug: 'reference/docx-tools' },
						{ label: 'Spreadsheet Tools (xlsx.*)', translations: { vi: 'Công Cụ Excel (xlsx.*)' }, slug: 'reference/xlsx-tools' },
						{ label: 'Common, CLI & Python SDK', translations: { vi: 'Tiện Ích Chung, CLI & SDK' }, slug: 'reference/common-and-sdk' },
					],
				},
				{
					label: 'Cookbooks & Workflows',
					translations: { vi: 'Kịch Bản Thực Chiến' },
					items: [
						{ label: 'Multi-Page Executive Report', translations: { vi: 'Xuất Báo Cáo Nhiều Trang' }, slug: 'cookbooks/multi-page-report' },
						{ label: 'Scanned PDF to 1:1 Word Form', translations: { vi: 'Tái Tạo Biểu Mẫu Từ PDF Scan' }, slug: 'cookbooks/scanned-pdf-to-docx' },
						{ label: 'Safe 2D Spreadsheet Mutation', translations: { vi: 'Chèn Khối & Dịch Công Thức Excel' }, slug: 'cookbooks/spreadsheet-mutation' },
					],
				},
				{
					label: 'Quality Verification',
					translations: { vi: 'Kiểm Định Chất Lượng' },
					items: [
						{ label: 'Automated Quality Gates', translations: { vi: 'Cổng Kiểm Định Tự Động' }, slug: 'quality-gates/universal-gates' },
						{ label: 'Structured Diagnostics', translations: { vi: 'Chẩn Đoán Lỗi Cấu Trúc' }, slug: 'quality-gates/fail-closed' },
					],
				},
				{
					label: 'Changelog',
					translations: { vi: 'Nhật Ký Phiên Bản' },
					items: [
						{ label: 'Release Notes (v1.0.2)', translations: { vi: 'Lịch Sử Cập Nhật (v1.0.2)' }, slug: 'changelog' },
					],
				},
			],
		}),
	],
});
