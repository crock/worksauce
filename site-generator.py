import json
import re
import os
import sys
from datetime import datetime

now = datetime.now().strftime("%Y%m%d")

if sys.argv[1]:
    now = sys.argv[1]
    print(f"Using date: {now}")

def inline_stylesheet():
    with open("assets/global.css") as f:
        styles = f.read()
    
    return f"""
<style type="text/css">
{styles}
</style>
"""

def generate_page_html(title, content, metaDescription = ""):
    analyticsHtml = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2BHVK54E8T"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-2BHVK54E8T');
</script>
"""

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    {analyticsHtml}
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Dev Portfolio Showcase</title>
    <meta name="description" content="{metaDescription}">
    <link rel="stylesheet" href="/assets/global.css" />
</head>
<body>
    {content}
    <script src="/assets/script.js"></script>
</body>
</html>
"""

def generate_iframe_html(src, title = ""):
    return f"""
<iframe src="{src}" title="{title}" frameborder="0" allowfullscreen width="100%" height="720"></iframe>
"""

def create_site_page(name, html, directoryListing = False):
    outputPath = f"www/{now}/{name}/index.html"
    if not name:
        outputPath = f"www/{now}/index.html"
    if directoryListing:
        outputPath = f"www/{now}/index.html"
    os.makedirs(os.path.dirname(outputPath), exist_ok=True)

    with open(outputPath, "w") as f:
        f.write(html)
        print(f"Created {name} at {outputPath}")
    with open("www/index.html", "w") as f:
        f.write(html)
        print(f"Created homepage at www/index.html")

def copy_assets():
    os.makedirs("www/assets", exist_ok=True)
    os.system("rsync -r assets/* www/assets")
    print("Copied assets to www/assets")

def get_screenshot_public_path(site):
    domain = site["domain"]
    filename = f"http_{domain}_80.jpg"
    screenshotPath = f"/img/{now}/{filename}"
    
    return screenshotPath

def get_thumbnail_public_path(site):
    publicPath = get_screenshot_public_path(site)
    screenshotPath = f"{publicPath}?nf_resize=fit&w=350"
    
    return screenshotPath

def create_index_page(sites):
    # get list of json files in directory
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    # sort by date
    files.sort(key=lambda x: os.path.getmtime(os.path.join("data", x)))

    datestamps = list(map(lambda x: x.split("-")[0], files))

    html = f"""
<h1>Dev Portfolio Showcase</h1>
<p>Last Crawled: {now}</p>
<p>Total websites in showcase: {len(sites)}</p>
<p>View previous crawls:</p>
<ul class="previous-crawls">
"""
    for datestamp in datestamps:
        html += f"""
<li><a href="/{datestamp}/index.html">{datestamp}</a></li>
"""
    html += """
</ul>
<ul class="grid sites">
"""
    for site in sites:
        domain = site["domain"]
        title = site["title"]
        description = site["description"]

        pageSlug = re.sub(r"\.+", "-", domain)

        html += f"""
<li class="soft-shadow">
    <div class="img-preview">
        <a href="{get_screenshot_public_path(site)}" target="_blank">
            View Full Size
        </a>
        <img src="{get_thumbnail_public_path(site)}" alt="{domain} screenshot thumbnail" width="512" />
    </div>
    <a href="/{now}/{pageSlug}/index.html">{domain}</a>
    <p>{title}</p>
</li>
"""
    html += """
</ul>
"""
    pageContent = generate_page_html("Home", html, "Showcase and archive of the top-ranked web developer portfolios as indexed by Google")
    create_site_page(None, pageContent, directoryListing=True)

def main():
    path = os.path.join("data", f"{now}-sites.json")
    with open(path) as f:
        sites = json.load(f)
    if len(sites) == 0:
        print("No sites found")
        return
    for site in sites:
        domain = site["domain"]
        title = site["title"]
        description = site["description"]

        pageSlug = re.sub(r"\.+", "-", domain)

        html = f"""
<h1>{title}</h1>
<p>{description}</p>
{generate_iframe_html(f"https://{domain}/", title)}
"""

        pageContent = generate_page_html(f"Viewing {domain}", html, description)
        create_site_page(pageSlug, pageContent)
    create_index_page(sites)
    copy_assets()

if __name__ == '__main__':
    main()