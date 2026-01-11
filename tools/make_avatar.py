import argparse
import os
from pathlib import Path

from PIL import Image


def _square_crop_from_face(img: Image.Image):
    """Return a square crop box (left, top, right, bottom) focusing on the largest detected face.

    Requires opencv-python. If detection fails, returns None.
    """

    try:
        import cv2  # type: ignore
    except Exception:
        return None

    rgb = img.convert("RGB")
    w, h = rgb.size

    import numpy as np  # type: ignore

    np_img = np.array(rgb)[:, :, ::-1]  # RGB -> BGR
    gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)

    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(cascade_path)
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

    if faces is None or len(faces) == 0:
        return None

    # pick the largest face
    x, y, fw, fh = max(faces, key=lambda b: b[2] * b[3])

    # expand to include hair/shoulders, then make square
    cx = x + fw / 2
    cy = y + fh / 2

    side = max(fw, fh) * 2.2
    left = int(round(cx - side / 2))
    top = int(round(cy - side / 2))
    right = int(round(cx + side / 2))
    bottom = int(round(cy + side / 2))

    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    # ensure square after clamping
    crop_w = right - left
    crop_h = bottom - top
    side2 = min(crop_w, crop_h)
    left2 = left + (crop_w - side2) // 2
    top2 = top + (crop_h - side2) // 2

    return (left2, top2, left2 + side2, top2 + side2)


def _center_square_crop(img: Image.Image):
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return (left, top, left + side, top + side)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a square resume avatar from a portrait photo.")
    parser.add_argument(
        "--input",
        default=str(Path("assets") / "avatar_source.jpg"),
        help="Input portrait image path (jpg/png/webp). Default: assets/avatar_source.jpg",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=512,
        help="Output avatar size (pixels). Default: 512",
    )
    parser.add_argument(
        "--out-webp",
        default=str(Path("assets") / "avatar.webp"),
        help="Output webp path. Default: assets/avatar.webp",
    )
    parser.add_argument(
        "--out-png",
        default=str(Path("assets") / "avatar.png"),
        help="Output png path. Default: assets/avatar.png",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    img = Image.open(in_path)

    box = _square_crop_from_face(img)
    if box is None:
        box = _center_square_crop(img)

    cropped = img.crop(box).convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)

    out_webp = Path(args.out_webp)
    out_png = Path(args.out_png)
    out_webp.parent.mkdir(parents=True, exist_ok=True)

    cropped.save(out_webp, quality=88, method=6)
    cropped.save(out_png, optimize=True)

    print(f"Wrote {out_webp} and {out_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
