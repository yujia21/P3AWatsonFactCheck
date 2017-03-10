
# coding: utf-8

# In[15]:

def compare_keywords_dbpedia(keywords):
    count = 0
    tot_count = 0
    precise_count = 0
    for relation in keywords['relations'] :
        # if no relations
        if (len(relation) == 0):
            return "Error in parsing input"
        
        # total objects searched
        tot_count += len(relation[3])
        # total objects present in abstract
        count += sum(relation[3])
        
        # if precise count
        if (len(relation[5])!= 0) :
            # add true on total number of precise counts searched
            precise_count += sum(relation[5])/len(relation[5])

    # if no objects
    if (tot_count == 0) : 
        return "Error in parsing input"
    else : 
        # no precise : rely only on abstract. 
        if (precise_count == 0):
            truth_p = count*1.0/tot_count
        # has precise : half of precise + half of obj in abstract
        else : 
            truth_p = precise_count/2.0 + count/tot_count/2.0
        
        # if negation, flip truth value
        if (len(keywords['negations']) != 0) : 
            truth_p = 1-truth_p
        
        print('Truth percentage : '+str(truth_p))
        return (truth_p > 0.5)


# In[16]:

'''
k1 = {'negations': [], 'relations': [['Lee Hsien Loong', [['prime minister', ''], 'Singapore', ['Singapore', 'GeopoliticalEntity']], 'residesIn', [True, True, True], "Lee Hsien Loong (Chinese: 李显龙, pinyin: Lǐ Xiǎnlóng; born 10 February 1952) is a Singaporean politician. He is the third and current Prime Minister of Singapore, and has been in office since 2004. He is the eldest son of Singapore's first Prime Minister, Lee Kuan Yew. As the Secretary-General of the People's Action Party (PAP), Lee became Prime Minister in August 2004, succeeding Goh Chok Tong. He has been a Member of Parliament (MP) for Teck Ghee since 1984 and a member of the Cabinet since 1987, and was one of the key leaders in Singapore's political transition in the 1980s and 1990s. Before becoming Prime Minister in 2004 he served as the Minister for Trade and Industry, Minister for Finance and Deputy Prime Minister. Prior to his election to Parliament, he served as an officer in the Singapore Armed Forces, quickly rising to the rank of Brigadier-General.[citation needed]", [True, True]]], 'dates': []}
k2 = {'negations': [], 'relations': [['Ban Ki Moon', [['president', ''], 'UN', ['UN', 'Organization']], 'employedBy', [True, True, True], "Ban Ki-moon (Hangul: 반기문; hanja: 潘基文; born 13 June 1944) is a South Korean statesman and politician who is the eighth and current Secretary-General of the United Nations. Before becoming Secretary-General, Ban was a career diplomat in South Korea's Ministry of Foreign Affairs and in the United Nations. He entered diplomatic service the year he graduated from university, accepting his first post in New Delhi, India. Ban was the foreign minister of South Korea from January 2004 to November 2006. In February 2006 he began to campaign for the office of Secretary-General. Ban was initially considered a long shot for the office. As foreign minister of South Korea, however, he was able to travel to all the countries on the United Nations Security Council, a maneuver that turned him into the campaign's front runner. On 13 October 2006, he was elected to be the eighth Secretary-General by the United Nations General Assembly. On 1 January 2007, he succeeded Kofi Annan. Ban struggled in his first month to adjust to the culture of the United Nations, but quickly found his bearings and passed several major reforms on peacekeeping and UN employment practices.[citation needed] Diplomatically, Ban has taken particularly strong views on global warming, pressing the issue repeatedly with U.S. President George W. Bush, and on the Darfur conflict, where he helped persuade Sudanese president Omar al-Bashir to allow peacekeeping troops to enter Sudan. Ban was named the world's 32nd most powerful person by the Forbes list of The World's Most Powerful People in 2013, the highest among South Koreans. In 2014, he was named the third most powerful South Korean after Lee Kun-Hee and Lee Jae-yong.", [False]]], 'dates': []}
k3 = {'negations': [], 'relations': [['Donald Trump', [['president', ''], 'US', ['US', 'GeopoliticalEntity']], 'residesIn', [True, True, True, True], 'Donald John Trump (born June 14, 1946) is an American businessman, politician, and television personality. He is a candidate for the Republican nomination for President of the United States in the 2016 election. Trump is the chairman and president of The Trump Organization and the founder of Trump Entertainment Resorts, a gaming and hotel enterprise. His extensive self promotion, outspoken manner, career, personal life and wealth have made him a celebrity. Trump is a native of New York City and a son of Fred Trump, who inspired him to enter real estate development. While still attending college he worked for his father\'s firm, Elizabeth Trump & Son. Upon graduating from college in 1968 he joined the company, and in 1971 was given control, renaming the company "The Trump Organization." Since then he has built casinos, golf courses, hotels and other properties, many of which bear his name. He has received prominent media exposure and the NBC reality show The Apprentice bolstered his fame. His three marriages were extensively covered in tabloids. He first ran for President of the United States in 2000, winning two Reform Party primaries. On June 16, 2015, Trump announced his decision to run again for President, this time as a Republican. He won the New Hampshire primary with 35% of the vote, the South Carolina primary with 33% and the Nevada caucuses with 46%. On Super Tuesday in March 2016, Trump won Alabama, Arkansas, Georgia, Massachusetts, Tennessee, Vermont, and Virginia, solidifying his status as the Republican frontrunner.', [False, False]]], 'dates': [('20170101T000000', '2017')]}

print(compare_keywords_dbpedia(k1))
print(compare_keywords_dbpedia(k2))
print(compare_keywords_dbpedia(k3))
'''

