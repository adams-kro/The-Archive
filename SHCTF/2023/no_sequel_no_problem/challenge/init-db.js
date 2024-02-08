db = db.getSiblingDB("users_db");
db.user_tb.drop();

db.user_tb.insertMany([
    {
        "id": 1,
        "username": "admin",
        "password": "flag{34sy_P34sy_Bl1nd_1nject10n}"
    },
    {
        "id": 2,
        "username": "tukmogi",
        "password": "tukmogi",
    }
]);
