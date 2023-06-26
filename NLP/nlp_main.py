import spacy
import csv
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow_hub as hub
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import commonFunctions


nlp = spacy.load("en_core_web_lg")
module_url = "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"
tf.compat.v1.disable_eager_execution()

test_list_labels = ["SAME 1", "SAME 2", "SAME 3", "SAME 4", "SIMILAR 1", "SIMILAR 2", "DIFF 1", "DIFF 2"]
test_list = []

test_article1_same1 = """LONDON, Jan 19 (Reuters) - About two billion tonnes of carbon dioxide are being removed from the atmosphere every year, according to a report published on Thursday, but nearly all of it is accomplished through forests, despite growing investments in new technologies. The independent report, led by the University of Oxford, is the first to assess how much CO2 removal the world is already achieving - and how much more is needed. It estimates that roughly 1,300 times more carbon dioxide removal from new technologies — and twice as much from trees and soils — are needed by 2050 to limit temperatures to well below 2 degrees Celsius above pre-industrial temperatures, as set out in the Paris Agreement. "CO2 removal is rapidly moving up agendas," said report co-author Steve Smith, a climate scientist at the University of Oxford. But he said that despite growing interest and investment, "there are major gaps in information". CO2 removal involves capturing the greenhouse gas from the atmosphere and storing it for a long period of time either on land, in the ocean, in geological formations or in products. To date, almost all successful CO2 removal has been achieved through measures like planting trees and better managing soils. From 2020 to 2022, global investment in new CO2 removal capacity totalled around $200 million, according to the report, while some $4 billion has been funnelled into publicly-funded research and development since 2010. Although countries aren't currently planning to use CO2 removal to meet short-term climate goals by 2030, many envision it as part of their strategy for reaching net zero by 2050. Report co-author Jan Minx, of the Mercator Research Institute on Global Commons and Climate Change in Germany, said that while reducing emissions remains the top priority for reaching the Paris goal, "at the same time, we need to also aggressively develop and scale up CO2 removal, particularly those novel methods." He added that would take time as "we are still at the very start". Last December, the U.S. Department of Energy committed $3.7 billion to finance CO2 removal projects. And the European Union aims to capture five million tonnes of CO2 annually by 2030."""
test_list.append(test_article1_same1)
test_article1_same2 = """About two billion tonnes of carbon dioxide are being removed from the atmosphere every year, according to a report, but nearly all of it is accomplished through forests, despite growing investments in new technologies. The independent report published on Thursday and led by the University of Oxford is the first to assess how much CO2 removal the world is already achieving — and how much more is needed. It estimates that roughly 1,300 times more carbon dioxide removal from new technologies — and twice as much from trees and soils — are needed by 2050 to limit temperatures to well below 2 degrees Celsius above pre-industrial temperatures, as set out in the Paris Agreement. "CO2 removal is rapidly moving up agendas," said report co-author Steve Smith, a climate scientist at the University of Oxford, but he said that despite growing interest and investment, "there are major gaps in information." CO2 removal involves capturing the greenhouse gas from the atmosphere and storing it for a long period of time either on land, in the ocean, in geological formations or in products. To date, almost all successful CO2 removal has been achieved through measures like planting trees and better managing soils."""
test_list.append(test_article1_same2)
test_article1_same3 = """About two billion tonnes of carbon dioxide are being removed from the atmosphere every year, according to a report published on Thursday, but nearly all of it is accomplished through forests, despite growing investments in new technologies. The independent report, led by the University of Oxford, is the first to assess how much CO2 removal the world is already achieving - and how much more is needed. It estimates that roughly 1,300 times more carbon dioxide removal from new technologies — and twice as much from trees and soils — are needed by 2050 to limit temperatures to well below 2 degrees Celsius above pre-industrial temperatures, as set out in the Paris Agreement. "CO2 removal is rapidly moving up agendas," said report co-author Steve Smith, a climate scientist at the University of Oxford. But he said that despite growing interest and investment, "there are major gaps in information". CO2 removal involves capturing the greenhouse gas from the atmosphere and storing it for a long period of time either on land, in the ocean, in geological formations or in products. To date, almost all successful CO2 removal has been achieved through measures like planting trees and better managing soils. From 2020 to 2022, global investment in new CO2 removal capacity totalled around $200 million, according to the report, while some $4 billion has been funnelled into publicly-funded research and development since 2010. Although countries aren't currently planning to use CO2 removal to meet short-term climate goals by 2030, many envision it as part of their strategy for reaching net zero by 2050. Report co-author Jan Minx, of the Mercator Research Institute on Global Commons and Climate Change in Germany, said that while reducing emissions remains the top priority for reaching the Paris goal, "at the same time, we need to also aggressively develop and scale up CO2 removal, particularly those novel methods." He added that would take time as "we are still at the very start". Last December, the US Department of Energy committed $3.7 billion to finance CO2 removal projects. And the European Union aims to capture five million tonnes of CO2 annually by 2030."""
test_list.append(test_article1_same3)
test_article1_same4 = """About two billion tonnes of carbon dioxide are being removed from the atmosphere every year, according to a report published on Thursday (19 January), but nearly all of it is accomplished through forests, despite growing investments in new technologies. The independent report, led by the University of Oxford, is the first to assess how much CO2 removal the world is already achieving - and how much more is needed. It estimates that roughly 1,300 times more carbon dioxide removal from new technologies - and twice as much from trees and soils - are needed by 2050 to limit temperatures to well below 2 degrees Celsius above pre-industrial temperatures, as set out in the Paris Agreement. “CO2 removal is rapidly moving up agendas,” said report co-author Steve Smith, a climate scientist at the University of Oxford. But he said that despite growing interest and investment, “there are major gaps in information”. CO2 removal involves capturing the greenhouse gas from the atmosphere and storing it for a long period of time either on land, in the ocean, in geological formations or in products. To date, almost all successful CO2 removal has been achieved through measures like planting trees and better managing soils. From 2020 to 2022, global investment in new CO2 removal capacity totalled around $200 million, according to the report, while some $4 billion has been funnelled into publicly-funded research and development since 2010. Although countries aren't currently planning to use CO2 removal to meet short-term climate goals by 2030, many envision it as part of their strategy for reaching net zero by 2050. Report co-author Jan Minx, of the Mercator Research Institute on Global Commons and Climate Change in Germany, said that while reducing emissions remains the top priority for reaching the Paris goal, “at the same time, we need to also aggressively develop and scale up CO2 removal, particularly those novel methods.” He added that would take time as “we are still at the very start”. CO2 removals “is not something we could do, but something we absolutely have to do to reach the Paris Agreement temperature goal,” added Oliver Geden of the German Institute for International and Security Affairs. According to Dr Geden, “more than 120 national governments have a net-zero emissions target, which implies using CDR, but few governments have actionable plans for developing it. This presents a major shortfall.” Last December, the US Department of Energy committed $3.7 billion to finance CO2 removal projects. And the European Union aims to capture five million tonnes of CO2 annually by 2030."""
test_list.append(test_article1_same4)
test_article1_similar1 = """Vast amounts of planet-heating carbon dioxide are created during the manufacture of many key materials that support our lives - from paper to plastic. Our environment analyst Roger Harrabin has been exploring new low-carbon technologies which could help cut those emissions. He has enlisted artists to help him tell the story. Scientists have invented a magical gadget that sucks the ink off printer paper so each sheet can be used 10 times over. They aim to cut the amount of planet-heating carbon dioxide (CO2) emissions from the paper and pulp industry by reducing demand for office paper. The trick to the so-called "de-printer" is specially coated paper, which stops ink (or powdered toner) from soaking into the page. A powerful laser then vaporises the ink. Lead developer, Barak Yekutiely from Reep Technologies in Israel, describes it as circular printing. "If we care about the planet, we must stop cutting down so many trees," he says. The invention is featured in an iPlayer documentary on climate tech solutions. It's called The Art of Cutting Carbon, and it's my last film for the BBC after 35 years reporting the environment. The film forms part of an exhibition at Cornwall's Eden Project, where I have curated sculptures in steel, cement, plastic, aluminium and paper - to help me highlight the huge amounts of planet-heating CO2 produced globally from manufacturing these everyday materials. Experts say one way of tackling those emissions is to invent new technologies that limit the amount of CO2 produced. Another is simply to use less stuff. The de-printer is part of an avalanche of innovation to produce technologies fit for the low-carbon age. In northern Sweden, one company is a shining example of how to take CO2 out of steel manufacturing. Globally, the industry emits almost three billion tonnes of the gas a year - that's roughly equal to all the annual CO2-producing activities in the entire Indian economy. Normally, making steel involves mixing iron-bearing rock with coke - which derives from coal - then super-heating it at 1,500C, using highly-polluting coal or gas. The heat sets off a chemical reaction that turns the iron into a precursor of steel. But this creates even more CO2 - in fact, the process makes more tonnes of CO2 than it makes steel. But now, in the town of Lulea - just south of the Arctic Circle - the multinational steel manufacturer SSAB has found a way of stopping the creation of CO2. The first step is to use renewable power - such as from wind turbines or hydro electricity - instead of coal to produce the necessary heat. Step two is to substitute hydrogen for coke in the reaction stage. Instead of producing CO2 as a by-product, the reaction with hydrogen and iron produces only H2O… water. Demand is high for the world's first zero-carbon dioxide steel - the makers are turning down new orders. The cement industry produces 2.5 billion tonnes of CO2 a year. Cement is the main bonding ingredient for the concrete that forms the structures in our lives. But making it involves heating limestone and that creates clouds of CO2. Harnessing coal or gas to provide the heat creates a double dose. Now concrete makers are experimenting with other binding materials that don't need to be cooked in the same way, and big players in the industry aim to be carbon neutral by 2050. But we can't wait that long to tackle climate change, so the rail firm HS2 is building a viaduct in Buckinghamshire in south-east England made from a sandwich of cement and steel. This smart design allows less material to be used by harnessing the different physical properties of the cement and steel in a way that's catching on fast. The engineers say this innovation cuts materials costs and halves the CO2 emissions that would have been seen in a more traditional construction. Of course, taking a decision not to build the controversial HS2 route in the first place would have saved many more emissions. And there's a growing trend among engineers to try to squeeze more out of infrastructure that already exists, such as refurbishing buildings instead of knocking them down and using cement to build replacements. The plastics industry is another of the top five CO2 offenders. Almost all the world's plastic is derived from high-polluting oil and gas. But in the Netherlands a bio-chemical firm Avantium is claiming a world first - a plant-based plastic to rival PET, (polyethylene terephthalate) which is used to make most drinks bottles. The new product is called PEF (polyethylene furanoate) and is said to produce a third fewer emissions than PET. The raw material is derived from wheat and corn. I've tasted it and it's just like eating sugar."""
test_list.append(test_article1_similar1)
test_article1_similar2 = """Energy-related carbon dioxide emissions “flatlined” last year, the International Energy Agency said Tuesday in a report that raised hopes about the Earth's climate. Global emissions remained at approximately 33 gigatonnes in 2019 despite the world economy growing by 2.9%, the IEA said. The agency cited several factors, including a drop in emissions from electricity production in advanced economies due to the “expanding role” of renewables like wind and solar. Other factors included increased nuclear power generation, fuel switching to natural gas from coal, milder weather and slower economic growth in several emerging markets. “We now need to work hard to make sure that 2019 is remembered as a definitive peak in global emissions, not just another pause in growth,” IEA executive director Fatih Birol said in a statement. “We have the energy technologies to do this, and we have to make use of them all.“ Breaking some of the figures down, the U.S. saw energy-related CO2 emissions drop by 140 million tons — just under 3% — to 4.8 gigatonnes, nearly 1 Gt lower than their peak in 2000. Coal use for power generation declined by 15% in the United States. The European Union saw emissions decline by 160 million tons — equivalent to 5% — while Japan's emissions dropped by 45 million tons. In the EU, output from coal-fired plants fell by over 25% last year, the IEA said, with gas-fired generation rising by “close to 15% to overtake coal for the first time.” While the above is a positive, the IEA said emissions from outside “advanced economies” had increased by “close to” 400 million tons in 2019, with nearly 80% of this rise coming from countries in Asia. “The news that global energy-related emissions stopped growing in 2019, driven by a continued reduction in coal-powered electricity production in developed countries, is a sign of real progress in the fight to prevent dangerous climate change,” Simon Retallack, a director at the Carbon Trust, said in a statement. Retallack said it was “vital” that the pause was not a temporary one. “To ensure global emissions have peaked for good, developing as well as developed economies will need to embrace cleaner power generation at a faster pace,” he said. “They will also need to ensure emissions from other sectors, notably transport and agriculture, stop rising and begin to fall.”"""
test_list.append(test_article1_similar2)
test_not_similar_article1 = """At times, Joe Biden is his own worst enemy. When asked on Thursday whether it was true he had kept classified documents in a garage next to his sports car, he responded in a rather flippant manner that the garage was locked. That will lead some to wonder about the protestations from the White House that they are taking seriously the matter of whether Mr Biden mishandled classified materials after leaving the office of vice-president in 2017. But the justice department's appointment of a special counsel will concentrate minds and will undoubtedly overshadow the president's next months in office. He will also, eventually, have to answer the question of why it took so long to tell the public what had happened. The first batch was discovered a week before the midterm elections last November; did political considerations at the time colour the decisions that were made? It does not help matters that the second batch of documents, allegedly discovered by aides for the first time on Wednesday, were at his home in Wilmington, Delaware. In the two years he has been president, Mr Biden has logged 60 trips back to his home state, according to former CBS News correspondent and unofficial presidential statistics guru Mark Knoller. Locked or not, who else had access to the garage? No doubt Mr Biden's supporters and lawyers will argue there are key differences between the way Donald Trump behaved, with regard to his own alleged mishandling of documents, and how President Biden and his aides have handled the matter. It is true Mr Trump held on to hundreds of classified documents, failed to hand them all over when asked, and faced an FBI search warrant when the authorities lost patience with his lawyers. In contrast, Mr Biden's lawyers say that his case involves a small number of papers, the retention of which was inadvertent, and that they have co-operated at every stage. But those distinctions may pass most Americans by, leaving the Biden administration tarred with the same brush as its predecessor, damaging any claim it might have had to be pursuing the moral high ground. And with inflation falling and his approval ratings rebounding, the document discoveries will trim Mr Biden's sails as he prepares to campaign for re-election in 2024. An announcement on that was expected in the next few weeks. This terrible week for Biden may have his team reassessing that."""
test_list.append(test_not_similar_article1)
test_not_similar_article2 = """The Dutch government has decided to stop describing itself as Holland and will instead use only its real name - the Netherlands - as part of an attempted update of its global image. The national rebranding, which has been signed up to by business leaders, the tourist board and central government, will be rolled out later this year. Ministers want to shift the international focus from certain aspects of national life with which the country is commonly associated, such as its recreational drug culture and the red-light district of Amsterdam. As part of the new strategy, the Netherlands will be the official brand at the Eurovision song contest, which takes place in Rotterdam next May, and during the Olympic Games in Tokyo in 2020. The nation's football team, which is often referred to abroad as Holland, will solely be called the Netherlands in any official setting. A spokeswoman for the ministry of foreign affairs said the Netherlands needed a more uniform and coordinated national branding. She said: “We want to present the Netherlands as an open, inventive and inclusive country. We've modernised our approach. “What is special is that agreement has now been reached with relevant parties from both the government, Netherlands Board of Tourism and Conventions and private organisations including top sectors and the Confederation of Netherlands Industry and Employers about the image of the Netherlands that we want to present to the rest of the world in a substantive and unambiguous manner.” She said the government was taking a user-friendly and pragmatic approach to its name in order to boost exports, tourism, sport and spread “Dutch culture, norms and values”. She said: “It has been agreed that the Netherlands, the official name of our country, should preferably be used.” North and South Holland are provinces on the western coast of the Netherlands. From the 10th to the 16th century, Holland was one political unified entity and ruled by the counts of Holland. By the 17th century it was the dominant part of what was then the Dutch Republic. The kingdom of the Netherlands, from the Dutch Neder-landen, meaning low countries, emerged out of the defeat of Napoleon at the Battle of Waterloo in 1815. Earlier this year, the Dutch tourist board, whose website address is Holland.com, said it would be moving its focus from promoting the Netherlands as a whole to drawing attention instead to less well-known parts of the country. As many as 42 million people are forecast to visit the country annually by 2030, up from 18 million in 2018. Amsterdam's well-known attractions are a major pull factor, leading to complaints of overcrowding in the Dutch capital."""
test_list.append(test_not_similar_article2)


def heatmap(x_labels, y_labels, values):
    fig, ax = plt.subplots()
    im = ax.imshow(values)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10,
         rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, "%.2f"%values[i, j],
                           ha="center", va="center", color="w", fontsize=6)

    fig.tight_layout()
    plt.show()


def open_csv(file_name):
    
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data


def dataSet_to_listOfArticles(data_set):

    result_list  = []

    for j in range(len(data_set)):
        
        if len(data_set[j]) == 0 : #for titles #or data_set[j][0] ==  ""
            print(True)
            continue
        if data_set[j][1] == "":
            continue
        else:
            result_list.append(data_set[j])

    return result_list


def only_article_list(data):

    result_list  = []

    for j in range(len(data)):
        
        if len(data[j]) == 0 : #for titles #or data_set[j][0] ==  ""
            print(True)
            continue
        if data[j][1] == "":
            print("IS TRUE BUT SHOULD NOT BE!!!")
            continue
        else:
            result_list.append(data[j][1])

    return result_list


def determine_which_list(firstListName, secondListName):

    if firstListName == "BBC":
        active_data1 = bbcData
    if secondListName == "BBC":
        active_data2 = bbcData
    if firstListName == "TheSun":
        active_data1 = sunData
    if secondListName == "TheSun":
        active_data2 = sunData
    if firstListName == "DailyMail":
        active_data1 = dailyMailData
    if secondListName == "DailyMail":
        active_data2 = dailyMailData
    if firstListName == "TheMirror":
        active_data1 = mirrorData
    if secondListName == "TheMirror":
        active_data2 = mirrorData
    if firstListName == "TheGuardian":
        active_data1 = guardianData
    if secondListName == "TheGuardian":
        active_data2 = guardianData

    return active_data1, active_data2
    
    
def corr (firs_list, second_list):


    #first_list_articles = only_article_list(firs_list)
    #second_list_articles = only_article_list(second_list)

    embed = hub.Module(module_url)

    similarity_input_placeholder = tf.compat.v1.placeholder(tf.string, shape=(None))
    similarity_message_encodings = embed(similarity_input_placeholder)
    with tf.compat.v1.Session() as session:
        session.run(tf.compat.v1.global_variables_initializer())
        session.run(tf.compat.v1.tables_initializer())
        message_embeddings_ = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: firs_list})
        message_embeddings_1 = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: second_list})

        corr = np.inner(message_embeddings_, message_embeddings_1)
        print(corr)
        print(type(corr))
        np.savetxt("distances_of_mixed_100_3e.csv", corr, delimiter=",", fmt="%.3e")
        
        #SORTING WHERE IS THE BIAS PART
        """

        temp_list = []
        test_list = []

        for i in range(len(corr)):
            i_is_there = False

            for j in range(len(corr[i])):
                
                print(corr[i][j])
                if corr[i][j] > 0.9 and i != j:
                    if not i_is_there:
                        temp_list.append(firs_list[i+1])
                        test_list.append(first_list_articles[i])
                        i_is_there = True
                    test_list.append(first_list_articles[j])
                    temp_list.append(firs_list[j+1])

                    print(temp_list)

            left_right = [0, 0, 0, 0, 0]

            print("NEW TEMP LIST ABOUT TO BEGIN")

            for k in temp_list:
                if ".bbc." in k[2]:
                    left_right[2] = 1
                if ".theguardian." in k[2]:
                    left_right[0] = 1
                if ".mirror." in k[2]:
                    left_right[1] = 1
                if ".thesun." in k[2]:
                    left_right[3] = 1
                if ".dailymail." in k[2]:
                    left_right[4] = 1

            if left_right[0] == 1 and left_right[1] == 1 and left_right[2] == 1 and left_right[3] == 0 and left_right[4] == 0:
                commonFunctions.write_row_to_csv("NOT COVERED", "BY RIGHT", "test2.csv", "COVERED BY LEFT AND CENTRE")
                for n in temp_list:
                    commonFunctions.write_row_to_csv(n[0], n[1], "test2.csv", n[2])
                commonFunctions.write_row_to_csv("GAP", "GAP", "test2.csv", "GAP")

            if left_right[0] == 1 and left_right[1] == 1 and left_right[2] == 0 and left_right[3] == 0 and left_right[4] == 0: 
                commonFunctions.write_row_to_csv("NOT COVERED", "BY RIGHT", "test2.csv", "AND NOT COVERED BY CENTRE")
                for n in temp_list:
                    commonFunctions.write_row_to_csv(n[0], n[1], "test2.csv", n[2])
                commonFunctions.write_row_to_csv("GAP", "GAP", "test2.csv", "GAP")

            if left_right[0] == 0 and left_right[1] == 0 and left_right[2] == 1 and left_right[3] == 1 and left_right[4] == 1:
                commonFunctions.write_row_to_csv("NOT COVERED", "BY LEFT", "test2.csv", "COVERED BY RIGHT AND CENTRE")
                for n in temp_list:
                    commonFunctions.write_row_to_csv(n[0], n[1], "test2.csv", n[2])
                commonFunctions.write_row_to_csv("GAP", "GAP", "test2.csv", "GAP")

            if left_right[0] == 0 and left_right[1] == 0 and left_right[2] == 0 and left_right[3] == 1 and left_right[4] == 1:
                commonFunctions.write_row_to_csv("NOT COVERED", "BY LEFT", "test2.csv", "AND NOT COVERED BY CENTRE")
                for n in temp_list:
                    commonFunctions.write_row_to_csv(n[0], n[1], "test2.csv", n[2])
                commonFunctions.write_row_to_csv("GAP", "GAP", "test2.csv", "GAP")

            temp_list = []
            left_right = [0, 0, 0, 0, 0] """




        """print(firs_list[i]) # to print correctly from OPEN CSV file
        similar_to_csv(firs_list[i])
        print(second_list[j]) # to print correctly from OPEN CSV file
        similar_to_csv(second_list[j])"""

            

        heatmap(test_list_labels, test_list_labels, corr)


def similar_to_csv(data_cell):

    file_name = "similar_articles.csv"
    commonFunctions.write_row_to_csv(data_cell[0], data_cell[1], file_name, data_cell[2])


all_articles = open_csv("similar_articles_finished.csv")

all_one_file = open_csv("AllArticles.csv")

mixed_example = open_csv("mixed_sample_20_each.csv")

publishers_list  = ["BBC", "TheMirror", "TheSun", "TheGuardian", "DailyMail"]

"""
#------- open all csv files, store data to variables
#data_list = []
bbcData = open_csv('BBC_Data.csv')
#data_list.append(bbcData)
mirrorData = open_csv('mirror_Data.csv')
#data_list.append(mirrorData)
sunData = open_csv("theSun_Data.csv")
#data_list.append(sunData)
guardianData = open_csv("Guardian_Data.csv")
#data_list.append(guardianData)
dailyMailData = open_csv("Daily_Mail_Data.csv")
#data_list.append(dailyMailData)
"""
"""
#------- extact article texts into list from data sets
article_txt_list = []
bbcList = dataSet_to_listOfArticles(bbcData)
article_txt_list.append(bbcList)
mirrorList = dataSet_to_listOfArticles(mirrorData)
article_txt_list.append(mirrorList)
sunList =  dataSet_to_listOfArticles(sunData)
article_txt_list.append(sunList)
guardianList = dataSet_to_listOfArticles(guardianData)
article_txt_list.append(guardianList)
dailyMailList = dataSet_to_listOfArticles(dailyMailData)
article_txt_list.append(dailyMailList)
"""




corr(test_list, test_list)




























"""
#IF-IDF
vect = TfidfVectorizer(min_df = 1, stop_words = "english")

tfidf = vect.fit_transform(article_list)

pairwise_similarity = tfidf * tfidf.T

array = pairwise_similarity.toarray()
for i in range(12):
    print(f"THIS IS NR {i}")
    print(array[i])
"""



"""
#spacy library solution
counter = 0
for i in range(len(title_list) -1):
    for j in range(0, len(title_list)):
        nlp0 = nlp(title_list[i])
        nlp1 = nlp(title_list[j])
        sim = nlp0.similarity(nlp1)
        print(f"Similarity between title_list {i} and title_list {j} is {sim}")

counter = 0
for i in range(len(article_list) -1):
    for j in range(0, len(article_list)):
        nlp0 = nlp(article_list[i])
        nlp1 = nlp(article_list[j])
        sim = nlp0.similarity(nlp1)
        print(f"Similarity between article_list {i} and article_list {j} is {sim}")
"""



"""with open("bbcTEST.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(type(row))
    if not row:
        print(row)
        continue
    if not row[0]:
        print(row)
        continue
    if not row[1]:
        print(row)
        continue
    if row[0] and row[1]:
        print(row[0])
        print(row[1])"""

