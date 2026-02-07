# Academic PDF Notes Generator Skill

一个用于从学术 PDF 文档生成高质量中文学习笔记的完整工作流。

## 📁 目录结构

```
academic_pdf_notes/
├── SKILL.md              # 主指令文件（AI 的操作手册）
├── scripts/              # 辅助脚本
│   └── pdf_extractor.py  # PDF 文本提取工具
├── templates/            # 笔记模板
│   └── note_template.md  # 标准笔记结构模板
└── examples/             # 示例输出
    └── example_14.1.md   # 示例笔记
```

## 🚀 快速开始

### 对于 AI 助手

当用户请求生成 PDF 笔记时：

1. **阅读指令**：
   ```
   查看 SKILL.md 了解完整工作流程
   ```

2. **提取 PDF**：
   ```bash
   python3 scripts/pdf_extractor.py <PDF文件> --start <页码> --end <页码>
   ```

3. **生成笔记**：
   - 参考 `templates/note_template.md` 的结构
   - 参考 `examples/example_14.1.md` 的质量标准
   - 遵循 SKILL.md 中的所有要求

### 对于用户

只需告诉 AI：

```
使用 academic_pdf_notes skill 为 <PDF文件> 的第 X-Y 章生成笔记
```

AI 会自动：
1. 提取 PDF 内容
2. 分析章节结构
3. 生成结构化笔记
4. 确保格式一致

## ✨ 特性

- ✅ **自动化流程**：从 PDF 提取到笔记生成全自动
- ✅ **一致性保证**：所有笔记使用相同的结构和格式
- ✅ **双层内容**：核心总结 + 深度补充
- ✅ **现代知识**：整合最新技术和实践
- ✅ **质量标准**：明确的检查清单

## 📖 文件说明

### SKILL.md
主指令文件，包含：
- 完整的工作流程（6个步骤）
- 质量标准和要求
- 常见场景处理
- 输出检查清单

### scripts/pdf_extractor.py
PDF 文本提取工具：
- 支持页码范围提取
- 支持章节自动检测
- 支持多种输出格式

### templates/note_template.md
标准笔记结构模板：
- 核心内容总结部分
- 深度补充与拓展部分
- 完整的章节框架

### examples/example_14.1.md
示例笔记，展示：
- 期望的笔记质量
- 正确的格式使用
- 内容组织方式

## 🎯 使用场景

适用于：
- 📚 教科书章节笔记
- 📄 学术论文总结
- 📖 技术文档整理
- 🎓 考试复习资料

## 🔧 依赖

- Python 3.x
- PyMuPDF (pymupdf)

安装：
```bash
pip install pymupdf
```

## 📝 笔记质量标准

生成的笔记应该：
- ✅ 忠实原文，不遗漏关键信息
- ✅ 结构清晰，层次分明
- ✅ 完整保留代码和公式
- ✅ 标注所有图表引用
- ✅ 术语中英文对照
- ✅ 深度补充有价值的外部知识

## 🤝 贡献

如需改进此 Skill：
1. 更新 `SKILL.md` 中的指令
2. 在 `templates/` 中添加新模板
3. 在 `examples/` 中添加新示例

## 📄 许可证

MIT License

---

**提示**：这是一个 AI Skill，主要供 AI 助手使用。用户只需简单地请求生成笔记，AI 会自动遵循 SKILL.md 中的指令完成任务。
