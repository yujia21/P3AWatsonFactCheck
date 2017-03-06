
# coding: utf-8

# In[1]:

get_ipython().system(u'jupyter nbconvert --to script Compare.ipynb')


# In[21]:

def compare_keywords(keywords):
    nb_phrases = 0
    nb_good_phrases = 0
    nb_gp_per_rel = []
    nb_p_per_rel = []
    page_phrases = 0
    
    for rel in keywords['relations']:
        phrases = list(set([phrase for sublist in rel[4] for phrase in sublist]))
        nb_phrases += len(phrases)
        nb_good_phrases += len(rel[3])
        nb_p_per_rel.append(len(phrases))
        nb_gp_per_rel.append(len(rel[3]))
        page_phrases += rel[5]
        print('Total sentences : '+str(rel[5]))
        print('Total sentences with 1 keyword : '+str(len(phrases)))
        print('Total sentences with 2 keywords: '+str(len(rel[3])))

    p = 1/float(nb_phrases+nb_good_phrases)
    final_prob = 0
    
    for rel in keywords['relations']:
        for phrase in phrases:
            final_prob += 0.5 * p
        for gd_phrase in rel[3]:
            final_prob += p
    
    if (final_prob >= 0.5) and (nb_phrases/page_phrases >=0.1) :
        print(final_prob)
        return True
    else : 
        print(final_prob)
        return False


# In[24]:

def compare_keywords_dbpedia(keywords):
    count = 0
    tot_count = 0
    
    for relation in keywords['relations'] :
        if (len(relation) == 0):
            return "Error in parsing input"
        tot_count += len(relation[-2])
        count += sum(relation[-2])
    if (tot_count == 0) : 
        return False
    else : 
        print (count*1.0/tot_count)
        return (count*1.0/tot_count > 0.5) and (len(keywords['negations']) == 0)


# In[17]:

'''
k1 = {'negations': ['not'], 'dates': [], 'relations': [['Lee Hsien Loong', ['prime minister', 'Singapore'], 'residesIn', [True, True], "Lee Hsien Loong (Chinese: 李显龙, pinyin: Lǐ Xiǎnlóng; born 10 February 1952) is a Singaporean politician. He is the third and current Prime Minister of Singapore, and has been in office since 2004. He is the eldest son of Singapore's first Prime Minister, Lee Kuan Yew. As the Secretary-General of the People's Action Party (PAP), Lee became Prime Minister in August 2004, succeeding Goh Chok Tong. He has been a Member of Parliament (MP) for Teck Ghee since 1984 and a member of the Cabinet since 1987, and was one of the key leaders in Singapore's political transition in the 1980s and 1990s. Before becoming Prime Minister in 2004 he served as the Minister for Trade and Industry, Minister for Finance and Deputy Prime Minister. Prior to his election to Parliament, he served as an officer in the Singapore Armed Forces, quickly rising to the rank of Brigadier-General.[citation needed]"]]}
k2 = {'negations': [], 'dates': [], 'relations': [['Ban Ki-moon', ['president', 'UN'], 'employedBy', [True, True], "Ban Ki-moon (Hangul: 반기문; hanja: 潘基文; born 13 June 1944) is a South Korean statesman and politician who is the eighth and current Secretary-General of the United Nations. Before becoming Secretary-General, Ban was a career diplomat in South Korea's Ministry of Foreign Affairs and in the United Nations. He entered diplomatic service the year he graduated from university, accepting his first post in New Delhi, India. Ban was the foreign minister of South Korea from January 2004 to November 2006. In February 2006 he began to campaign for the office of Secretary-General. Ban was initially considered a long shot for the office. As foreign minister of South Korea, however, he was able to travel to all the countries on the United Nations Security Council, a maneuver that turned him into the campaign's front runner. On 13 October 2006, he was elected to be the eighth Secretary-General by the United Nations General Assembly. On 1 January 2007, he succeeded Kofi Annan. Ban struggled in his first month to adjust to the culture of the United Nations, but quickly found his bearings and passed several major reforms on peacekeeping and UN employment practices.[citation needed] Diplomatically, Ban has taken particularly strong views on global warming, pressing the issue repeatedly with U.S. President George W. Bush, and on the Darfur conflict, where he helped persuade Sudanese president Omar al-Bashir to allow peacekeeping troops to enter Sudan. Ban was named the world's 32nd most powerful person by the Forbes list of The World's Most Powerful People in 2013, the highest among South Koreans. In 2014, he was named the third most powerful South Korean after Lee Kun-Hee and Lee Jae-yong."]]}
k3 = {'negations': [], 'dates': [('20170101T000000', '2017')], 'relations': [['Donald Trump', ['president', 'US'], 'residesIn', [True, True, False], 'Donald John Trump (born June 14, 1946) is an American businessman, politician, and television personality. He is a candidate for the Republican nomination for President of the United States in the 2016 election. Trump is the chairman and president of The Trump Organization and the founder of Trump Entertainment Resorts, a gaming and hotel enterprise. His extensive self promotion, outspoken manner, career, personal life and wealth have made him a celebrity. Trump is a native of New York City and a son of Fred Trump, who inspired him to enter real estate development. While still attending college he worked for his father\'s firm, Elizabeth Trump & Son. Upon graduating from college in 1968 he joined the company, and in 1971 was given control, renaming the company "The Trump Organization." Since then he has built casinos, golf courses, hotels and other properties, many of which bear his name. He has received prominent media exposure and the NBC reality show The Apprentice bolstered his fame. His three marriages were extensively covered in tabloids. He first ran for President of the United States in 2000, winning two Reform Party primaries. On June 16, 2015, Trump announced his decision to run again for President, this time as a Republican. He won the New Hampshire primary with 35% of the vote, the South Carolina primary with 33% and the Nevada caucuses with 46%. On Super Tuesday in March 2016, Trump won Alabama, Arkansas, Georgia, Massachusetts, Tennessee, Vermont, and Virginia, solidifying his status as the Republican frontrunner.']]}

print(compare_keywords_dbpedia(k1))
print(compare_keywords_dbpedia(k2))
print(compare_keywords_dbpedia(k3))
'''

