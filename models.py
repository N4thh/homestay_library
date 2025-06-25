from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Homestay(db.Model):
    __tablename__ = 'homestays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)
    image_urls = db.Column(db.ARRAY(db.String))
    priority = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Thêm các trường khác nếu cần

class Review:
    def __init__(self, id, homestay_id, rating, comment, created_at, username=None, user_id=None):
        self.id = id
        self.homestay_id = homestay_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.user_id = user_id
        
        # Lấy username từ database nếu có user_id
        if user_id:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                conn.close()
                self.username = user['username'] if user else ""
        else:
            self.username = username if username else ""

    @staticmethod
    def create(user_id, homestay_id, rating, comment):
        return Review(
            id=str(uuid.uuid4()),
            user_id=user_id,
            homestay_id=homestay_id,
            rating=rating,
            comment=comment,
            created_at=datetime.now().isoformat()
        )

    @staticmethod
    def calculate_average_rating(reviews):
        if not reviews:
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / len(reviews), 1)

class ReviewJSONManager:
    def __init__(self):
        self.data_file = os.path.join('data', 'reviews.json')
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def read_reviews(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading reviews: {e}")
            return []

    def write_reviews(self, reviews):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(reviews, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error writing reviews: {e}")
            return False

    def add_review(self, review):
        reviews = self.read_reviews()
        # Kiểm tra xem user đã review homestay này chưa (kiểm tra theo user_id nếu có)
        if review.user_id:
            existing_review = next((r for r in reviews if r['user_id'] == review.user_id and str(r['homestay_id']) == str(review.homestay_id)), None)
            if existing_review:
                return False, "Bạn đã đánh giá homestay này rồi"
        
        reviews.append(review.__dict__)
        return self.write_reviews(reviews)

    def get_reviews_by_homestay(self, homestay_id):
        reviews = self.read_reviews()
        return [Review(**review) for review in reviews if str(review['homestay_id']) == str(homestay_id)]

    def get_average_rating(self, homestay_id):
        reviews = self.get_reviews_by_homestay(homestay_id)
        if not reviews:
            return 0
        return sum(r.rating for r in reviews) / len(reviews)