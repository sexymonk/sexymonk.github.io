# 个人简历与网页（本地）

## 预览网页

- 直接用浏览器打开根目录的 `index.html`
- Windows 下也可以用本地静态服务器（可选）：
  - `python -m http.server 8000`
  - 然后访问 `http://localhost:8000/`

## 简历文件

- 中文简历：`resume/resume.zh-CN.md`
- 英文简历：`resume/resume.en.md`

## 中英切换

- 网页右上角点击 `中/EN` 切换
- 或通过 URL 参数强制指定：
  - `/?lang=zh`
  - `/?lang=en`

## 证件照裁剪（头像）

1. 把你发的那张证件照保存为：`assets/avatar_source.jpg`（或 .png）
2. 运行：`python tools/make_avatar.py`
3. 会生成：`assets/avatar.webp` 和 `assets/avatar.png`（网页会自动使用 webp）

## 论文补充视频（Supplementary）

- `media/supplementary.mp4`
- `media/supplementary.web.mp4`（网页压缩版，约 12MB）
- 注意：文件较大（约 410MB）。若要部署到 GitHub Pages，建议：
  - 上传到 B站/YouTube 并在网页中外链
  - 或放到 GitHub Release / 使用 Git LFS（视仓库限制而定）
  - 或提供压缩版（已生成）：
    - 生成命令：`powershell -ExecutionPolicy Bypass -File tools/compress_supplementary.ps1`

## 隐私建议（重要）

如果你打算把网页部署到 GitHub Pages（公开），建议你确认是否要公开手机号：

- 当前网页展示了邮箱与手机号（便于投递/联系）
- 如需“公开版（隐藏手机号）+ 投递版（含手机号）”，我可以再帮你拆两套
