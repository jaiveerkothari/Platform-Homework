Platform Homework for the Sprout Social Interview

Developed for Django 1.9

To run the app,
navigate to project directory
>> cd Platform-Homework

>> python manage.py runserver

go to http://127.0.0.1:8000/tweets/
this is the homepage of the django app called tweets, which implements as basic REST api. 

From this page, you can go to http://127.0.0.1:8000/tweets/view01/ to get a user's home_timeline (last 20 objects). 
If the inputted user_id is valid, then a json object of the home_timeline will be rendered. If the input is invalid, an error message in the form on json will be rendered. 

On http://127.0.0.1:8000/tweets/view02/ you can send a tweet from the given user's account.

If the tweet is sent succesfully, a success message will be displayed. If there is an error, the error message will be printed to the screen. 


