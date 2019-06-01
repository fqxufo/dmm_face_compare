from requests_html import HTMLSession
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys



session = HTMLSession()
baseurl = 'http://www.dmm.co.jp/search/=/searchstr='
header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'}
session.headers.update(header)


def download():
    input_str = input('输入车牌号:').strip().replace(' ','')
    url = baseurl + input_str
    r = session.get(url)

    cover_image = r.html.find('img.float-l',first=True)
    has_reault = (cover_image != None)

    if (has_reault):
        print(cover_image.attrs['src'])
        cover_image_src = 'http:' + cover_image.attrs['src']
        title = r.html.find('.ttl-list',first=True)
        print(title.text)
        video = r.html.find('.btn a',first=True)
        print(video.attrs['href'])
        video_src = video.attrs['href'].replace('_sm_','_dmb_')


        full_cover_src = cover_image_src.replace('ps.','pl.')
        full_cover_image = session.get(full_cover_src)


        cover_image_filename = input_str + '-coverImage.jpg'
        video_file_name = input_str + '-teaservideo.mp4'
        with open(cover_image_filename,'wb') as f:
            f.write(full_cover_image.content)
        
        print('下载预告片中......')
        teaser_video = session.get(video_src)

        with open(video_file_name,'wb') as f:
            f.write(teaser_video.content)

        # img=mpimg.imread(inputStr + '-coverImage.jpg')
        # imgplot = plt.imshow(img)
        # plt.show()

        return(cover_image_filename,video_file_name)

    else:
        print('车牌号错误,找不到结果')
        sys.exit(0)


