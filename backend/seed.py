import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config.database import SessionLocal, Base, engine
from app.entities.user import User
from app.entities.train import Train
from app.entities.train_class import TrainClass
from app.enums import UserRole, ClassType
from app.config.security import get_password_hash


def seed():
    print("🌱 Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Users
        admin_user = db.query(User).filter(User.email == "admin@railbook.com").first()
        if not admin_user:
            admin_user = User(
                first_name="Admin",
                last_name="RailBook",
                email="admin@railbook.com",
                password=get_password_hash("Admin@123"),
                mobile_number="9876543210",
                role=UserRole.ADMIN,
            )
            db.add(admin_user)
            print("  Created Admin user: admin@railbook.com (Password: Admin@123)")

        pattbhi_user = db.query(User).filter(User.email == "pattbhi@railbook.com").first()
        if not pattbhi_user:
            pattbhi_user = User(
                first_name="Pattbhi",
                last_name="Kumar",
                email="pattbhi@railbook.com",
                password=get_password_hash("Pattbhi@123"),
                mobile_number="9887766554",
                role=UserRole.USER,
            )
            db.add(pattbhi_user)
            print("  Created User: pattbhi@railbook.com (Password: Pattbhi@123)")

        db.commit()

        # 2. Seed Trains and Classes matching popular routes in screenshot
        train_data = [
            {
                "number": "12951",
                "name": "Mumbai Rajdhani Express",
                "source": "Mumbai",
                "destination": "Delhi",
                "dep": "17:00",
                "arr": "08:32",
                "classes": [
                    {"type": ClassType.ONE_A, "fare": 4200.00, "total": 24, "avail": 18},
                    {"type": ClassType.TWO_A, "fare": 2850.00, "total": 54, "avail": 36},
                    {"type": ClassType.THREE_A, "fare": 2050.00, "total": 72, "avail": 52},
                ]
            },
            {
                "number": "12952",
                "name": "New Delhi Rajdhani Express",
                "source": "Delhi",
                "destination": "Mumbai",
                "dep": "16:55",
                "arr": "08:35",
                "classes": [
                    {"type": ClassType.ONE_A, "fare": 4200.00, "total": 24, "avail": 14},
                    {"type": ClassType.TWO_A, "fare": 2850.00, "total": 54, "avail": 41},
                    {"type": ClassType.THREE_A, "fare": 2050.00, "total": 72, "avail": 60},
                ]
            },
            {
                "number": "12608",
                "name": "Lalbagh SF Express",
                "source": "Bangalore",
                "destination": "Chennai",
                "dep": "06:20",
                "arr": "12:15",
                "classes": [
                    {"type": ClassType.CC, "fare": 465.00, "total": 75, "avail": 62},
                    {"type": ClassType.TWO_S, "fare": 145.00, "total": 108, "avail": 85},
                    {"type": ClassType.EC, "fare": 980.00, "total": 56, "avail": 34},
                ]
            },
            {
                "number": "12702",
                "name": "Hussainsagar Express",
                "source": "Hyderabad",
                "destination": "Mumbai",
                "dep": "14:50",
                "arr": "04:55",
                "classes": [
                    {"type": ClassType.SL, "fare": 410.00, "total": 72, "avail": 45},
                    {"type": ClassType.THREE_A, "fare": 1120.00, "total": 72, "avail": 28},
                    {"type": ClassType.TWO_A, "fare": 1600.00, "total": 54, "avail": 19},
                ]
            },
            {
                "number": "12301",
                "name": "Howrah Rajdhani Express",
                "source": "Kolkata",
                "destination": "Delhi",
                "dep": "16:55",
                "arr": "10:05",
                "classes": [
                    {"type": ClassType.ONE_A, "fare": 4350.00, "total": 24, "avail": 12},
                    {"type": ClassType.TWO_A, "fare": 2980.00, "total": 54, "avail": 30},
                    {"type": ClassType.THREE_A, "fare": 2150.00, "total": 72, "avail": 48},
                ]
            },
            {
                "number": "11074",
                "name": "Chennai Pune Express",
                "source": "Chennai",
                "destination": "Pune",
                "dep": "15:55",
                "arr": "07:20",
                "classes": [
                    {"type": ClassType.SL, "fare": 490.00, "total": 72, "avail": 39},
                    {"type": ClassType.THREE_A, "fare": 1340.00, "total": 72, "avail": 25},
                    {"type": ClassType.TWO_A, "fare": 1920.00, "total": 54, "avail": 15},
                ]
            },
            {
                "number": "12015",
                "name": "Ajmer Shatabdi Express",
                "source": "Delhi",
                "destination": "Jaipur",
                "dep": "06:10",
                "arr": "10:40",
                "classes": [
                    {"type": ClassType.CC, "fare": 690.00, "total": 75, "avail": 55},
                    {"type": ClassType.EC, "fare": 1340.00, "total": 56, "avail": 40},
                ]
            },
        ]

        for t_info in train_data:
            existing_t = db.query(Train).filter(Train.train_number == t_info["number"]).first()
            if not existing_t:
                train = Train(
                    train_number=t_info["number"],
                    train_name=t_info["name"],
                    source=t_info["source"],
                    destination=t_info["destination"],
                    departure_time=t_info["dep"],
                    arrival_time=t_info["arr"],
                )
                db.add(train)
                db.flush()

                for c_info in t_info["classes"]:
                    tc = TrainClass(
                        train_id=train.id,
                        class_type=c_info["type"],
                        fare=c_info["fare"],
                        total_seats=c_info["total"],
                        available_seats=c_info["avail"],
                    )
                    db.add(tc)

                print(f"  Added train: {t_info['name']} ({t_info['number']})")

        db.commit()
        print("✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
