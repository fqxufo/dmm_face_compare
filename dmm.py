from requests_html import HTMLSession
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys



session = HTMLSession()
baseurl = 'http://www.dmm.co.jp/search/=/searchstr='
header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'}
session.headers.update(header)

inputStr = input('输入车牌号:').strip().replace(' ','')
url = baseurl + inputStr

r = session.get(url)



coverImage = r.html.find('img.float-l',first=True)
hasResult = (coverImage != None)

if (hasResult):
    print(coverImage.attrs['src'])
    coverImageSrc = 'http:' + coverImage.attrs['src']
    title = r.html.find('.ttl-list',first=True)
    print(title.text)
    video = r.html.find('.btn a',first=True)
    print(video.attrs['href'])
    videoSrc = video.attrs['href'].replace('_sm_','_dmb_')


    fullCoverSrc = coverImageSrc.replace('ps.','pl.')
    fullCoverImage = session.get(fullCoverSrc)


    with open(inputStr + '-coverImage.jpg','wb') as f:
        f.write(fullCoverImage.content)

    teaserVideo = session.get(videoSrc)

    with open(inputStr + '-teaservideo.mp4','wb') as f:
        f.write(teaserVideo.content)

    # img=mpimg.imread(inputStr + '-coverImage.jpg')
    # imgplot = plt.imshow(img)
    # plt.show()

else:
    print('车牌号错误,找不到结果')
    sys.exit(0)


