def compare_keywords_dbpedia(keywords):
    count = 0
    tot_count = 0
    precise_count = 0
    for relation in keywords['relations'] :
        if (len(relation) == 0):
            return "Error in parsing input"
        tot_count += len(relation[3])
        count += sum(relation[3])
        if (len(relation[5])!= 0) :
            precise_count += sum(relation[5])/len(relation[5])
    if (tot_count == 0) : 
        return False
    else : 
        if (precise_count == 0):
            print(count*1.0/tot_count)
            return (count*1.0/tot_count > 0.5) and (len(keywords['negations']) == 0)
        else : 
            print(precise_count/2.0 + count/tot_count/2.0)
            return ((precise_count/2.0 + count/tot_count/2.0) > 0.5) and (len(keywords['negations']) == 0)