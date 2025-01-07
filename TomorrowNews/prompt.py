from TomorrowNews.graph import news_graph

def gettomorrownews():
    for event in news_graph.stream({"messages": [("system", "Using today’s actual newspaper as a foundation, \
                                                  apply reasoning and analysis to predict future events. \
                                                  Create the next day’s edition of 'Tomorrow News,' \
                                                  complete with imaginative yet plausible headlines and stories. \
                                                  Avoid simply continuing or expanding on today’s news—instead, \
                                                  focus on predicting the next events or surprising developments \
                                                  that could arise as consequences of current happenings or emerge unexpectedly. \
                                                  Make it feel like a genuine glimpse into the future!\
                                                  after finishing this step, create an HTML newspaper style page with different sections\
                                                  for every news, the two columns at right and left sides, and a wide main column in the midle, \
                                                  and arrange it in a professional way with good font and sizes like a real paper.\
                                                  convert the created news to a title and the column, for the main headline,\
                                                  use image tool and create a photo or image and use the result url in your HTML,\
                                                  then create the final result that is the newspaper pure HTML without anything extra,\
                                                  your response will be parsed directly in a browser, so should be rendered correctly as an HTML")]}):
        print("event: ", event)
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
    
    return value["messages"][-1].content
    #return "no answer"