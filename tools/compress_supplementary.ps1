param(
  [string]$Input = "media\supplementary.mp4",
  [string]$Output = "media\supplementary.web.mp4"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  throw "ffmpeg not found in PATH. Install ffmpeg first."
}

if (-not (Test-Path -LiteralPath $Input)) {
  throw "Input not found: $Input"
}

Write-Host "Compressing: $Input -> $Output" -ForegroundColor Cyan

ffmpeg -y -i $Input `
  -vf "scale=-2:720" `
  -c:v libx264 -preset medium -crf 28 -profile:v high -level 4.1 -pix_fmt yuv420p `
  -c:a aac -b:a 128k `
  -movflags +faststart `
  $Output

Write-Host "Done." -ForegroundColor Green
