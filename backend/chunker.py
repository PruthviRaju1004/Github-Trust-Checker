import re
from dataclasses import dataclass

@dataclass
class Chunk:
    heading: str
    text: str

def chunk_markdown(markdown: str) -> list[Chunk]:
    lines = markdown.split("\n")
    chunks = []
    current_heading = "Overview"
    current_lines = []
    header_pattern = re.compile(r"^(#{1,3})\s+(.*)")
    in_code_block = False
    def flush():
        text = "\n".join(current_lines).strip()
        if text:
            chunks.append(Chunk(heading=current_heading, text=text))

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block   # flip it
            current_lines.append(line)
            continue                             # skip header check for this line

        if in_code_block:
            current_lines.append(line)
            continue                             # skip header check while inside code
        match = header_pattern.match(line)
        if match:
            flush()
            current_heading = match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    flush()
    return chunks


# if __name__ == "__main__":
#     sample = """# Flask

# Flask is a lightweight WSGI web application framework.

# ## Installation

# Install with pip: pip install flask

# ## Quickstart

# Here's a minimal example app.
# """
#     for c in chunk_markdown(sample):
#         print(f"[{c.heading}] ({len(c.text)} chars): {c.text[:50]!r}")