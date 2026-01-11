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

## 待你补充的信息（补齐后我会把网页/简历一键完善）

- 邮箱、电话、城市（是否需要隐私版）
- 学历（本科/硕士/博士）、专业、入学时间、预计毕业时间
- 目标实习岗位（例如：图形算法/仿真/渲染/GPU/研究实习），以及可到岗时间
- 2–4 个代表性项目：每个项目给我「一句话目标 + 你负责的内容 + 技术栈 + 可量化结果 + 链接」
- 技能清单：编程语言、CUDA/并行、图形/仿真相关关键词、工程工具
- 英文能力（可选）
- 头像选择：目前网页用 `iCloud 照片/IMG_7287.PNG` 居中裁剪生成的 `assets/avatar.webp`（可换成 7285/7286）
- 如果你改用证件照：按上面的脚本生成即可

## 已检测到的证明/材料

- `刘俊圆个人简历.pdf`：已提取联系方式、教育/经历、项目列表并写入中英简历
- `应急学院刘俊圆春分工程实践证明.pdf`：已加入“证明与社会实践/Activities”

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
