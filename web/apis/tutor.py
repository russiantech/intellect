

def small_intro(txt):
    size = len(txt)
    replace = "....."
    dotted = txt.replace(txt[size - 15:], replace)
    return dotted

info = {
    "photo": "chris.png",
    "name": "Chris James",
    "title": "A.I Expert",
    "lang": "English",
    "intro": "Passionate full-stack artificial intelligence developer",
    "about": "$2000",
    "website": "techa.com",
    "email":"techa@tech.com",
    "phone":"08138958645",
    "coursecount":45,
    "newcourse":6,
    "rating":345,
    "approx_rating": 4.85,
    "hours": 243,
    "trainee": 24.35,

 "course": {
        'unique':{ 
            "photo": "course-1.webp",
            "title": "Advanced React Web Developer Course",
            "fee": "27.50",
            "rating": 4
        },

        'unique2':{
            "photo": "course-2.webp",
            "title": "Python for Beginners: From Zero to Expert",
            "fee": "15.50",
            "rating": 5
        },
        'unique3':{
             "photo": "course-3.webp",
            "title": "Learn and Understand NodeJS",
            "fee": "44.25",
            "rating": 3
        },
        'unique4':{
             "photo": "course-4.webp",
            "title": "HTML 5 - The Complete Guide for Every Level",
            "fee": 27.50,
            "rating": 4
        },
        'unique5':{ 
             "photo": "course-5.webp",
            "title": "Advanced Techniques with Gulpjs",
            "fee": 23.25,
            "rating": 4
        },
        'unique6':{
             "photo": "course-6.webp",
            "title": "Introduction to Sass with Full Website",
            "fee": "19.65",
            "rating": 2
        }
    },

    "review" :{
    'user1':{
        'photo':'chris.png',
        'name':'Chris James',
        'rating':4,
        'comment':'What an awesome developer!, we love you',
        'when':'last week tuesday'
            },
    'user2':{
        'photo':'chris.png',
        'name':'Chris James',
        'rating':4,
        'comment':'Cupcake cake fruitcake. Powder chocolate bar soufflé gummi bears topping donut.',
        'when':'2 days ago',
        },
    'user3':{
        'photo':'chris.png',
        'name':'Chris James',
        'rating':4,
        'comment':'Still in the proces of building techa and..',
        'when':'2 months ago',
    }
    }

    
    }