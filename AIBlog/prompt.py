import os
from datetime import datetime, timedelta
from AIBlog.azurestorage import get_row, insert_history
from AIBlog.graph import agent_graph
from utils import get_flat_date, get_flat_date_hour, parse_flat_date_hour

def getaiblog(parsed_date):
    timestamp = datetime.utcnow()
    flat_date_hour = get_flat_date(parsed_date) + "_00"

    if not os.environ.get("DEBUG", False):
        if lastdayblog := get_row(flat_date_hour):
            return lastdayblog["html_content"], parse_flat_date_hour(flat_date_hour)
        flat_date_hour = get_flat_date() + "_00"
        if parsed_date is not None and (lastdayblog := get_row(flat_date_hour)):
            return lastdayblog["html_content"], parse_flat_date_hour(flat_date_hour)

    for event in agent_graph.stream({"messages": [("system", f"""
        1. Search the internet for the latest news about AI and GenAI advancements.
        2. Navigate to the sites found as a result.
        3. Decide on a specific topic related to AI/GenAI advancements to write a blog about.
        4. Do thorough research on the chosen topic and write a detailed, Medium-style blog post.
        5. Create several relevant and realistic photos to accompany the blog (describe each photo as a professional photographer, ensuring the descriptions are suitable for image generation tools and retry if filtered).
        6. Create an HTML page for the blog, using the blog text and the generated photos.

        Output: Return only the pure HTML code for the blog page (no extra text, no markdown, just the HTML). The page should be visually appealing, responsive for both desktop and mobile, and include:
        - A clear blog header/title.
        - Well-formatted blog content with headings, paragraphs, and images placed appropriately.
        - Readable fonts, good contrast, and a cohesive color scheme.
        - Clean layout with proper spacing and alignment.
        - All images embedded using their URLs.
        - The HTML must be ready to render directly in a browser.
    """)]}):
        print("event: ", event)
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
    content = value["messages"][-1].content
    insert_history(rowkey=flat_date_hour, html_content=content)
    return content, timestamp