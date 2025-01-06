from TomorrowNews.graph import news_graph

def gettomorrownews():
    for event in news_graph.stream({"messages": [("system", "Using today’s actual newspaper as a foundation, \
                                                  apply reasoning and analysis to predict future events. \
                                                  Create the next day’s edition of 'Tomorrow News,' \
                                                  complete with imaginative yet plausible headlines and stories. \
                                                  Avoid simply continuing or expanding on today’s news—instead, \
                                                  focus on predicting the next events or surprising developments \
                                                  that could arise as consequences of current happenings or emerge unexpectedly. \
                                                  Make it feel like a genuine glimpse into the future!")]}):
        print("event: ", event)
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
    
    return value["messages"][-1].content
    #return "no answer"