import easyocr


def extract_text_from_image(image_path):
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image_path)

    text = " ".join([t for (_, t, _) in result])
    return text.strip()
