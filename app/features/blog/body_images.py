import re

IMAGE_PARAGRAPH = re.compile(
    r"^(?:/(?!/)|https://)\S+\.(?:png|jpe?g|webp|gif|avif)$", re.IGNORECASE
)

_PARAGRAPH_SPLIT = re.compile(r"\n{2,}")


def first_image_paragraph(body: str) -> str | None:
    for paragraph in _PARAGRAPH_SPLIT.split(body):
        if IMAGE_PARAGRAPH.fullmatch(paragraph.strip()):
            return paragraph.strip()
    return None
