# UPSKILL PROJECT

### Your users should be able to:
1. Signup & log in with an email and password with account verification. There should be a
reset password feature to recover lost passwords password.
2. Learners Can download resources
3. Learners can view announcement
4. Real time chat app

### Admin
1. Perform CRUD on Course, Announcement, Resource, Room and Quiz 

## Installation

To install the project, you need to have Python 3 and pip installed on your system. Then, follow these steps:

- Clone this repository: 
[UpSkill](https://github.com/Kjeff24/UpSkill.git)
- Create a virtual environment: 
```
python -m venv venv
```
- Activate the virtual environment: 
```
`source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
```
- Install the required dependencies: 
```
pip install -r requirements.txt
```


## Usage

- To run the project, you can set your email and password to handle email being sent. You can use a `.env` file to store them or change them from `settings.py`. For example:

```
EMAIL_FROM_USER = 'your email'
EMAIL_HOST_USER = 'your email'
EMAIL_HOST_PASSWORD = 'your email password'
```

- Then, you can run the following commands:
``` 
python manage.py runserver
```

By default the development server will start at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


## Models
The project contains the following models:
| Models| Fields| Functions|
| ----- | ------| ---------|
| User |- is_tutor<br>- is_learner<br>- is_email_verified<br>- first_name<br>- last_name<br>- bio<br>- avatar |
| Course |- name<br>- description<br>- instructor<br>- created<br>- updated|
|Participants|- user<br>- course|
|Enrollment|- course<br>- date_enrolled<br>- members |
|Resource|- name<br>- course<br>- description<br>- youtubeLink<br>- file<br>- created<br>- updated |
|Announcement|- title<br>- content<br>- course<br>- date<br>- created<br>- updated|
|Room|- room_topic<br>- course<br>- room_description<br>- created<br>- updated|
|Message|- user<br>- room<br>- body<br>- updated<br>- created |
|Quiz|- name<br>- course<br>- number_of_questions<br>- time<br>- required_score_to_pass<br>- difficluty |- get_questions|
|Question|- text<br>- quiz<br>- created |- get_answers|
|Answer|- text<br>- correct<br>- question<br>- created |
|Result|- quiz<br>- user<br>- score<br>- completion_time<br>- created<br>- started  |


## Endpoints

The project provides the following endpoints:

- ` `: front page home
- `admin/`: Django admin (would be excluded during production)
- `tutor_admin/`: Custom django admin for each tutor
- `about/`: front page about
- `contact/`: front page contact
- `login/`: login page
- `logout/`: logout user
- `signup/`: signup
- `learner_home/<str:pk>/`: learner home
- `update_user/<str:pk>/`: update user
- `activate-user/<uidb64>/<token>`: account activation
- `reset_password/`: password reset
- `reset_password_sent/`: password reset sent
- `reset/<uidb64>/<token>/`: password reset form
- `reset_password_complete/`: password reset done
- `course/<str:pk>/`: course page
- `course/<str:pk>/resource`: resource page
- `course/<str:pk>/announcement`: announcement page
- `course/<str:pk>/chat_room`: chat room page
- `course/<str:pk>/quiz_page`: quiz page
- `course/<str:pk2>/chat_room/<str:pk>/`: individual chat room page 
- `profile/<str:pk>/`: user profile page 
- `course/<str:pk2>/quiz/`: view all quizzes of a course
- `course/<str:pk2>/quiz/<pk>/`: Real quiz and answers page
- `course/<str:pk2>/quiz/<pk>/save/`: save quiz
- `course/<str:pk2>/quiz/<pk>/data/`: view quiz solutions with their correct answers
- `api/login/`: login
- `api/register/`: register
- `api/logout/`: logout
- `api/courses/`: Get courses
- `api/participants/`: Get and post participants
- `api/announcements/`: Get announcements
- `api/messages/`: Get and post messages
- `api/rooms/`: Get rooms
- `re_path(r'^.*/$', custom_404)`: a view for unavailable pages

