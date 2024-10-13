from flask import Flask,request,jsonify

from sqlalchemy.orm import sessionmaker
from bd import engine,Users,Announcement,create_tables

Session = sessionmaker(bind=engine)
session = Session()

app = Flask("app")

@app.route("/api/v1/announcements/<int:id>/",methods=["GET"])
def get_all(id):
    announcements = session.query(Announcement).join(Users).filter(Announcement.id == id).first()
    if announcements:
        return jsonify(announcements.dict)
    else:
        return "Error"

@app.route("/api/v1/users/",methods=["POST"])
def post_new_u():
    new_user = request.json
    user = Users(**new_user)
    session.add(user)
    session.commit()
    session.close() 
    return jsonify(new_user)

@app.route("/api/v1/announcements/",methods=["POST"])
def post_new():
    new_announcement = request.json
    user = Announcement(**new_announcement)
    session.add(user)
    session.commit()
    session.close() 
    return jsonify(new_announcement)

@app.route("/api/v1/announcements/<int:id>/",methods=["DELETE"])
def del_one(id):
    for_del = session.query(Announcement).filter(Announcement.id == id).delete()
    session.commit()
    session.close() 
    return "Delete"


# app.add_url_rule()

if __name__ == "__main__":
    create_tables(engine)
    app.run(debug=True)