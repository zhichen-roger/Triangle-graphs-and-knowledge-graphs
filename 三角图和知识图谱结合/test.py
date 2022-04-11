#
# from py2neo import Graph, Node, Relationship,NodeMatcher
# graph = Graph("http://localhost:7474", username="neo4j", password='admin')
# matcher = NodeMatcher(graph)
# stone = matcher.match('Stone').where("_.name='Sandstone'").first()
# print(stone)
# graph.run("Neo4j Cypher Query Language")

# 第二种方式
import webbrowser
from create_echarts_Stand import CreateEcharts

searcher = CreateEcharts()
# searcher.create_stone("Quartz wackes", "templates//echarts//render1" + ".html")
# chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
# webbrowser.get('chrome').open('http://localhost:63342/untitled1/demo%200.1.2/templates/echarts/render1.html?_ijt=l3g81qhg9nb3iuea6ffngnsn7r',new=0,autoraise=True)
list = searcher.stone_classfion("Litho-feldspathic sandstone")
print("***************************")
for i in range(len(list)):
    if(list[i]=="Garzanti"):
        print("Garzanti A")
    elif(list[i]=="Folk"):
        print("Folk B")
    elif(list[i]=='Pettijohn'):
        print("Pettijohn C")


