from __future__ import print_function
import requests
from lxml import html
from title2bib.crossref import get_bib_from_title
import bibtexparser
from builtins import input
from PIL import Image
from . import __version__
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
headers = {
    # "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
}
print("\n\t Checking state of scihub...")
url_state ="https://raw.githubusercontent.com/bibcure/scihub_state/master/state.txt"
try:
    r = requests.get(url_state)
    state_scihub = [i.split(">>")[1] for i in r.iter_lines()]
    url_captcha_scihub = state_scihub[0]
    url_libgen = state_scihub[1]
    url_scihub = state_scihub[2]
    xpath_libgen_a = state_scihub[3]
    xpath_scihub_captcha = state_scihub[4]
    xpath_scihub_iframe = state_scihub[5]
    xpath_scihub_pdf = state_scihub[6]
    has_update = state_scihub[7] != __version__
    if has_update:
        print("\n\t\tWill be better if you upgrade scihub2pdf.")
        print("\t\tFor that, just do:\n")
        print("\t\t\t sudo pip install scihub2pdf --upgrade\n")
except:
    url_captcha_scihub = "http://moscow.sci-hub.cc"
    url_libgen = "http://libgen.io/scimag/ads.php"
    url_scihub = "http://sci-hub.cc/"
    xpath_libgen_a = "/html/body/table/tr/td[3]/a"
    xpath_scihub_captcha = "//*[@id='captcha']"
    xpath_scihub_iframe = "//iframe/@src"
    xpath_scihub_pdf = "//*[@id='pdf']"


def norm_url(url):
    if url.startswith("//"):
        url = "http:" + url

    return url


def download_from_libgen(bib, s):
    params = {"doi": bib["doi"], "downloadname": ""}

    r = s.get(url_libgen, params=params, headers=headers)
    print("libgen link", r.url)
    if r.status_code != 200:
        print("Fail libgen url", r.status_code)
        print("Maybe libgen is down. Try to use sci-hub instead.")
        return

    html_tree = html.fromstring(r.content)
    html_a = html_tree.xpath(xpath_libgen_a)
    if len(html_a) == 0:
        print("Copy and paste the below link into your browser")
        print("\n\t", r.url, "\n")
        return

    download_link = norm_url(html_a[0].attrib["href"])
    bib["scihub"] = download_link
    download_pdf(bib, s)

    return


def check_captcha(iframe_url, url, html_tree, s):
    html_captcha = html_tree.xpath(xpath_scihub_captcha)
    if len(html_captcha) > 0:
        captcha_url = url_captcha_scihub+html_captcha[0].attrib["src"]
        r = s.get(captcha_url)

        Image.open(StringIO(r.content)).show()
        captcha_solution = input("Put the CAPTCHA: ")
        r = s.post(iframe_url, data={
            "captcha_code": captcha_solution
        })
        return True
    else:

        return False


def download_from_scihub(bib, s):

    url = url_scihub+bib["doi"]
    print("sci-hub link", url)
    r = s.get(url, headers=headers, allow_redirects=True)

    if r.status_code != 200:
        print("Fail scihub url", r.status_code)
        return

    html_tree = html.fromstring(r.content)
    iframe_url = html_tree.xpath(xpath_scihub_iframe)

    if len(iframe_url) == 0:
        print("Iframe not found.")
        print("Copy and paste the below link into your browser")
        print("\n\t", url, "\n")
        return

    iframe_url = iframe_url[0]
    ri = s.get(iframe_url, headers=headers)
    html_tree_ri = html.fromstring(ri.content)

    if check_captcha(iframe_url, url,  html_tree_ri, s):
        return download_from_scihub(bib, s)

    html_pdf = html_tree.xpath(xpath_scihub_pdf)

    if len(html_pdf) == 0:
        print("pdf file not found")
        print("\n\t", url)
        return

    download_link = norm_url(html_pdf[0].attrib["src"])
    bib["scihub"] = download_link
    download_pdf(bib, s)
    return


def download_pdf(bib, s):
    r = s.get(bib["scihub"], headers=headers)
    if r.status_code == 200:
        pdf_file = open(bib["pdf_file"], "wb")
        pdf_file.write(r.content)
        pdf_file.close()
        print("Download of", bib["pdf_file"], " ok")
    else:
        print("Fail in download ",
              bib["pdf_file"],
              " status_code ",
              r.status_code)


def download_pdf_from_bibs(bibs, location="",
                           use_libgen=False):
    def put_pdf_location(bib):
        pdf_name = bib["ID"] if "ID" in bib else bib["doi"].replace("/", "_")
        pdf_name += ".pdf"
        pdf_file = location+pdf_name

        bib["pdf_file"] = pdf_file
        return bib

    bibs_with_doi = list(filter(lambda bib: "doi" in bib, bibs))

    bibs = list(map(put_pdf_location, bibs_with_doi))

    with requests.Session() as s:
        if use_libgen:
            #libgen has no  captcha, try to use multiprocessing?
            list(map(lambda bib: download_from_libgen(bib, s), bibs))
        else:
            for bib in bibs:
                download_from_scihub(bib, s)


def download_from_doi(doi, location="", use_libgen=False):
    bib = {"doi": doi}
    pdf_name = "sci2pdf-{}.pdf".format(doi.replace("/", "_"))
    pdf_file = location+pdf_name
    bib["pdf_file"] = pdf_file

    with requests.Session() as s:
        if use_libgen:
            download_from_libgen(bib, s)
        else:
            download_from_scihub(bib, s)


def download_from_title(title, location="", use_libgen=False):
    found, bib_string = get_bib_from_title(title)

    if found:
        bib = bibtexparser.loads(bib_string).entries[0]
        if "doi" in bib:
            pdf_name = "sci2pdf-{}.pdf".format(
                bib["doi"].replace("/", "_")
            )
            pdf_file = location+pdf_name
            bib["pdf_file"] = pdf_file
            with requests.Session() as s:
                if use_libgen:
                    download_from_libgen(bib, s)
                else:
                    download_from_scihub(bib, s)
        else:
            print("Absent DOI")
