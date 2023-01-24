from flask import Flask, render_template
#from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#from flask_googlemaps import GoogleMaps
#from flask_googlemaps import Map
from sqlalchemy import func
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

#app.config['SECRET_KEY'] = os.urandom(24)   #秘密鍵
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Root.123@localhost/scheme"
map_key = "AIzaSyAy8HaejG8a1961OtEyy4FKJ_OF0XhIof8"     #githubに登録するときはキーを消す


db = SQLAlchemy(app)
#bootstrap = Bootstrap(app)
#GoogleMaps(app)

#GoogleMaps(app, key="AIzaSyAy8HaejG8a1961OtEyy4FKJ_OF0XhIof8")

#データベースモデル定義
class Region(db.Model):
    __tablename__="region"
    id          = db.Column(db.INT, primary_key=True, autoincrement=True)
    name        = db.Column(db.VARCHAR(16))
    name_kana   = db.Column(db.VARCHAR(32))
    name_roman  = db.Column(db.VARCHAR(64))
    ord         = db.Column(db.INT)

    area = db.relationship("Area", backref = db.backref("region"), lazy = True)

class Area(db.Model):
    __tablename__="area"
    id          = db.Column(db.INT, primary_key=True, autoincrement=True)
    region_id   = db.Column(db.INT, db.ForeignKey("region.id"))
    name        = db.Column(db.VARCHAR(16))
    name_kana   = db.Column(db.VARCHAR(32))
    name_roman  = db.Column(db.VARCHAR(64))
    ord         = db.Column(db.INT)
    latitude    = db.Column(db.FLOAT)
    longitude   = db.Column(db.FLOAT)
    
    survey = db.relationship("Survey", backref = db.backref("area"), lazy = True)
    
class Survey(db.Model):
    __tablename__="survey"
    id                  = db.Column(db.INT, primary_key=True, autoincrement=True)
    area_id	            = db.Column(db.INT, db.ForeignKey("area.id"))
    name                = db.Column(db.TEXT)
    surveyor            = db.Column(db.TEXT)
    director_name       = db.Column(db.TEXT)
    director_address    = db.Column(db.TEXT)
    note                = db.Column(db.TEXT)

    site = db.relationship("Site", backref = db.backref("survey"), lazy = True)
    
class Site(db.Model):
    __tablename__="site"
    id          = db.Column(db.INT, primary_key=True, autoincrement=True)
    survey_id   = db.Column(db.INT, db.ForeignKey("survey.id"))
    name        = db.Column(db.TEXT)
    latitude    = db.Column(db.FLOAT)
    longitude   = db.Column(db.FLOAT)
    date        = db.Column(db.DATE)
    value00     = db.Column(db.FLOAT)
    value01     = db.Column(db.FLOAT)
    value02     = db.Column(db.FLOAT)
    value03     = db.Column(db.FLOAT)
    value04     = db.Column(db.FLOAT)
    value10     = db.Column(db.FLOAT)
    value11     = db.Column(db.FLOAT)
    value12     = db.Column(db.FLOAT)
    value20     = db.Column(db.FLOAT)
    value21     = db.Column(db.FLOAT)
    value22     = db.Column(db.FLOAT)
    value23     = db.Column(db.FLOAT)
    value30     = db.Column(db.FLOAT)
    value31     = db.Column(db.FLOAT)
    value32     = db.Column(db.FLOAT)
    value40     = db.Column(db.FLOAT)
    value41     = db.Column(db.FLOAT)
    value42     = db.Column(db.FLOAT)
    value43     = db.Column(db.FLOAT)
    value44     = db.Column(db.FLOAT)
    value50     = db.Column(db.FLOAT)
    value51     = db.Column(db.FLOAT)
    value52     = db.Column(db.FLOAT)
    value53     = db.Column(db.FLOAT)
    value54     = db.Column(db.FLOAT)
    note        = db.Column(db.TEXT)
    
#メイン
@app.route("/")
def index():
    regions         = Region.query.all()
    areas           = Area.query.all()
    #region_survey_count = Survey.query.filter_by().join(Area, Area.id == Survey.area_id).join(Region, Region.id == Area.region_id).group_by(Region.name, Survey.id).count()
    #area_survey_count   = Survey.query.filter_by(area_id=id).group_by().count()
    #survey_count    = Survey.query.filter_by(area_id=id).group_by(Survey.area_id).count()
    
    #カウント
    area_counts = [0] * 49
    region_counts = [0] * 8
    
    for region_id in regions:
        area_region_ids = Area.query.filter_by(region_id=region_id.id).all()
        
        for area_region_id in area_region_ids: 
            survey_count = Survey.query.filter_by(area_id=area_region_id.id).count()

            region_counts[region_id.id] = region_counts[region_id.id] + survey_count
            area_counts[area_region_id.id] = survey_count
    
    return render_template("index.html", title = "WESI2022", regions = regions, areas = areas, region_counts = region_counts, area_counts = area_counts)
    
@app.route("/surveys/index/<int:id>")
def surveys_index(id):
    surveys = Survey.query.filter_by(area_id=id).all()
    area    = Area.query.filter_by(id=id).first()
    
    #survey_count = Region.query.filter_by(Area.area_id=id).count().sum()
    #survey_count = Survey.query.filter_by(area_id=id).group_by().count()
    
    #subq = db.session.query(Area.id).filter(Area.id == id).group_by(Survey.area_id).join(Survey, Area.id == Survey.area_id)
    #survey_count = db.session.query(subq, func.count(Survey.area_id).label("count")).first()
    
    #region_count = None
    area_count = db.session.query(Area.id, func.count(Survey.area_id).label("count")).filter(Area.id == id).group_by(Survey.area_id).join(Survey, Area.id == Survey.area_id).first()    #AreaテーブルのidとSurveyテーブルのarea_idの個数を数える
    #site_count = Site.query.filter_by().group_by().count()
    survey_count = db.session.query(Survey.id, func.count(Site.survey_id).label("count")).filter().group_by(Site.survey_id).join(Site, Survey.id == Site.survey_id).all()
    
    #カウント
    test = []
    region_counts = 0
    site_counts = []

    sites_date_max = []
    sites_date_min = []

    #調査のカウント（地方）
    region_id = area.region_id
    area_region_ids = Area.query.filter_by(region_id=area.region_id).all()
    for area_region_id in area_region_ids:
        test.append(area_region_id.id)
        
        #db.session.query(func.count(Survey.id).label("count")).filter(Survey.area_id == region_id.id).first()#.group_by(Survey.area_id).join(Survey, Area.id == Survey.area_id).first()
        
        region_count = Survey.query.filter_by(area_id=area_region_id.id).count()#.label("count")
        region_counts = region_counts + region_count
    
    #地点のカウント（調査）と調査日/期間
    j = 0
    survey_area_ids = Survey.query.filter_by(area_id=id).all()
    for survey_area_id in survey_area_ids:
        site_count = Site.query.filter_by(survey_id=survey_area_id.id).count()
        site_counts.append(site_count)
        
        sites_date = Site.query.filter_by(survey_id=survey_area_id.id)
        site_date_max = db.session.query(func.max(Site.date)).filter(Site.survey_id == survey_area_id.id).first()
        site_date_min = db.session.query(func.min(Site.date)).filter(Site.survey_id == survey_area_id.id).first()
        sites_date_max.append(site_date_max)
        sites_date_min.append(site_date_min)
        
        #i = 0
        #for site_date in sites_date:
            #now_date = site_date.date
            #if i < 1:
                #sites_date_max.append(site_date.date)
                #sites_date_min.append(site_date.date)
            #elif sites_date_max[j] < site_date.date:
                #sites_date_max[j] = site_date
            #elif sites_date_min[j] > site_date.date:
                #sites_date_min[j] = site_date
                
            #i = i + 1
        
        #j = j + 1
        #site_date_min = db.session.query(func.min(Site.date)).filter(Site.survey_id == survey_area_id.id).first()
        
        #sites_date_max.append(site_date_max.date)
        #sites_date_min.append(site_date_min)
    
    #map
    #地点の座標　←　各地点の座標の平均、　地点は複数、　同じ県である必要性
    surveys_map = Survey.query.filter_by(area_id = id).all()
    #sites = Site.query.filter(Site.Survey.area_id == id).all()
    
    lat = 0
    lats = []
    lng = 0
    lngs = []
    count = 0
    counts = 0
    
    i = 0
    for survey_map in surveys_map:
        sites_map = Site.query.filter_by(survey_id = survey_map.id).all()
        lats.append([])
        lngs.append([])
        counts = counts + 1
        
        for site_map in sites_map:  #ここで各siteの座標の平均を求めておきたい
            lat = lat + site_map.latitude
            lng = lng + site_map.longitude
            count = count + 1

            #lats[i].append(site_map.latitude)
            #lngs[i].append(site_map.longitude)
        
        lats[i] = lat / count
        lngs[i] = lng / count
        i = i + 1
    
    test = [lats, lngs]
    
    #return test
    
    return render_template("survey_index.html", map_key = map_key, title = "WESI2022", surveys = surveys, area = area, region_count = region_count, area_count = area_count, region_counts = region_counts, site_counts = site_counts, sites_date_max = sites_date_max, sites_date_min = sites_date_min, lats = lats, lngs = lngs, counts = counts)

@app.route("/sites/index/<int:id>")
def sites_index(id):
    survey  = Survey.query.filter_by(id=id).first()
    sites   = Site.query.all()
    return render_template("site_index.html", map_key = map_key, title = "WESI2022", survey = survey, sites = sites)

@app.route("/sites/show/<int:id>")
def sites_show(id):
    itemLabels = ["総合平均", "自然な姿", "ゆたかな生き物", "水のきれいさ", "快適な水辺", "地域とのつながり"]
    subItemLabels = [
        ["自然なすがた", "ゆたかな生き物", "水のきれいさ", "快適な水辺", "地域とのつながり"],
        ["水の流れはゆたかですか", "岸のようすは自然らしいですか" ,"魚が川をさかのぼれるだろうか"],
        ["河原と水辺に植物がはえていますか", "鳥はいますか", "魚がいますか", "川底に生き物がいますか"],
        ["水は透明ですか？", "水はくさくないですか", "水はきれいですか"],
        ["川やまわりのけしきは美しいですか", "ごみが目につきますか", "水にふれてみたいですか", "どんなにおいを感じますか", "どんな音が聞こえますか"],
        ["川にまつわる話を聞いたことがありますか", "水辺に近づきやすいですか", "多くの人が利用していますか", "産業などの活動", "環境の活動"]
    ]
    
    s = [
        ["value00", "value01", "value02", "value03", "value04"],
        ["value10", "value11", "value12"],
        ["value20", "value21", "value22", "value23"],
        ["value30", "value31", "value32"],
        ["value40", "value41", "value42", "value43", "value44"],
        ["value50", "value51", "value52", "value53", "value54"],
    ]

    subItemVals = [
        [0, 0, 0, 0, 0],
        [0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    
    site   = Site.query.filter_by(id=id).first()
    
    subItemVals[0][0] = site.value00
    subItemVals[0][1] = site.value01
    subItemVals[0][2] = site.value02
    subItemVals[0][3] = site.value03
    subItemVals[0][4] = site.value04
    subItemVals[1][0] = site.value10
    subItemVals[1][1] = site.value11
    subItemVals[1][2] = site.value12
    subItemVals[2][0] = site.value20
    subItemVals[2][1] = site.value21
    subItemVals[2][2] = site.value22
    subItemVals[2][3] = site.value23
    subItemVals[3][0] = site.value30
    subItemVals[3][1] = site.value31
    subItemVals[3][2] = site.value32
    subItemVals[4][0] = site.value40
    subItemVals[4][1] = site.value41
    subItemVals[4][2] = site.value42
    subItemVals[4][3] = site.value43
    subItemVals[4][4] = site.value44
    subItemVals[5][0] = site.value50
    subItemVals[5][1] = site.value51
    subItemVals[5][2] = site.value52
    subItemVals[5][3] = site.value53
    subItemVals[5][4] = site.value54
    
    site_c = {
        "chart_labels":"仮項目1, 仮項目2, 仮項目3, 仮項目4", 
        "chart_data":"2, 3, 5, 1",
        "chart_title":"仮タイトル",
        "chart_target":"仮ターゲット",
    }
    
    #5, (3, 4, 3, 5, 5)
#    labels = [
#        ["", "", "", "", ""],
#        ["", "", ""],
#        ["", "", "", ""],
#        ["", "", ""],
#        ["", "", "", "", ""],
#        ["", "", "", "", ""]
#    ]
    
    #レーダーチャートのデータ
    site_chart_json = []
    site_chart = [{}, {}, {}, {}, {}, {}]

    for i in range(len(subItemLabels)):
        labels = ["", "", "", "", ""]
        vals = [0, 0, 0, 0, 0]
        
        label = ""
        val = ""
        
        site_chart_json.append({})
        
        for j in range(len(subItemLabels[i])):
            if j > 0:
                label = label + ", "
                val = val + ", "
            
            label = label + str(subItemLabels[i][j])
            val = val + str(subItemVals[i][j])
        
        site_chart_json[i]["chart_labels"] = label
        site_chart_json[i]["chart_data"] = val
        #site_chart_json[i] = json.dumps(site_chart_json[i], ensure_ascii=False)
        
        site_chart[i] = site_chart_json[i]

    
    #return site_chart_json   #これをコメントアウトするとjsonのデータだけを確認できる
    #return str(type(site_chart_json[1]))   #これをコメントアウトするとjsonのデータだけを確認できる
    
    return render_template("site_show.html", map_key = map_key, title = "WESI2022", itemLabels = itemLabels, subItemLabels = subItemLabels, subItemVals = subItemVals, site = site, site_chart = site_chart)
    
@app.route("/help")
def help():
    return render_template("help.html", title = "WESI2022")

#CSVを利用してデータを入力する
@app.route("/csv_import")
def csv_import():
    #データベースをリセットする
    deletes = Site.query.all()
    for delete in deletes:
        db.session.delete(delete)
        db.session.commit()
    deletes = Survey.query.all()
    for delete in deletes:
        db.session.delete(delete)
        db.session.commit()
    deletes = Area.query.all()
    for delete in deletes:
        db.session.delete(delete)
        db.session.commit()
    deletes = Region.query.all()
    for delete in deletes:
        db.session.delete(delete)
        db.session.commit()

    testname = " "

    #region
    df = pd.read_csv("wesi2022/seeds/regions.csv")
    df = df.replace({np.nan: None})

    for i in range(len(df)):
        region = Region()
        region.id           = i + 1
        region.name         = df.loc[i]["name"]
        region.name_kana    = df.loc[i]["name_kana"]
        region.name_roman   = df.loc[i]["name_roman"]
        region.ord        = df.loc[i]["order"]
        db.session.add(region)
        testname = testname + region.name
        db.session.commit()

    #area
    df = pd.read_csv("wesi2022/seeds/areas.csv")
    df = df.replace({np.nan: None})

    for i in range(len(df)):
        area = Area()
        area.id             = i + 1
        area.region_id      = df.loc[i]["region_id"]
        area.name           = df.loc[i]["name"]
        area.name_kana      = df.loc[i]["name_kana"]
        area.name_roman     = df.loc[i]["name_roman"]
        area.ord            = df.loc[i]["order"]
        area.latitude       = df.loc[i]["latitude"]
        area.longitude      = df.loc[i]["longitude"]
        db.session.add(area)
        testname = testname + area.name
        db.session.commit()
    
    #survey
    df = pd.read_csv("wesi2022/seeds/surveys.csv")
    df = df.replace({np.nan: None})

    for i in range(len(df)):
        survey = Survey()
        survey.id               = df.loc[i]["id"]
        survey.area_id          = df.loc[i]["area_id"]
        survey.name             = df.loc[i]["name"]
        survey.surveyor         = df.loc[i]["surveyor"]
        survey.director_name    = df.loc[i]["director_name"]
        survey.director_address = df.loc[i]["director_address"]
        survey.note             = df.loc[i]["note"]
        db.session.add(survey)
        testname = testname + survey.name
        db.session.commit()
    
    #site
    df = pd.read_csv("wesi2022/seeds/sites_test.csv")
    df = df.replace({np.nan: None})
    # testname = testname + str(len(df))#survey.name
    
    for i in range(len(df)):
        site = Site()
        id          = i + 1
        site.survey_id   = df.loc[i]["survey_id"]
        site.name        = df.loc[i]["name"]
        site.date        = df.loc[i]["date"]
        site.latitude    = df.loc[i]["latitude"]
        site.longitude   = df.loc[i]["longitude"]
        site.date        = df.loc[i]["date"]
        site.value00     = df.loc[i]["value00"]
        site.value01     = df.loc[i]["value01"]
        site.value02     = df.loc[i]["value02"]
        site.value03     = df.loc[i]["value03"]
        site.value04     = df.loc[i]["value04"]
        site.value10     = df.loc[i]["value10"]
        site.value11     = df.loc[i]["value11"]
        site.value12     = df.loc[i]["value12"]
        site.value20     = df.loc[i]["value20"]
        site.value21     = df.loc[i]["value21"]
        site.value22     = df.loc[i]["value22"]
        site.value23     = df.loc[i]["value23"]
        site.value30     = df.loc[i]["value30"]
        site.value31     = df.loc[i]["value31"]
        site.value32     = df.loc[i]["value32"]
        site.value40     = df.loc[i]["value40"]
        site.value41     = df.loc[i]["value41"]
        site.value42     = df.loc[i]["value42"]
        site.value43     = df.loc[i]["value43"]
        site.value44     = df.loc[i]["value44"]
        site.value50     = df.loc[i]["value50"]
        site.value51     = df.loc[i]["value51"]
        site.value52     = df.loc[i]["value52"]
        site.value53     = df.loc[i]["value53"]
        site.value54     = df.loc[i]["value54"]
        site.note        = df.loc[i]["note"]
        db.session.add(site)
        testname = testname + survey.name
        db.session.commit()

    return testname

@app.route("/test")
def test():
    #regions         = Region.query.all()
    
    #region_survey_count = Survey.query.filter_by().join(Area, Area.id == Survey.area_id).join(Region, Region.id == Area.region_id).group_by(Region.id, Area.id).count()
    #survey_count = Survey.query.select(Survey.area_id).group_by(Survey.area_id).having(Survey.area_id == 1).count()
    #survey_count = db.engine.execute("SELECT COUNT(*) FROM survey INNER JOIN area ON survey.area_id = area.id WHERE area.id = 4;")
    #survey_count = db.engine.execute("SELECT COUNT(*) FROM survey;")

    return render_template("var_test.html", title = "WESI2022")#, regions = regions, region_survey_count = survey_count)

@app.route("/json_test")
def json_test():
    
    j = [
        {
            "項目":"A, B, C",
            "数値":[2, 3, 5]
        },
        {
            "項目":"D, E",
            "数値":"1, 4"
        }
    ]
    js = json.dumps(j)
    
    vj = []
    vj.append({})
    vj[0]["str"] = "S"
    vj[0]["sta"] = "A"
    vj.append({})
    vj[1]["str"] = "S"


    return vj
    #return j[0]["数値"][2]
    
    
    #return render_template("json_test.html", js = js)

@app.route("/map_test")
def map_test():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ],
        styles="height:300px;width:300px;margin:0;"
    )
    return render_template('map_test.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
    app.run(debug=True, port = 8080)