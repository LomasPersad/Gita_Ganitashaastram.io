# Import modules
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib import rc
# import matplotlib.image as mpimg
import seaborn as sns
from wordcloud import WordCloud,STOPWORDS, ImageColorGenerator
import re
import json
import collections
from nltk.probability import FreqDist
from nltk.text import Text
import nltk
from tqdm import tqdm

# from indic_transliteration import sanscript
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
# https://fonts.google.com/specimen/Eczar?subset=devanagari#standard-styles

#test1

#------Extract sections from large datafile

def get_data(nam):
    f = open(nam)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()
    return data

def get_verses():
    # Opening JSON file
    f = open('LP_dataset_english.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()

    # Iterating through the chapters
    # list
    # for i in data['chapters']:
    #     print(data['chapters'][i]['name'])
    V=['a']*640
    indx=0
    BG_total = pd.DataFrame(columns=['Chapter','Verse','Sanskrit','Transliteration'])
    # Iterating through the verses
    for i in data['chapters']:
        for v in data['verses'][i]:
            # print(data['verses'][str(i)][str(v)]['text'].replace('।।\* ।।',' '))
            print('chapter{} and verse{}'.format(i,v))
            tmp=data['verses'][str(i)][str(v)]['text'].replace('|',' ') #remove symbol
            tmp = tmp.replace('।', ' ')#remove symbol
            tmp = re.sub(r'\d+', '', tmp) #remove number
            V[indx]=tmp
            # Store in dataframe
            translit=data['verses'][str(i)][str(v)]['transliteration']
            # translit = translit.replace('-',' ')
            BG_total=BG_total.append({'Chapter': i, 'Verse': v, 'Sanskrit': tmp, 'Transliteration': translit},ignore_index = True)

            indx+=1


    # print(indx)
    # data_file = open("LP_verses.json", "w", encoding="utf-8")
    # json.dump(V, data_file, ensure_ascii=False)
    BG_total.to_csv('BG_dataframe.csv')


def compile_stopwords_list_frequency(text, freq_percentage=0.02):

    words = nltk.tokenize.word_tokenize(text)
    freq_dist = FreqDist(word.lower() for word in words)
    words_with_frequencies = [(word, freq_dist[word]) for word in freq_dist.keys()]
    sorted_words = sorted(words_with_frequencies, key=lambda tup: tup[1])
    length_cutoff = int(freq_percentage*len(sorted_words))
    stopwords = [tuple[0] for tuple in sorted_words[-length_cutoff:]]
    return stopwords

def plot_barchart():
    # get data
    data = get_data('LP_dataset_english.json')  # all data
    plt_vers = pd.DataFrame(columns=['chpt', 'Verse_count'])

    alist = []
    for i in data['chapters']:
        num = data['chapters'][str(i)]['verses_count']
        chpt_name = data['chapters'][str(i)]['name']
        chpt_name = chpt_name.split(':')
        print(txt_color.PURPLE + 'Chpt. {} has {} verses'.format(i, num))

        # new_list={'chpt': int(i), 'Verse_count': int(num)}

        # new_list = {'chpt':'Chpt. {} - {}'.format(i,chpt_name[0]), 'Verse_count': int(num)}
        new_list = {'chpt': "$\\bf{Chpt.}$" + "$\\bf{" + '{}'.format(i) + "}$" + '-' + chpt_name[0] + '-'+ "$\\bf{"+'{}'.format(num) +"}$ "+ 'verses',
                    'Verse_count': int(num)}
        alist.append(new_list)

        # plt_vers = plt_vers.append({'chpt': int(i), 'Verse_count': int(num)},
        #                            ignore_index=True)
        # plt_vers[n]=num
        # n+=1
    Chpt_versecount = pd.DataFrame.from_records(alist)  # create table

    # Setting the dimensions of the figure
    Chpt_versecount = Chpt_versecount.sort_values(by=['Verse_count'])
    # set figure size
    plt.figure(figsize=(20, 10))
    # plot polar axis
    ax = plt.subplot(111, polar=True)
    # remove grid
    plt.axis('off')
    # Set the coordinates limits
    # upperLimit = 100
    lowerLimit = 0
    # Compute max and min in the dataset
    max = Chpt_versecount['Verse_count'].max()

    # Let's compute heights: they are a conversion of each item value in those new coordinates
    # In our example, 0 in the dataset will be converted to the lowerLimit (10)
    # The maximum will be converted to the upperLimit (100)
    slope = (max - lowerLimit) / max
    heights = slope * Chpt_versecount['Verse_count'] + lowerLimit
    # Compute the width of each bar. In total we have 2*Pi = 360°
    width = 2 * np.pi / len(Chpt_versecount['Verse_count'])
    # Compute the angle each bar is centered on:
    indexes = list(range(1, len(Chpt_versecount['Verse_count']) + 1))
    angles = [element * width for element in indexes]
    # angles

    # Draw bars
    bars = ax.bar(
        x=angles,
        height=heights,
        width=width,
        bottom=lowerLimit,
        linewidth=2,
        edgecolor="white",
        color="#a371c7",
    )
    # little space between the bar and the label
    labelPadding = 1

    # Add labels
    for bar, angle, height, label in zip(bars, angles, heights, Chpt_versecount["chpt"]):

        # Labels are rotated. Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle)

        # Flip some labels upside down
        alignment = ""
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "right"
            rotation = rotation + 180
        else:
            alignment = "left"

        # Finally add the labels
        ax.text(
            x=angle,
            y=lowerLimit + bar.get_height() + labelPadding,
            s=label,
            ha=alignment,
            va='center',
            color="#000000",
            rotation=rotation,
            rotation_mode="anchor")

    # for container in ax.containers:
    #     ax.bar_label(container, weight='bold',color='#27065c') #fontsize=8 label_type='center'

    plt.savefig('plots/BG_verse_count.png', dpi=300)
    plt.show()

    # Old barchart

    # plt.figure(figsize=(15,5), frameon=False)
    # # plt.rc('font', family='Open Sans')
    # plt.tick_params(labelsize=11, length=6, width=2)
    # # Passing the data to plot
    # # sns.countplot(plt_vers)
    # my_image = plt.imread('plots/BG2.jpg')
    # ax=sns.barplot(x='chpt', y='Verse_count', data=Chpt_versecount)
    # for container in ax.containers:
    #     ax.bar_label(container,weight='bold')
    #     # ax.text(
    #     #     bar.get_x() + bar.get_width() / 2,
    #     #     bar.get_height() + 0.3,
    #     #     round(bar.get_height(), 1),
    #     #     horizontalalignment='center',
    #     #     color=bar_color,
    #     #     weight='bold'
    #     # )
    # # plt.imshow(img, extent=[110, 40, 110, 400], aspect='auto')
    # # plt.imshow(my_image,
    # #          aspect=ax.get_aspect(),
    # #          extent= ax.get_xlim() + ax.get_ylim(),
    # #          zorder=1, alpha=0.6)
    # ax=sns.barplot(x='chpt', y='Verse_count', data=Chpt_versecount)
    # plt.xlabel("Chapter number", fontsize=20, fontname='Nimbus sans')
    # plt.ylabel("Number of Verses", fontsize=20, fontname='Nimbus sans')
    # # Displaying the plot
    # plt.tight_layout()
    # plt.show()
    # # plt.savefig('plots/BG_verse_count.png')
    # # plt.savefig('plots/BG_verse_count.png')

def get_top_words(BGdata,n):
    df_verses = BGdata.apply(lambda row: row['Transliteration'].strip().split(), axis=1)
    data1 = []
    for row in df_verses:
        temp = []
        for words in row:
            if len(words) > 2:
                temp.append(words)
        data1.append(temp)
    data_flat1 = [item for sublist in data1 for item in sublist]
    # Getting to know the most prominent 10 words used across the documen
    # as per my knowledge of this holy document it makes sense to see these results because of the words used such as भारत, अर्जुन, कर्म, ज्ञानं.
    top_n_translit = [i[0] for i in sorted(dict(collections.Counter(data_flat1)).items(), key=lambda k: k[1], reverse=True)[:n]]
    return top_n_translit, data_flat1

def Translit_Wordcloud(data_flat1,savename):
    # data_flat1 = get_top_words(BGdata, 5)[1]
    # create stopword list from top_10_translit
    # stopwords = compile_stopwords_list_frequency(top_10_translit)
    # stopwords.remove("arjun")
    # stopwords.remove("krishna")

    img_data = Image.open("plots/Krishna.png")
    # sherlock_data = Image.open("/home/ubuntu/Downloads/k2.png")
    mask = np.array(img_data)
    # plot world cloud- generate for all, then each chapter
    wordfreq1 = collections.Counter(data_flat1)
    text = data_flat1
    plt.figure(figsize=(20, 10), facecolor='k')
    wordcloud = WordCloud(background_color="white", width=1300, height=600, max_words=2000,
                          font_path='/home/ubuntu/Downloads/Eczar/Eczar-VariableFont_wght.ttf', mask=mask).generate(str(text)) #,contour_width=1, contour_color='steelblue'
    # wordcloud.to_file('plots/WC_krish.png')
    wordcloud.to_file('plots/' + savename)
    #show
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


    # #-----------create coloring from image
    # Colorimg = Image.open("plots/k2.png")
    # mask = np.array(Colorimg)
    # image_colors = ImageColorGenerator(mask)
    # # plot world cloud- generate for all, then each chapter
    # wordfreq1 = collections.Counter(data_flat1)
    # text = data_flat1
    # fig = plt.figure(figsize=(20, 10), facecolor='k')
    # wordcloud = WordCloud(background_color="white", width=1300, height=600, max_words=2000,
    #                       font_path='/home/ubuntu/Downloads/Eczar/Eczar-VariableFont_wght.ttf', mask=mask).generate(
    #     str(text))
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    # plt.axis("off")
    # plt.show()
    # wordcloud.to_file('plots/WC_krish.png')

def get_top_sanskrit_words(BGdata,n):
    df_verses = BGdata.apply(lambda row: row['Sanskrit'].strip().split(), axis=1)
    data1 = []
    for row in df_verses:
        temp = []
        for words in row:
            if len(words) > 2:
                temp.append(words)
        data1.append(temp)
    data_flat1 = [item for sublist in data1 for item in sublist]
    # Getting to know the most prominent 10 words used across the documen
    # as per my knowledge of this holy document it makes sense to see these results because of the words used such as भारत, अर्जुन, कर्म, ज्ञानं.
    top_n_translit = [i[0] for i in sorted(dict(collections.Counter(data_flat1)).items(), key=lambda k: k[1], reverse=True)[:n]]
    return top_n_translit, data_flat1

def sanskrit_Wordcloud(data_flat1,savename):
    # data_flat1 = get_top_words(BGdata, 5)[1]
    # create stopword list from top_10_translit
    # stopwords = compile_stopwords_list_frequency(top_10_translit)
    # stopwords.remove("arjun")
    # stopwords.remove("krishna")

    stopword = open('hindi-tokenizer-master/stopwords.txt', 'r')
    stop_words = []
    # pre-process stopword
    for i in stopword:
        i = re.sub('[\n]', '', i)
        stop_words.append(i)
        stopwords = set(stop_words)

    # creating a dictionary of all the words with values as their counts.
    # wordfreq = {}
    # for w in tqdm(data_flat1):
    #     if w in wordfreq.keys():
    #         wordfreq[w] += 1
    #     else:
    #         wordfreq[w] = 1

    img_data = Image.open("plots/Krishna.png")
    # sherlock_data = Image.open("/home/ubuntu/Downloads/k2.png")
    mask = np.array(img_data)
    # plot world cloud- generate for all, then each chapter
    wordfreq1 = collections.Counter(data_flat1)
    # text = data_flat1
    plt.figure(figsize=(20, 10), facecolor='k')
    wordcloud = WordCloud(background_color="white", width=1080, height=960, max_words=2000,
                          font_path='/home/ubuntu/Downloads/chandas.ttf',
                          mask=mask,min_font_size = 5,stopwords=stopwords).generate_from_frequencies(wordfreq1)
                          #,contour_width=1, contour_color='steelblue'
                          # font_path='/home/ubuntu/Downloads/Yatra_One/YatraOne-Regular.ttf',
                          # stopwords=stopwords)
                          # /home/ubuntu/Downloads/lohit_devanagari/Lohit-Devanagari.ttf

    # wordcloud = WordCloud(font_path='/home/ubuntu/Downloads/chandas.ttf', width=1080, height=960,
    #                       background_color='black',
    #                       max_words=100,
    #                       collocations=False,
    #                       min_font_size=5).generate_from_frequencies(wordfreq)
    # wordcloud.to_file('plots/WC_krish.png')
    wordcloud.to_file('plots/' + savename)
    #show
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


    # #-----------create coloring from image
    # Colorimg = Image.open("plots/k2.png")
    # mask = np.array(Colorimg)
    # image_colors = ImageColorGenerator(mask)
    # # plot world cloud- generate for all, then each chapter
    # wordfreq1 = collections.Counter(data_flat1)
    # text = data_flat1
    # fig = plt.figure(figsize=(20, 10), facecolor='k')
    # wordcloud = WordCloud(background_color="white", width=1300, height=600, max_words=2000,
    #                       font_path='/home/ubuntu/Downloads/Eczar/Eczar-VariableFont_wght.ttf', mask=mask).generate(
    #     str(text))
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    # plt.axis("off")
    # plt.show()
    # wordcloud.to_file('plots/WC_krish.png')

class txt_color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'




if __name__ == "__main__":
    #-----------------------main code
    #--------redo getverse -save csv
    # get_verses()

    #---------------------ANALYSE Sanskrit
    # Opening JSON file
    # f = open('LP_verses.json')
    # Verses = json.load(f)
    # f.close()
    # ---------------OLD way
    # Verses=get_data('LP_verses.json')
    # df_verses = pd.DataFrame(Verses)
    # df_verses.rename(columns ={0:'hindi'}, inplace = True)
    # ----------------OLD way
    # nltk.download('punkt')
    # df.to_csv(file_name, sep='\t', encoding='utf-8')

    # Load data from analyse function
    BGdata= pd.read_csv('BG_dataframe.csv') # ['Chapter','Verse','Sanskrit','Transliteration']

    # --------------Barchart #------plot chapter-verse#
    # plot_barchart()

    #<---------------Transliteration section
    #get top n words
    top_n_translit,data_flat=get_top_words(BGdata,10)
    # for w in enumerate(top_n_translit):
    #     print(txt_color.PURPLE +'top 10 words are:' + txt_color.END + top_n_translit[w.index(0)])
    print(top_n_translit)

    #Make wordcloud of all verses
    Translit_Wordcloud(data_flat,'WC_krish.png')

    #Common words for each chapter - double check!
    # for i in range(1,2):
    #     # i=1
    #     BGdata2=BGdata[BGdata.Chapter==i]
    #     top_n_translit,data_flat=get_top_words(BGdata2,10)
    #     # print(top_n_translit)
    #     bgita = Text(data_flat)
    #     bgita.concordance('uvācha')
    #     print(f'"Krishna" appears {data_flat.count("kṛiṣhṇa")} time(s) in chapter {i}')
    #     print(f'"Arjuna" appears {data_flat.count("arjuna")} time(s) in chapter {i}')
    #     # print(f'"cha" appears {data_flat.count("cha")} time(s)')
    #     # savenm='wc_krish2_chapt{}.png'.format(i)
    #     # Translit_Wordcloud(data_flat,savenm)

    #Count speakers



    #<----------------------hindi section
    top_n_Sans,data_flat_sans=get_top_sanskrit_words(BGdata,15)
    print(top_n_Sans)
    # sanskrit_Wordcloud(data_flat_sans,'WC_sans_krish.png')
    print(f'"Krishna" appears {data_flat_sans.count("श्रीभगवानुवाच")} time(s)')
    print(f'"Arjuna" appears {data_flat_sans.count("अर्जुन" )} time(s)')

    # joined = " ".join(data_flat_sans)
    Krish_word_count=sum(data_flat_sans.count(x) for x in ("श्रीभगवानुवाच", "माधव","केशव","हृषिकेश","अच्युत","मधुसूदन","मुरारि","केशव","दामोदर","वसुदेव","गोविंद","मुरली"))
    print(Krish_word_count)

    #collect each speaker
    # Arjun_verse=[]
    # Arjun_verse_translit = []
    Krishna_verse = []
    Krishna_verse_translit = []

    Arjun_verse = pd.DataFrame(columns=['Chapter', 'Verse', 'Sanskrit', 'Transliteration'])

    for index,ver in enumerate(BGdata['Sanskrit']):
        line=ver
        translit_line=BGdata['Transliteration'][index]
        i=BGdata['Chapter'][index]
        v=BGdata['Verse'][index]

        if line.find(u'अर्जुन उवाच') > -1:
            speaker = 'Arjun'
            Arjun_verse=Arjun_verse.append({'Chapter': i, 'Verse': v, 'Sanskrit': line, 'Transliteration': translit_line},ignore_index = True)
            # Arjun_verse.append(line)
            # Arjun_verse_translit.append(translit_line)
            continue
        if line.find(u'श्रीभगवानुवाच') > -1:
            speaker = 'Bhagawan'
            Krishna_verse.append(line)
            Krishna_verse_translit.append(translit_line)
            continue
        if line.find(u'सञ्जय उवाच') > -1:
            speaker = 'Sanjay'
            continue
        if line.find(u'धृतराष्ट्र उवाच') > -1:
            speaker = 'Dhritarashtra'
            continue
        # if (line.find(u'ॐ तत्सदिति श्रीमद्भगवद्गीतासूपनिषत्सु') > -1) or (line.find(u'ब्रह्मविद्यायां') > -1) or (
        #         line.find(u'ध्यायः') > -1):
        #     speaker = 'None'
        #     continue
    for idx,v in enumerate(Arjun_verse['Transliteration']):
        # print(v)

        chpt=Arjun_verse['Chapter'][idx]
        vrs=Arjun_verse['Verse'][idx]
        print(f'Chapter {chpt}.{vrs}: {v}')





    #plot world cloud- generate for all, then each chapter
    for i in range(1,2):
        # i=1
        BGdata2=BGdata[BGdata.Chapter==i]
        top_n_Sans,data_flat_sans=get_top_sanskrit_words(BGdata2,10)
        # print(top_n_translit)
        # bgita = Text(data_flat)
        # bgita.concordance('uvācha')
        print(f'"Krishna" appears {data_flat_sans.count("श्रीभगवानुवाच")} time(s) in chapter {i}')
        print(f'"Krishna" appears {data_flat_sans.count("हृषीकेशो")} time(s) in chapter {i}')
        print(f'"Arjuna" appears {data_flat_sans.count("अर्जुन")} time(s) in chapter {i}')
        # print(f'"cha" appears {data_flat.count("cha")} time(s)')
        # savenm='wc_sans_krish2_chapt{}.png'.format(i)
        # sanskrit_Wordcloud(data_flat_sans,savenm)


