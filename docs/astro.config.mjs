// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://docwright.dev',
	integrations: [
		starlight({
			title: 'Docwright AI Toolkits',
			description: 'The AI-Native Office & Diagram Toolkit Plugin for AI Agents (Word, Excel, Technical Diagrams)',
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
					items: [
						{ label: 'Introduction', slug: 'getting-started' },
						{ label: 'Why AI Fails at Docs', slug: 'getting-started/why-ai-fails' },
						{ label: 'Installation', slug: 'getting-started/installation' },
						{ label: '1-Click AI IDE Setup', slug: 'getting-started/ai-ide-setup' },
						{ label: '5-Layer Architecture', slug: 'getting-started/architecture' },
					],
				},
				{
					label: 'Domain Guides',
					items: [
						{ label: 'Word (DOCX) Engine', slug: 'domain-guides/word-docx' },
						{ label: 'Spreadsheets (XLSX) Engine', slug: 'domain-guides/excel-xlsx' },
						{ label: 'Technical Diagrams (Draw.io)', slug: 'domain-guides/diagram-drawio' },
					],
				},
				{
					label: 'Tool Reference (51 Tools)',
					items: [
						{ label: 'Catalog Overview', slug: 'reference' },
						{ label: 'Word Tools (docx.*)', slug: 'reference/docx-tools' },
						{ label: 'Spreadsheet Tools (xlsx.*)', slug: 'reference/xlsx-tools' },
						{ label: 'Diagram Tools (diagram.*)', slug: 'reference/diagram-tools' },
					],
				},
				{
					label: 'Enterprise Cookbooks',
					items: [
						{ label: 'Multi-Page Executive Report', slug: 'cookbooks/multi-page-report' },
						{ label: '1:1 Scanned PDF Reconstruction', slug: 'cookbooks/scanned-pdf-to-docx' },
						{ label: 'Safe Spreadsheet 2D Mutation', slug: 'cookbooks/spreadsheet-mutation' },
						{ label: 'Microservice Diagram Generation', slug: 'cookbooks/cloud-architecture' },
					],
				},
				{
					label: 'Quality Gates & Diagnostics',
					items: [
						{ label: '13 Universal Gates (UG-01..13)', slug: 'quality-gates/universal-gates' },
						{ label: 'OpenXML Error Invariants', slug: 'quality-gates/openxml-invariants' },
						{ label: 'Fail-Closed Diagnostics', slug: 'quality-gates/fail-closed' },
					],
				},
			],
		}),
	],
});
