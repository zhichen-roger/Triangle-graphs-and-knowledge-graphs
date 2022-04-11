#-*-coding:utf-8-*-
from py2neo import Graph
from pyecharts import options as opts
from pyecharts.charts import Graph as gr
from QAKG.tool.jscode import JsCode

class CreateEcharts:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "admin"))
        self.num_limit = 50

    # 石头的分类
    def stone_classfion(self, keyname):
        entities = []
        entities.append(keyname)
        sqls = []
        # 石头的名称
        sql = ["MATCH (m:classfion) where m.name = '{0}' return m.name".format(i) for i in entities]
        sqls.append(sql)
        # 石头Garzanti's classification分类
        sql = [
            "MATCH (m:Stone)-[r:Garzanti_classification]->(n:classfion) where n.name = '{0}' return m.name, r.classfion,r.rule,r.references,n.name".format(
                i) for i in entities]
        sqls.append(sql)
        # 石头Pettijohn_classification分类
        sql = [
            "MATCH (p:Stone)-[q:Pettijohn_classification]->(m:StandStone)-[r:Pettijohn_classification]->(n:classfion) where n.name = '{0}' return m.name, r.classfion,r.rule,r.references,n.name,p.name,q.classfion,q.rule".format(
                i) for i in entities]
        sqls.append(sql)
        # 石头Folk_classification分类
        sql = [
            "MATCH (m:Stone)-[r:Folk_classification]->(n:classfion) where n.name = '{0}' return m.name, r.classfion,r.rule,r.references,n.name".format(
                i) for i in entities]
        sqls.append(sql)
        answers = []
        classfion = []
        for s in sqls:
            ress = self.g.run(s[0]).data()
            print(ress)
            print("外层")
            if len(ress) == 0 or '' in ress[0].values():  # 没查到
                continue
            for r in ress:
                print(r)
                print(len(list(r.keys())))
                print("内层")
                if (len(list(r.keys())) == 1):
                    # answers.append([list(r.keys())[0].split('.')[1],r[list(r.keys())[0]]])
                    pass
                else:  # 代表石头分类
                    if r['r.classfion'] == "Garzanti's classification":
                        answers.append(["Garzanti_classification", r['r.classfion']])
                        answers.append(["Garzanti_rule", r['r.rule']])
                        answers.append(["Garzanti_references", r['r.references']])
                        answers.append(["Garzanti_upname", r['m.name']])
                        classfion.append("Garzanti")
                    elif (r['r.classfion'] == "Folk's classification"):
                        answers.append(["Folk_classification", r['r.classfion']])
                        answers.append(["Folk_rule", r['r.rule']])
                        answers.append(["Folk_references", r['r.references']])
                        answers.append(["Folk_upname", r['m.name']])
                        classfion.append("Folk")
                    elif (r['r.classfion'] == "Pettijohn's classification"):
                        answers.append(["Pettijohn_classification", r['r.classfion']])
                        answers.append(["Pettijohn_rule", r['r.rule']])
                        answers.append(["Pettijohn_references", r['r.references']])
                        answers.append(["Pettijohn_upname", r['m.name']])
                        classfion.append("Pettijohn")

        # answers结果list
        for i in range(len(answers)):
            print(answers[i])
            print("这里***")

        # classfion结果list
        # for i in range(len(classfion)):
        #     print(classfion[i])
        return classfion

    # 石头的关系图
    def create_stone(self,keyname,url):
        entities = []
        entities.append(keyname)
        sqls = []
        # 石头的名称
        sql = ["MATCH (m:classfion) where m.name = '{0}' return m.name".format(i) for i in entities]
        sqls.append(sql)
        # 石头Garzanti's classification分类
        sql = ["MATCH (m:Stone)-[r:Garzanti_classification]->(n:classfion) where n.name = '{0}' return m.name, r.classfion,r.rule,r.references,n.name".format(i)for i in entities]
        sqls.append(sql)
        # 石头Pettijohn_classification分类
        sql = ["MATCH (p:Stone)-[q:Pettijohn_classification]->(m:StandStone)-[r:Pettijohn_classification]->(n:classfion) where n.name = '{0}' return m.name, r.classfion,r.rule,r.references,n.name,p.name,q.classfion,q.rule".format(i) for i in entities]
        sqls.append(sql)
        # 石头Folk_classification分类
        sql = ["MATCH (m:Stone)-[r:Folk_classification]->(n:classfion) where n.name = '{0}' return m.name, r.classfion,r.rule,r.references,n.name".format(i)for i in entities]
        sqls.append(sql)
        answers = []
        # classfion = []
        for s in sqls:
            ress = self.g.run(s[0]).data()
            print(ress)
            print("外层")
            if len(ress) == 0 or '' in ress[0].values():  # 没查到
                continue
            for r in ress:
                print(r)
                print(len(list(r.keys())))
                print("内层")
                if (len(list(r.keys())) == 1):
                    #answers.append([list(r.keys())[0].split('.')[1],r[list(r.keys())[0]]])
                    pass
                else:  # 代表石头分类
                    if r['r.classfion'] == "Garzanti's classification":
                        answers.append(["Garzanti_classification", r['r.classfion']])
                        answers.append(["Garzanti_rule", r['r.rule']])
                        answers.append(["Garzanti_references", r['r.references']])
                        answers.append(["Garzanti_upname", r['m.name']])
                        # classfion.append("Garzanti")
                    elif(r['r.classfion'] == "Folk's classification"):
                        answers.append(["Folk_classification", r['r.classfion']])
                        answers.append(["Folk_rule", r['r.rule']])
                        answers.append(["Folk_references", r['r.references']])
                        answers.append(["Folk_upname", r['m.name']])
                        # classfion.append("Folk")
                    elif(r['r.classfion'] == "Pettijohn's classification"):
                        answers.append(["Pettijohn_classification", r['r.classfion']])
                        answers.append(["Pettijohn_rule", r['r.rule']])
                        answers.append(["Pettijohn_references", r['r.references']])
                        answers.append(["Pettijohn_upname", r['m.name']])
                        # classfion.append("Pettijohn")


        # answers结果list
        for i in range(len(answers)):
            print(answers[i])
            print("这里***")

        # classfion结果list
        # for i in range(len(classfion)):
        #     print(classfion[i])

        # 统计category类别
        types = set()
        types.add("Standstone")
        relation_types = set()
        for i in range(len(answers)):
            relation_types.add(answers[i][0])
        print(relation_types)
        print("__________")
        for i in range(len(answers)):
                types.add(answers[i][0])
        categories = []  # 存储与center_name有关系的数据的类型
        categories.append({})
        for x in types:
            categories.append({'name': x})
        print(categories)
        print("那里")

        # 创建nodes
        nodes = []
        nodes.append({"name": entities[0] + "|Standstone", "des": entities[0],
                      "category": categories.index({'name': "Standstone"}), "symbolSize": 90})
        for x in relation_types:
            nodes.append({"name": x + "|centernode", "des": "", "symbolSize": 30})

        for i in range(len(answers)):
            cate=answers[i][0]
            node = {"name": answers[i][1]+"|"+cate ,
                    "des": answers[i][1],
                    "category": categories.index({'name': cate}), "symbolSize": 70}
            if node not in nodes:
                nodes.append(node)

        for n in nodes:
            print(n)  # nodes创建完成
        print("nodes这里")

        # 创建关系
        links = []
        for x in relation_types:
            links.append({"source": entities[0] + "|Standstone", "target": x + "|centernode",
                          "name": x})

        for i in range(len(answers)):
            cate = answers[i][0]
            links.append({"source": answers[i][0] + "|centernode", "target": answers[i][1] + "|" + cate,
                          "name": " "})
        # 建图
        c = (
            gr(init_opts=opts.InitOpts(width="100%", height="700px"))
                .add("", nodes, links, categories=categories,
                     repulsion=2500, label_opts=opts.LabelOpts(position="inside", formatter=JsCode(
                    """function (x) { var strs = x.data.name;   var n='';    var str='centernode';   if(strs.search(str)!=-1) {return  n;}   var strs = x.data.name.split('|')[0];  if(strs.length<=6){                       return strs;                   }else {                       name = strs.slice(0,6) + '...';                        return name;                   }}""").js_code),
                     tooltip_opts=opts.TooltipOpts(formatter=JsCode(
                         """function (x) { if(x.dataType === 'edge'){return x.data.name;} var strs = x.data.des;  var str = ''; for(var i = 0, s; s = strs[i++];) { if(i==500){str+='...'; break;} str += s; if(!(i % 50)) str += '<br>'; } return str;}""").js_code),
                     edge_label=opts.LabelOpts(position="",
                                               formatter=JsCode("""function (x) {return x.data.name;}""").js_code),
                     edge_symbol=['circle', 'arrow'], edge_symbol_size=[4, 10], is_focusnode="true"
                     )
                .set_global_opts(title_opts=opts.TitleOpts(title=entities[0] + "相关知识图谱"))

        )
        c.render(url)




if __name__ == '__main__':
    searcher = CreateEcharts()
    searcher.stone_classfion("Litho-feldspathic sandstone")
    searcher.create_stone("Litho-feldspathic sandstone","templates//echarts//render1"+".html")
    #searcher.create_stone("Quartz wackes", "templates//echarts//render1" + ".html")