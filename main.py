from bs4 import BeautifulSoup
import requests
import os

links = []
flowers = {'redrose': "https://in.pinterest.com/nshikarwar/red-rose-for-someone-special/",
           'dandelionWhite': "https://www.pinterest.com/adjanskim/dandelions/",
           'sunflower': "https://www.pinterest.com/ashkmitch/sunflower-pictures/"
           }


def get_srclinks(url, name):
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    # print(soup.prettify())
    image_tags = soup.find_all('img',{"class":"hCL kVc L4E MIw"})
    for image_tag in image_tags:
        links.append(image_tag['src'])
    if len(links):
        print(f"Got the links for {name}")


def download_img(links, name):
    path = f"images_{name}"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print(f"directory created for {name}")

    print(links)
    imgsdownloaded = 0
    imgsnotdownloaded = 0
    for image in links:
        if '.svg' in image:
            imgsnotdownloaded = imgsnotdownloaded + 1
        else:
            r = requests.get(image).content
            filename = f'images_{name}/image' + str(imgsdownloaded) + '.jpg'
            with open(filename, 'wb+') as f:
                f.write(r)
            imgsdownloaded = imgsdownloaded + 1
    print(f'{imgsdownloaded} {name} Images Downloaded')
    print(f'{imgsnotdownloaded} {name} Images failed to Download')
    links.clear()


for name, link in flowers.items():
    get_srclinks(link, name)
    download_img(links, name)
