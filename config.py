from dotenv import load_dotenv
import os
from app import app

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQL_ALCHEMY_TRICK_MODIFICATIONS'] = os.getenv('SQL_ALCHEMY_TRICK_MODIFICATIONS')