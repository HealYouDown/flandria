from app.home.blueprint import home_bp
from app.models import ItemList, Monster, Quest
from app.constants import DATABASE_TABLENAMES

@home_bp.route("/sitemap.txt")
def sitemap():
    urls = [
        "https://www.flandria.info",
        "https://www.flandria.info/database",
        "https://www.flandria.info/auth/login",
        "https://www.flandria.info/auth/register",
        "https://www.flandria.info/planner/mercenary",
        "https://www.flandria.info/planner/saint",
        "https://www.flandria.info/planner/noble",
        "https://www.flandria.info/planner/explorer",
        "https://www.flandria.info/planner/ship",
        "https://www.flandria.info/about",
        "https://www.flandria.info/privacy",
    ]

    for tablename in DATABASE_TABLENAMES:
        urls.append("https://www.flandria.info/database/{tablename}".format(tablename=tablename))
    
    for monster in Monster.query.all():
        urls.append("https://www.flandria.info/database/monster/{code}".format(code=monster.code))

    for quest in Quest.query.all():
        urls.append("https://www.flandria.info/database/quest/{code}".format(code=quest.code))

    for item in ItemList.query.all():
        urls.append("https://www.flandria.info/database/{table}/{code}".format(table=item.table, code=item.code))

    result = "\n".join(urls)

    return result
