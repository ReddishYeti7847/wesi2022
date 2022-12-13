from flask import Flask, render_template
#from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
import numpy as np

app = Flask(__name__)

#app.config['SECRET_KEY'] = os.urandom(24)   #秘密鍵
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Root.123@localhost/scheme"

db = SQLAlchemy(app)
#bootstrap = Bootstrap(app)

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
    region_survey_count = Survey.query.filter_by().join(Area, Area.id == Survey.area_id).join(Region, Region.id == Area.region_id).group_by(Region.name, Survey.id).count()
    area_survey_count   = Survey.query.filter_by(area_id=id).group_by().count()
    #survey_count    = Survey.query.filter_by(area_id=id).group_by(Survey.area_id).count()
    return render_template("index.html", title = "WESI2022", regions = regions, areas = areas, region_survey_count = region_survey_count, survey_count = area_survey_count)
    
@app.route("/surveys/index/<int:id>")
def surveys_index(id):
    surveys = Survey.query.all()
    area    = Area.query.filter_by(id=id).first()
    
    #survey_count = Region.query.filter_by(Area.area_id=id).count().sum()
    #survey_count = Survey.query.filter_by(area_id=id).group_by().count()
    
    #subq = db.session.query(Area.id).filter(Area.id == id).group_by(Survey.area_id).join(Survey, Area.id == Survey.area_id)
    #survey_count = db.session.query(subq, func.count(Survey.area_id).label("count")).first()
    
    region_count = None
    area_count = db.session.query(Area.id, func.count(Survey.area_id).label("count")).filter(Area.id == id).group_by(Survey.area_id).join(Survey, Area.id == Survey.area_id).first()    #AreaテーブルのidとSurveyテーブルのarea_idの個数を数える
    #site_count = Site.query.filter_by().group_by().count()
    survey_count = db.session.query(Survey.id, func.count(Site.survey_id).label("count")).filter().group_by(Site.survey_id).join(Site, Survey.id == Site.survey_id).all()
    
    return render_template("survey_index.html", title = "WESI2022", surveys = surveys, area = area, region_count = region_count, area_count = area_count, survey_count = survey_count)

@app.route("/sites/index/<int:id>")
def sites_index(id):
    sites   = Site.query.all()
    return render_template("site_index.html", title = "WESI2022", sites = sites)

#CSVを利用してデータを入力する
@app.route("/csv_import")
def csv_import():
    #データベースをリセットする
    deletes = Survey.query.all()
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


if __name__ == "__main__":
    app.run(debug=True, port = 8080)