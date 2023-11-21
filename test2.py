import asyncio
from pyppeteer import launch

async def fetch_html(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    # Wait for some time to allow dynamic content to load
    await page.waitForTimeout(5000)

    # Get the fully rendered HTML
    html_content = await page.content()

    await browser.close()

    return html_content

# Replace 'your_edgeprop_url' with the actual URL
url = 'https://www.edgeprop.my/rent/malaysia/shop?keyword=Mid%20Valley&'

# Run the event loop
loop = asyncio.get_event_loop()
html_content = loop.run_until_complete(fetch_html(url))

# Now, you can process the HTML content using your preferred method
print(html_content)