import itertools
import os
import re
from langchain_upstage import (
    UpstageLayoutAnalysisLoader,
)
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from PIL import Image
import fitz
import io


def pdf_parser(pdf_path: str, save_path: str = "./uploads") -> str:
    """Parse a PDF file and return the text."""
    paper_name = os.path.basename(pdf_path).split(".")[0]
    save_path = os.path.join(save_path, paper_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Dump images
    reader = PdfReader(pdf_path)
    image_list = []
    for page_idx, page in enumerate(reader.pages):
        for image_idx, image in enumerate(page.images):
            with open(
                os.path.join(save_path, f"{page_idx}_{image_idx}.png"), "wb"
            ) as f:
                f.write(image.data)
            image_list.append(f"{page_idx}_{image_idx}.png")
    # Dump texts
    layzer = UpstageLayoutAnalysisLoader(pdf_path, output_type="html")
    docs = layzer.load()

    doc = docs[0]
    doc.metadata["paper_name"] = paper_name
    content = doc.page_content

    # insert image into content at <img> tag
    for image_idx, path in enumerate(image_list):
        img_tag_regex = r"<img\b(?![^>]*\bsrc\b)[^>]*>"

        def insert_img_link(match):
            # Insert the image link into matched string
            return match.group()[:-1] + f'src="{path}"' + match.group()[-1]

        content = re.sub(img_tag_regex, insert_img_link, content, count=1)
    doc.page_content = content

    with open(os.path.join(save_path, "parsed.html"), "w") as f:
        for doc in docs:
            f.write(content)


def to_abs_path(rel_path: str) -> str:
    """Convert a relative path to an absolute path."""
    return os.path.join(os.path.dirname(__file__), rel_path)


if __name__ == "__main__":
    # Example usage
    pdf_parser(
        to_abs_path(
            "sample_pdfs/Language Models are Unsupervised Multitask Learners.pdf"
        )
    )
