#data = Course.query.filter().all()

def rater(r):
    match r:
        case 5:
            return '<option value="1">1</option> <option value="2">2</option> <option value="3">3</option>\
                <option value="4">4</option> <option value="5">5</option>'
        case 1:
            return '1.svg'
        case 2:
            return '2.svg'
        case 3:
            return '3.svg'
        case 4:
            return '4.svg'
        case _:
            pass
    pass

def badger(level):
    match level:
        case 0:
            return '0.svg'
        case 1:
            return '1.svg'
        case 2:
            return '2.svg'
        case 3:
            return '3.svg'
        case 4:
            return '4.svg'
        case _:
            return '0.svg'


rel = {
    "1": {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" \
            stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="acorn-icons \
                acorn-icons-cupcake text-primary"><path d="M16.5 11.5L14.5586 12.2894C13.6118 12.6743 12.527 12.4622 11.7949 \
                    11.7489V11.7489C10.7962 10.7757 9.20383 10.7757 8.20507 11.7489V11.7489C7.47305 12.4622 6.38817 12.6743 5.44139 \
                        12.2894L3.5 11.5"></path><path d="M14 5L15.1555 5.30852C16.0463 5.54637 16.7839 6.17049 17.1659 \
                            7.00965V7.00965C17.6884 8.15765 17.6161 9.48873 16.9721 10.5733L16.3962 11.5433C16.2168 11.8454 16.0919 \
                                12.1767 16.0271 12.522L15.4588 15.5529C15.1928 16.9718 13.9539 18 12.5102 18H7.48978C6.04613 18 4.80721 \
                                    16.9718 4.54116 15.5529L3.97288 12.522C3.90813 12.1767 3.78322 11.8454 3.60383 11.5433L3.0279 \
                                        10.5733C2.38394 9.48873 2.31157 8.15765 2.83414 7.00965V7.00965C3.21614 6.17049 3.95371 5.54637 \
                                            4.84452 5.30852L6 5"></path><path d="M6 6.5C6 4.29086 7.5454 2 10 2C12.4546 2 14 4.29086 14 \
                                                6.5"></path></svg>',
        "cat": "Web Application Development",
        "count": 99
    },
    "2":{
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="acorn-icons acorn-icons-cupcake text-primary"><path d="M16.5 11.5L14.5586 12.2894C13.6118 12.6743 12.527 12.4622 11.7949 11.7489V11.7489C10.7962 10.7757 9.20383 10.7757 8.20507 11.7489V11.7489C7.47305 12.4622 6.38817 12.6743 5.44139 12.2894L3.5 11.5"></path><path d="M14 5L15.1555 5.30852C16.0463 5.54637 16.7839 6.17049 17.1659 7.00965V7.00965C17.6884 8.15765 17.6161 9.48873 16.9721 10.5733L16.3962 11.5433C16.2168 11.8454 16.0919 12.1767 16.0271 12.522L15.4588 15.5529C15.1928 16.9718 13.9539 18 12.5102 18H7.48978C6.04613 18 4.80721 16.9718 4.54116 15.5529L3.97288 12.522C3.90813 12.1767 3.78322 11.8454 3.60383 11.5433L3.0279 10.5733C2.38394 9.48873 2.31157 8.15765 2.83414 7.00965V7.00965C3.21614 6.17049 3.95371 5.54637 4.84452 5.30852L6 5"></path><path d="M6 6.5C6 4.29086 7.5454 2 10 2C12.4546 2 14 4.29086 14 6.5"></path></svg>',
        "cat": "React & React Native",
        "count": 99
        },
    "3":{
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="acorn-icons acorn-icons-radish text-primary"><path d="M11.7852 15.4134C9.18166 18.0169 4.8614 17.9177 3.53558 16.5919C2.20976 15.2661 2.11059 10.9458 4.71409 8.34231C7.31758 5.73881 8.82906 4.91481 12.0209 8.10661C15.2127 11.2984 14.3887 12.8099 11.7852 15.4134Z"></path><path d="M6.36401 8.10657 8.13178 9.87433M9 14 10.7678 15.7678M3 12 4.76777 13.7678M12.1777 7.94978V7.94978C13.4445 6.68295 15.3799 6.36889 16.9823 7.1701L17.1274 7.24268M12.1777 7.94975V7.94975C13.4445 6.68292 13.7586 4.74757 12.9573 3.14515L12.8848 3M14.157 6.00006 15.5712 4.58585"></path></svg>',
        "cat": "Python programming",
        "count": 45
        },
    '4': {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="acorn-icons acorn-icons-banana text-primary"><path d="M16.7566 4.98357L16.987 3.71739C17.1028 3.08064 16.9034 2.42718 16.4517 1.96363L16 1.5"></path><path d="M13.0879 16.3477C8.8506 18.7942 3.90457 18.1602 2.04063 14.9318C0.176701 11.7034 5.44182 14.9166 10.5567 11.9636C15.6716 9.01049 15.5214 2.84411 17.3853 6.07254C19.2492 9.30097 17.3252 13.9013 13.0879 16.3477Z"></path></svg>',
        "cat": "Hacking",
        "count": 44
        }
        }

related = {
    "id1": {
        "title": "Chris James",
        "topic": "Python programming"
    },
    "id2":{
        "title": "Smith",
        "topic": "Jane"
        },
    "id3":{
        "title" : 15,
        "topic": "Data Structures and Algorithms"
        },
    'id4': {
        "title" : 'React programming',
        "topic": "Hooks and usestates"
        }
        }
        

courses = {
    
    "A": {
        "title": "Advanced React Developer",
        "photo": "course-1.webp",
        "oldfee": "$5000",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
    },
    "B":{
        "title": "Python for Beginners: From Zero to Expert",
        "photo": "course-2.webp",
        "oldfee": "$6000",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    "C":{
        "title": "Learn ad Understand NodeJS",
        "photo": "course-3.webp",
        "oldfee": "$7000",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
"related": "A"
        },
    'D': {
        "title": "HTML 5 -The Complete Guide for Every Level",
        "photo": "course-4.webp",
        "oldfee": "$10,000",
        "fee": "$8000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
"related": "A"
        },
    'E': {
        "title": "Introduction to Sass with full website",
        "photo": "course-5.webp",
        "oldfee": "$6,000",
        "fee": "$3000",
        "rating": "4.95",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
"related": "A"
        },
    'F': {
        "title": "Java - The Complete Guide",
        "photo": "course-6.webp",
        "oldfee": "$40,000",
        "fee": "$8000",
        "rating": "4.89",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    'G': {
        "title": "PHP for beginners with CMS Project",
        "photo": "course-7.webp",
        "oldfee": "$10,000",
        "fee": "$7000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    'H': {
        "title": "10 Real Life C++ Projects",
        "photo": "course-8.webp",
        "oldfee": "$100,000",
        "fee": "$24.99",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    'I': {
        "title": "Introduction to Ubuntu: Best Practice For Beginners",
        "photo": "course-9.webp",
        "oldfee": "$10,000",
        "fee": "$8000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    'J': {
        "title": "Advanced React Developer",
        "photo": "course-4.webp",
        "oldfee": "$10,000",
        "fee": "$8000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    'K': {
        "title": "Advanced React Developer",
        "photo": "course-10.webp",
        "oldfee": "$10,000",
        "fee": "$8000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": "A"
        },
    2 : {
        "title": "Advanced React Developer",
        "photo": "course-4.webp",
        "oldfee": "$10,000",
        "fee": "$8000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
        "trend": 1,
        "related": ["A","B","F","G"]
        },


        }


#CHAPTERS
lesson = {
        '01.Dashboards': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies "
            
            },
        '02.Applications': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '03.Interface': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '04.Conclusion': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '05.What\'s Next': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '06.Credits': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies"
            
            }

        },

#INTRODUCTORY PART OF COURSE
info = { 

    "badger": badger,
    "title": "Advanced React Developer",
    "photo": "course-2.webp",
    "poster": "course-1.webp",
    "video": "View_From_A_Blue_Moon_Trailer-576p.mp4",
    "fee": "$2000",
    "rating": 4.5,
    "duration":"duration",
    "category":"category",
    "views":"12k",
    "comment":"289",
    "tutor_photo":"chris.png",
    "tutor_name":"chris James",
    "tutor_title":"A.I Expert",
    "kwords":"kwords",
"trend": 1,
"related": "A",
    "content":"This is a test introduction of the courses. Python Programming just got easier than expected \
        with russian advanced developers prorams"
}

tags = {
        "python": 400, 
        "react": 300,
        "hacking": 88,
        "ruby-on-rails":1,
        "amazon tech": 34
    } 

#REVIEWS:
rev_test = [
        {
        'photo':'chris.png',
        'name':'Chris James',
        'rating':5,
        'comment':'What an awesome developer!, we love you',
        'when':'last week tuesday'
        },
        {
        'photo':'chris.png',
        'name':'Chris James',
        'rating':4,
        'comment':'Cupcake cake fruitcake. Powder chocolate bar soufflé gummi bears topping donut.',
        'when':'2 days ago',
        },
        {
        'photo':'chris.png',
        'name':'Chris James',
        'rating':4,
        'comment':'Still in the proces of building techa and..',
        'when':'2 months ago',
        }
],

#REVIEWS:
rev = {

        'avg':'5.6',
        'total':56,
        'rating':4,

        "person" : {
    
            'user1':{
                'photo':'chris.png',
                'name':'Chris James',
                'rating':5,
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

    },

#AT GLANCE
glance = {
        "duration": "70hours",
        "content": "8 Chapters",
        "level": "Beginner",
        "release": "05.11.2021",
        "rating": "4.8(843)",
        "completed": "1.522"
    },

#BADGES
badge = {
        'unique':{
            'title':'No Badge(s)',
            'level': 0
        },
        'unique0':{
            'title':'Javascript Novice',
            'level': 1
        },
        'unique1':{
            'title':'React Beginner',
            'level': 2
        },
        'unique2':{
            'title':'Node.js Expert',
            'level': 3
        },
        'unique3':{
            'title':'Front-end Appprentice',
            'level': 4
        }
    }

#SECTIONS -> based on chapter(id)
sections = {
    '0':{
            'topic':'The SQL SELECT Statement',
            'body': 'The SELECT statement is used to select data from a database.The result is stored in a result table, \
                called the result-set.'
        },
    '1':{
            'topic':'SELECT Column Example',
            'body': 'The following SQL statement selects the "CustomerName" and "City" columns from the "Customers" table:<br>\
                SELECT * FROM Customers; '
        },
    '2':{
            'topic':'Navigation in a Result-set',
            'body': 'Most database software systems allow navigation in the result-set with programming functions, \
                like: Move-To-First-Record, Get-Record-Content, Move-To-Next-Record, etc.'
        },
    '3':{
            'topic':'SQL SELECT DISTINCT Statement',
            'body': 'The SELECT DISTINCT statement is used to return only distinct (different) values.'
        },
    '4':{
            'topic':'The SQL SELECT DISTINCT Statement',
            'body': 'In a table, a column may contain many duplicate values; and sometimes you only want to list the different (distinct) \
                values.The DISTINCT keyword can be used to return only distinct (different) values. SQL SELECT DISTINCT Syntax \
                    SELECT DISTINCT column_name,column_name FROM table_name;'
        }
}

trend = {
    
    "A": {
        "title": "Advanced React Developer",
        "photo": "course-2.webp",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
"trend": 1,
"related": "A"
    },
    "B":{
        "title": "Advanced React Developer",
        "photo": "course-2.webp",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
"trend": 1,
"related": "A"
        },
    "C":{
        "title": "Advanced React Developer",
        "photo": "course-2.webp",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
"trend": 1,
"related": "A"
        },
    'D': {
        "title": "Advanced React Developer",
        "photo": "course-2.webp",
        "fee": "$2000",
        "rating": "4.5",
        "duration":"duration",
        "category":"category",
        "kwords":"kwords",
"trend": 1,
"related": "A"
        },
    'E': {
        "title": "Android Development(Java)",
        "photo": "course-7.webp",
        "oldfee": "$11.00",
        "fee": "$11.00",
        "rating": "4.5"
        },


        },

#fetch a particlular course with the unique
course_data = { 
    "badger": badger,
    "title": "Advanced React Developer",
    "photo": "course-2.webp",
    "poster": "course-1.webp",
    "video": "View_From_A_Blue_Moon_Trailer-576p.mp4",
    "fee": "$2000",
    "rating": 4.5,
    "duration":"duration",
    "category":"category",
    "views":"12k",
    "comment":"289",
    "tutor_photo":"chris.png",
    "tutor_name":"chris James",
    "tutor_title":"A.I Expert",
    "kwords":"kwords",
    
"trend": 1,
"related": "A",
    "content":"This is a test introduction of the courses. Python Programming just got easier than expected \
        with russian advanced developers prorams", 
    
    "tags": "python(400) react(300) hacking(88) ruby-on-rails(1) amazon tech",

    
    'chapters': {
        '01.Dashboards': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '02.Applications': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '03.Interface': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '04.Conclusion': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '05.What\'s Next': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            },
        '06.Credits': 
            { 
                1: "- Danish brownie fruitcake tootsie",
                2: "- Fruitcake tart dessert",
                3: "- Snaps muffin macaroon tiramisu",
                4: "- Ice cream marshmallow",
                5: "- Plum caramels fruitcake",
                6: "- Bar carrot cake",
                7: "- - Snaps muffin macaroon tiramisu",
                8: "- Danish cake gummies jelly",
                9: "- Bar carrot cake",
                10: "- Cotton candy gummies ",
            
            }

        },

    "reviews": {
        'avg':'5.6',
        'total':56,
        'rating':4,

        "reviewer" :{
            'user1':{
                'photo':'chris.png',
                'name':'Chris James',
                'rating':5,
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

    },

    "glance":{
        "duration": "70hours",
        "content": "8 Chapters",
        "level": "Beginner",
        "release": "05.11.2021",
        "rating": "4.8(843)",
        "completers": "1.522"
    },

    "badge": {
        'unique':{
            'title':'No Badge(s)',
            'level': 0
        },
        'unique0':{
            'title':'Javascript Novice',
            'level': 1
        },
        'unique1':{
            'title':'React Beginner',
            'level': 2
        },
        'unique2':{
            'title':'Node.js Expert',
            'level': 3
        },
        'unique3':{
            'title':'Front-end Appprentice',
            'level': 4
        }
    }
    
    } 
    
    

