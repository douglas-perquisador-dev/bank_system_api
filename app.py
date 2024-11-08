import routes
from config import app, db
# import models for migrations
from models import accounts, users, transactions


# Cria as tabelas no banco de dados caso ainda não existam
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)
