from config import app, db
import views

# Cria as tabelas no banco de dados caso ainda não existam
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)
