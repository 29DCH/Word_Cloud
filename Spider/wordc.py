from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import jieba
import PIL
import matplotlib.pyplot as plt
import numpy as np


def wordcloudplot(txt,name):
    path = 'SourceHanSerifK-Light.otf'
    alice_mask = np.array(PIL.Image.open('jaychou.jpg'))
    alice_mask1 = np.array(PIL.Image.open('alice_mask.png'))
    #WordCloud构造方法
    wordcloud = WordCloud(font_path=path,
                          background_color="white",
                          margin=5, width=1800, height=800, mask=alice_mask, max_words=2000, max_font_size=60,stopwords = STOPWORDS,
                          random_state=40,contour_color='steelblue')
    wordcloud1 = WordCloud(font_path=path,
                          background_color="white",
                          margin=5, width=1800, height=800, mask=alice_mask1, max_words=2000,max_font_size=50,stopwords = STOPWORDS,
                          random_state=40,contour_color='steelblue')
    wordcloud = wordcloud.generate(txt)
    wordcloud1 = wordcloud1.generate(txt)
    wordcloud.to_file('../pictures/'+name+'/'+name+'.jpg')
    wordcloud1.to_file('../pictures/' + name + '/' + 'test.jpg')
    # image_colors = ImageColorGenerator(alice_mask)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    # image_colors = ImageColorGenerator(alice_mask1)
    plt.imshow(wordcloud1, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def makewordc(name):
    a = []
    f = open(r'../Songs/'+name+'/lrcs.txt', 'r').read()
    words = list(jieba.cut(f))
    for word in words:
        if len(word) > 1:
            a.append(word)
    txt = r' '.join(a)
    wordcloudplot(txt,name)


if __name__ == '__main__':
    makewordc('jaychou')