
db = db.getSiblingDB("my_project"); // 데이터베이스 선택

// 고유 인덱스 생성
db.comments.createIndex({ commentUid: 1 }, { unique: true });
db.episodes.createIndex({ productId: 1 }, { unique: true });

print("Indexes created successfully!");
