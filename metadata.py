import time




Exam_Title = "UPSC"
Booklet = "A"

start_time = time.time()  # This gives time in epochs
exam_start_time = time.strftime("%H:%M:%S", time.localtime(start_time))
end_time = start_time + 240
exam_end_time = time.strftime("%H:%M:%S", time.localtime(end_time))

cities = [
"Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", 
"Pune", "Jaipur", "Lucknow", "Chandigarh", 
"Surat", "Ahmedabad", "Mumbai"
]


server_URL = "http://192.168.29.106:2222"
insert_data_endpoint = "/insert_data"
validate_user_endpoint = "/validate_user"

centers = {
            "Delhi": ["Jawaharlal Nehru Stadium", "Indira Gandhi Indoor Stadium", "Dyal Singh College", "Miranda House"],
            "Bangalore": ["Bangalore University", "RV College of Engineering", "Christ University", "Mount Carmel College"],
            "Hyderabad": ["Osmania University", "Jawaharlal Nehru Technological University", "St. Francis College", "Nizam College"],
            "Chennai": ["Anna University", "Loyola College", "Madras Christian College", "SRM Institute of Science and Technology"],
            "Kolkata": ["Calcutta University", "Jadavpur University", "Presidency University", "St. Xavier's College"],
            "Pune": ["Savitribai Phule Pune University", "Fergusson College", "Symbiosis International University", "MIT World Peace University"],
            "Jaipur": ["University of Rajasthan", "Malaviya National Institute of Technology", "Banasthali Vidyapith", "Jaipur National University"],
            "Lucknow": ["University of Lucknow", "Amity University", "Babu Banarasi Das University", "Indian Institute of Management"],
            "Chandigarh": ["Punjab University", "Panjab Engineering College", "DAV College", "GGDSD College"],
            "Surat": ["Veer Narmad South Gujarat University (VNSGU)", "D.R.B College", "St. Thomas School", "Sardar Vallabhbhai National Institute of Technology (SVNIT)"],
            "Ahmedabad": ["Gujarat University", "L.D. College of Engineering", "St. Xavier's College", "Indian Institute of Management (IIM)"],
            "Mumbai": ["University of Mumbai", "Indian Institute of Technology (IIT) Bombay", "St. Xavier's College", "Narsee Monjee Institute of Management Studies (NMIMS)"]
        }




quiz_data = {
  "booklets": {
    "A": {
      "questions": [
        "Which animal is known as the 'king of the jungle'?",
        "What is the only mammal capable of flight?",
        "Which fruit is known as the 'king of fruits'?",
        "What is the name of the fairy in Peter Pan?",
        "Which planet is known as the 'Red Planet'?",
        "How many colors are there in a rainbow?",
        "Which fictional character is known for saying 'To infinity and beyond!'?",
        "What is the most common blood type in humans?",
        "What animal is known for its ability to change colors?",
        "Which fruit is often mistaken for a vegetable?",
        "What is the name of the toy cowboy in 'Toy Story'?",
        "Which bird is known for its ability to mimic human speech?",
        "What is the largest organ in the human body?",
        "Which country is known as the 'Land of the Rising Sun'?",
        "What is the capital city of Australia?",
        "What color are the berries of a holly plant?",
        "Which planet is known for its rings?",
        "Which animal can sleep for up to three years?",
        "Which famous scientist developed the theory of relativity?",
        "What is the hottest planet in our solar system?",
        "What is the name of the fictional wizarding school in the Harry Potter series?",
        "Which vegetable is known for making people cry when cut?",
        "What is the name of the superhero with the alter ego Bruce Wayne?",
        "Which classic toy has the slogan 'Play-Doh'?",
        "What is the smallest country in the world?",
        "Which animal is known for its distinctive black and white stripes?",
        "Which famous artist cut off part of his own ear?",
        "What type of animal is the 'Loch Ness Monster' reputed to be?",
        "Which plant is known for producing the world's hottest chili peppers?",
        "What is the term for a word that is spelled the same forwards and backwards?",
        "Which popular soda brand has a red and white logo and is known for its 'Santa Claus' ads?",
        "What do you call a group of lions?",
        "Which famous musician is known as the 'King of Pop'?",
        "What is the name of the fictional city where Batman lives?",
        "Which fruit is known as the 'apple of paradise'?",
        "What is the term for a fear of spiders?",
        "Which fictional character is known for his green skin and love of eating flies?",
        "What is the name of the fairy tale character who had a glass slipper?",
        "Which animal is known for its long neck and legs, and lives in Africa?",
        "What is the term for a fear of heights?",
        "Which famous painter is known for his 'Starry Night'?",
        "Which bird is famous for its colorful tail feathers and courtship dance?",
        "What is the name of the mythical creature that breathes fire?",
        "Which country is known for inventing pizza?",
        "What is the term for a word that sounds like what it describes, like 'buzz' or 'clang'?",
        "What is the name of the actor who played Jack Sparrow in 'Pirates of the Caribbean'?",
        "Which planet is known as the 'Giant Red Spot'?",
        "What is the name of the ship that famously sank on its maiden voyage in 1912?",
        "Which type of bear is known for its white fur and lives in the Arctic?",
        "What is the term for a word that has the opposite meaning of another word?",
        "Which superhero is known for his web-slinging abilities and his secret identity as Peter Parker?",
        "What is the name of the fictional detective created by Sir Arthur Conan Doyle?"
      ],
      "options": 
        [
          ["Lion", "Elephant", "Tiger", "Bear"],
          ["Bat", "Bird", "Insect", "Squirrel"],
          ["Durian", "Mango", "Banana", "Apple"],
          ["Tinker Bell", "Cinderella", "Snow White", "Aurora"],
          ["Mars", "Venus", "Jupiter", "Saturn"],
          ["7", "6", "8", "5"],
          ["Buzz Lightyear", "Woody", "Mr. Potato Head", "Rex"],
          ["O", "A", "B", "AB"],
          ["Chameleon", "Lizard", "Frog", "Snake"],
          ["Tomato", "Cucumber", "Pepper", "Carrot"],
          ["Woody", "Buzz Lightyear", "Mr. Potato Head", "Rex"],
          ["Parrot", "Crow", "Sparrow", "Pigeon"],
          ["Skin", "Liver", "Heart", "Lungs"],
          ["Japan", "China", "South Korea", "Thailand"],
          ["Sydney", "Melbourne", "Brisbane", "Canberra"],
          ["Red", "Blue", "Green", "Yellow"],
          ["Saturn", "Uranus", "Neptune", "Mars"],
          ["Snail", "Bat", "Turtle", "Elephant"],
          ["Einstein", "Newton", "Galileo", "Copernicus"],
          ["Venus", "Mercury", "Earth", "Mars"],
          ["Hogwarts", "Durmstrang", "Beauxbatons", "Ilvermorny"],
          ["Onion", "Garlic", "Chili", "Pepper"],
          ["Superman", "Batman", "Spider-Man", "Iron Man"],
          ["Barbie", "Play-Doh", "LEGO", "Hot Wheels"],
          ["Vatican City", "San Marino", "Monaco", "Liechtenstein"],
          ["Zebra", "Giraffe", "Leopard", "Tiger"],
          ["Van Gogh", "Picasso", "Monet", "Rembrandt"],
          ["Dinosaur", "Dragon", "Unicorn", "Mermaid"],
          ["Habanero", "Jalapeño", "Bell Pepper", "Serrano"],
          ["Palindrome", "Anagram", "Homophone", "Synonym"],
          ["Coca-Cola", "Pepsi", "Sprite", "7 Up"],
          ["Pride", "Pack", "Herd", "School"],
          ["Elvis Presley", "Michael Jackson", "Prince", "Madonna"],
          ["Gotham City", "Metropolis", "Star City", "Central City"],
          ["Mango", "Papaya", "Pineapple", "Apple"],
          ["Arachnophobia", "Claustrophobia", "Acrophobia", "Nyctophobia"],
          ["Shrek", "Kermit the Frog", "Oscar the Grouch", "Fozzie Bear"],
          ["Cinderella", "Snow White", "Sleeping Beauty", "Rapunzel"],
          ["Giraffe", "Elephant", "Hippopotamus", "Lion"],
          ["Acrophobia", "Claustrophobia", "Nyctophobia", "Agoraphobia"],
          ["Van Gogh", "Monet", "Rembrandt", "Picasso"],
          ["Peacock", "Parrot", "Flamingo", "Eagle"],
          ["Dragon", "Phoenix", "Unicorn", "Griffin"],
          ["Italy", "France", "Greece", "Spain"],
          ["Onomatopoeia", "Oxymoron", "Hyperbole", "Metaphor"],
          ["Johnny Depp", "Orlando Bloom", "Geoffrey Rush", "Harrison Ford"],
          ["Jupiter", "Saturn", "Neptune", "Mars"],
          ["Titanic", "Lusitania", "Olympic", "Britannic"],
          ["Polar Bear", "Brown Bear", "Grizzly Bear", "Black Bear"],
          ["Antonym", "Synonym", "Homonym", "Palindrome"],
          ["Spider-Man", "Iron Man", "Thor", "Hulk"],
          ["Sherlock Holmes", "Hercule Poirot", "Miss Marple", "Nero Wolfe"]
      ],
      "answers": [
        "Lion",
        "Bat",
        "Durian",
        "Tinker Bell",
        "Mars",
        "7",
        "Buzz Lightyear",
        "O",
        "Chameleon",
        "Tomato",
        "Woody",
        "Parrot",
        "Skin",
        "Japan",
        "Canberra",
        "Red",
        "Saturn",
        "Snail",
        "Einstein",
        "Venus",
        "Hogwarts",
        "Chili",
        "Batman",
        "Play-Doh",
        "Vatican City",
        "Zebra",
        "Van Gogh",
        "Dragon",
        "Habanero",
        "Palindrome",
        "Coca-Cola",
        "Pride",
        "Michael Jackson",
        "Gotham City",
        "Mango",
        "Arachnophobia",
        "Kermit the Frog",
        "Cinderella",
        "Giraffe",
        "Acrophobia",
        "Van Gogh",
        "Peacock",
        "Dragon",
        "Italy",
        "Onomatopoeia",
        "Johnny Depp",
        "Jupiter",
        "Titanic",
        "Polar Bear",
        "Antonym",
        "Spider-Man",
        "Sherlock Holmes"
      ]
    },
    "B": {
      "questions": [
        "What is the name of the toy cowboy in 'Toy Story'?",
        "What is the name of the fairy in Peter Pan?",
        "What is the hottest planet in our solar system?",
        "Which fruit is known as the 'king of fruits'?",
        "Which animal is known as the 'king of the jungle'?",
        "How many colors are there in a rainbow?",
        "Which planet is known for its rings?",
        "What is the only mammal capable of flight?",
        "Which country is known as the 'Land of the Rising Sun'?",
        "Which vegetable is known for making people cry when cut?",
        "Which superhero is known for his web-slinging abilities and his secret identity as Peter Parker?",
        "What is the term for a word that is spelled the same forwards and backwards?",
        "Which bird is known for its ability to mimic human speech?",
        "What is the name of the fictional city where Batman lives?",
        "Which classic toy has the slogan 'Play-Doh'?",
        "Which planet is known as the 'Red Planet'?",
        "What is the term for a word that sounds like what it describes, like 'buzz' or 'clang'?",
        "Which animal is known for its distinctive black and white stripes?",
        "Which famous artist cut off part of his own ear?",
        "What is the name of the actor who played Jack Sparrow in 'Pirates of the Caribbean'?",
        "What is the name of the mythical creature that breathes fire?",
        "Which fruit is often mistaken for a vegetable?",
        "What is the name of the fictional detective created by Sir Arthur Conan Doyle?",
        "Which type of bear is known for its white fur and lives in the Arctic?",
        "Which animal can sleep for up to three years?",
        "What is the term for a fear of heights?",
        "Which country is known for inventing pizza?",
        "What do you call a group of lions?",
        "Which famous musician is known as the 'King of Pop'?",
        "What is the smallest country in the world?",
        "What is the capital city of Australia?",
        "What is the name of the fictional wizarding school in the Harry Potter series?",
        "What is the smallest country in the world?",
        "What is the term for a fear of spiders?",
        "Which fruit is known as the 'apple of paradise'?",
        "What is the name of the fictional city where Batman lives?",
        "What is the name of the fairy tale character who had a glass slipper?",
        "Which bird is famous for its colorful tail feathers and courtship dance?",
        "Which plant is known for producing the world's hottest chili peppers?",
        "Which animal is known for its long neck and legs, and lives in Africa?",
        "Which superhero is known for his web-slinging abilities and his secret identity as Peter Parker?",
        "Which fictional character is known for saying 'To infinity and beyond!'?",
        "What is the most common blood type in humans?"
      ],
      "options": [
          ["Woody", "Buzz Lightyear", "Mr. Potato Head", "Rex"],
          ["Tinker Bell", "Cinderella", "Snow White", "Aurora"],
          ["Venus", "Mercury", "Earth", "Mars"],
          ["Durian", "Mango", "Banana", "Apple"],
          ["Lion", "Elephant", "Tiger", "Bear"],
          ["7", "6", "8", "5"],
          ["Saturn", "Uranus", "Neptune", "Mars"],
          ["Bat", "Bird", "Insect", "Squirrel"],
          ["Japan", "China", "South Korea", "Thailand"],
          ["Onion", "Garlic", "Chili", "Pepper"],
          ["Spider-Man", "Batman", "Iron Man", "Thor"],
          ["Palindrome", "Anagram", "Homophone", "Synonym"],
          ["Parrot", "Crow", "Sparrow", "Pigeon"],
          ["Gotham City", "Metropolis", "Star City", "Central City"],
          ["Play-Doh", "LEGO", "Hot Wheels", "Barbie"],
          ["Mars", "Venus", "Jupiter", "Saturn"],
          ["Onomatopoeia", "Oxymoron", "Hyperbole", "Metaphor"],
          ["Zebra", "Giraffe", "Leopard", "Tiger"],
          ["Van Gogh", "Picasso", "Monet", "Rembrandt"],
          ["Johnny Depp", "Orlando Bloom", "Geoffrey Rush", "Harrison Ford"],
          ["Dragon", "Phoenix", "Unicorn", "Griffin"],
          ["Tomato", "Cucumber", "Pepper", "Carrot"],
          ["Sherlock Holmes", "Hercule Poirot", "Miss Marple", "Nero Wolfe"],
          ["Polar Bear", "Brown Bear", "Grizzly Bear", "Black Bear"],
          ["Snail", "Bat", "Turtle", "Elephant"],
          ["Acrophobia", "Claustrophobia", "Nyctophobia", "Agoraphobia"],
          ["Italy", "France", "Greece", "Spain"],
          ["Pride", "Pack", "Herd", "School"],
          ["Michael Jackson", "Elvis Presley", "Prince", "Madonna"],
          ["Vatican City", "San Marino", "Monaco", "Liechtenstein"],
          ["Canberra", "Sydney", "Melbourne", "Brisbane"],
          ["Hogwarts", "Durmstrang", "Beauxbatons", "Ilvermorny"],
          ["Papaya", "Pineapple", "Mango", "Apple"],
          ["Arachnophobia", "Claustrophobia", "Acrophobia", "Nyctophobia"],
          ["Apple", "Mango", "Papaya", "Pineapple"],
          ["Gotham City", "Metropolis", "Star City", "Central City"],
          ["Cinderella", "Snow White", "Sleeping Beauty", "Rapunzel"],
          ["Peacock", "Parrot", "Flamingo", "Eagle"],
          ["Habanero", "Jalapeño", "Bell Pepper", "Serrano"],
          ["Giraffe", "Elephant", "Hippopotamus", "Lion"],
          ["Spider-Man", "Iron Man", "Thor", "Hulk"],
          ["Buzz Lightyear", "Woody", "Mr. Potato Head", "Rex"],
          ["O", "A", "B", "AB"]
        ],
      "answers": [
        "Woody",
        "Tinker Bell",
        "Venus",
        "Durian",
        "Lion",
        "7",
        "Saturn",
        "Bat",
        "Japan",
        "Onion",
        "Spider-Man",
        "Palindrome",
        "Parrot",
        "Gotham City",
        "Play-Doh",
        "Mars",
        "Onomatopoeia",
        "Zebra",
        "Van Gogh",
        "Johnny Depp",
        "Dragon",
        "Tomato",
        "Sherlock Holmes",
        "Polar Bear",
        "Snail",
        "Acrophobia",
        "Italy",
        "Pride",
        "Michael Jackson",
        "Vatican City",
        "Canberra",
        "Hogwarts",
        "Papaya",
        "Arachnophobia",
        "Apple",
        "Gotham City",
        "Cinderella",
        "Peacock",
        "Habanero",
        "Giraffe",
        "Spider-Man",
        "Buzz Lightyear",
        "O"
      ]
    }
  }
}



