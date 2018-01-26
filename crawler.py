import requests
from bs4 import BeautifulSoup


def get_anchors(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    anchors = soup.findAll('a', href=True)
    hrefs = [url]
    for anchor in anchors:
        if anchor['href'] not in hrefs:
            hrefs.append(anchor['href'])

    return hrefs


def get_seo_tag(s, keyword):
    tag = s.find('meta', {'name': keyword})

    if tag and tag.attrs and tag.attrs['content']:
        return str(tag.attrs['content'])
    else:
        return "Missing"


def get_og_tag(s, keyword):
    tag = s.find('meta', {'property': keyword})

    if tag and tag.attrs and tag.attrs['content']:
        return str(tag.attrs['content'])
    else:
        return "Missing"


def get_twitter_tag(s, keyword):
    tag = s.find('meta', {'name': keyword})

    if tag and tag.attrs and tag.attrs['content']:
        return str(tag.attrs['content'])
    else:
        return "Missing"


def format_image_url(image_url, prefix_url):
    if prefix_url not in image_url:
        return prefix_url + image_url
    else:
        return image_url


def render_page(url, recursive):

    template = open("templates/page_template.html", 'r').read()
    main_template = open('templates/main_template.html', 'r').read()

    anchors = [url]
    if recursive:
        anchors = get_anchors(url)
        for anchor in anchors:
            if url not in anchor:
                if anchor.find('/') == 0:
                    # Get all internal anchors from the url that are not duplicate
                    internal_anchors = get_anchors(url + anchor)
                    for internal_anchor in internal_anchors:
                        if internal_anchor not in anchors:
                            anchors.append(internal_anchor)

    formatted_template = ""
    for anchor in anchors:
        page_url = anchor
        if page_url.find('/') == 0 or page_url.find('#') == 0:
            page_url = url + page_url

        if url not in page_url or page_url.endswith(".jpg") or page_url.endswith(".png"):
            continue

        r = requests.get(page_url)
        if r.status_code is not 200:
            continue

        soup = BeautifulSoup(r.text, 'html.parser')

        # SEO
        title_tag = soup.find('title')
        if title_tag:
            title = str(title_tag.text)
        else:
            title = "Missing"
        meta_description = get_seo_tag(soup, "description")
        meta_keywords = get_seo_tag(soup, "keywords")
        meta_image = get_seo_tag(soup, "image")
        meta_image = format_image_url(meta_image, page_url)

        # OpenGraph
        og_title = get_og_tag(soup, "og:title")
        og_description = get_og_tag(soup, "og:description")
        og_image = get_og_tag(soup, "og:image")
        og_image = format_image_url(og_image, page_url)
        og_url = get_og_tag(soup, "og:url")
        og_site_name = get_og_tag(soup, "og:site_name")
        og_type = get_og_tag(soup, "og:type")

        # Twitter
        twitter_card = get_twitter_tag(soup, "twitter:card")
        twitter_site = get_twitter_tag(soup, "twitter:site")
        twitter_creator = get_twitter_tag(soup, "twitter:creator")
        twitter_title = get_twitter_tag(soup, "twitter:title")
        twitter_description = get_twitter_tag(soup, "twitter:description")
        twitter_url = get_twitter_tag(soup, "twitter:url")
        twitter_image_src = get_twitter_tag(soup, "twitter:image:src")
        twitter_image_src = format_image_url(twitter_image_src, page_url)

        print ("----------------")
        print (page_url)
        print ("----------------")
        formatted_template = formatted_template + str(template).format(page_url, title, meta_description,
                                                                           meta_keywords,
                                                                           meta_image,
                                                                           og_title, og_description, og_image, og_url,
                                                                           og_site_name,
                                                                           og_type,
                                                                           twitter_card, twitter_site, twitter_creator,
                                                                           twitter_title, twitter_description,
                                                                           twitter_url,
                                                                           twitter_image_src)

    main_template = str(main_template).format(formatted_template)
    return main_template