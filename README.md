# Streakbot :fire:

Streakbot is a telegram bot aimed to build effective habits with the use of streaks (think snapchat!). It's often said that it takes 30 days to build a habit and this bot challenges that belief with a system to help you create and track habits daily. With a scheduler function in place, a reminder is set for users daily to perform their habits daily. See below for more pictures and how you can start your journey with Streakbot today! :)

## Table of Contents
1. [Aim & User Stories](https://github.com/ykwei7/streakbot/blob/main/README.md#aim-and-user-stories)
2. [Features and Timeline](https://github.com/ykwei7/streakbot/blob/main/README.md#features-and-timeline)
3. [Learning Points](https://github.com/ykwei7/streakbot/blob/main/README.md#learning-points)
4. [Tech Stack](https://github.com/ykwei7/streakbot/blob/main/README.md#tech-stack)

## Aim and User Stories

The goal of streakbot is for users to create habits and perform them daily. As shown in [Atomic Habits](https://jamesclear.com/atomic-habits) by James Clear, habit building can be broken down into this four step pattern:

1. Cue - Make it obvious
2. Craving - Make it attractive
3. Response - Make it easy
4. Reward - Make it satisfying

For instance, given a scenario where you may hope to cultivate a habit of drinking water after waking up, you would start with adding a habit. Creating a habit is a fast process and with a few steps, it can be setup quickly.

<img width="264" alt="image" src="https://user-images.githubusercontent.com/60681330/180654106-2ee87ee1-086d-4713-bf18-94b83600d837.png">

A cue is then set into place when we receive this reminder the instant we wake up.

<img width="214" alt="image" src="https://user-images.githubusercontent.com/60681330/182628192-49dffcb1-4b45-4ca8-86de-5a5ffbd60f38.png">
 
Upon completion of this habit, we can click on "Completed" to mark this as completed for the day. Our streak is now up to 1, with 29 more days to go! And hopefully this serves as a visual craving to work towards the magical number of 30.

<img width="208" alt="image" src="https://user-images.githubusercontent.com/60681330/183230591-eaa0f46c-a371-4425-bfd6-f5552f7ab27d.png">

Upon hitting the 30 day mark, we are then rewarded with a special celebratory message! (Blurred to encourage you to see it for yourself)

<img width="218" alt="image" src="https://user-images.githubusercontent.com/60681330/183231092-2cced0fe-6c5e-44a8-b118-d760d9a632ce.png">
 
Ultimately, the most important part about habit building is to be consistent and Streakbot makes this process seamless and rewarding for you. Unsure about what to cultivate? Here's a quick [article](https://dariusforoux.com/habits-with-huge-return-on-life/) to get you started so create a habit, and start your journey today! 

## Features and Timeline

##### Feature 1: Tracking of habits
 
<img width="209" alt="image" src="https://user-images.githubusercontent.com/60681330/182632610-76485ade-145a-446c-89a5-7deba3018dc8.png">

Users can view all habits and track their progress for each individual habit.
<hr/>
 
##### Feature 2: Daily reminder for habits
 
<img width="214" alt="image" src="https://user-images.githubusercontent.com/60681330/182628192-49dffcb1-4b45-4ca8-86de-5a5ffbd60f38.png">
 
Users are reminded daily based on the timing set for each habit.
 
This is implemented via the `APScheduler` package where jobs are added to a scheduler. 
 
```python
self.scheduler.add_job(self.remind, trigger='interval', days = 1, 
 start_date=f"{currDate} 08:00:00", jobstore="default", args=[habit, None, user_id],
 replace_existing=True, id=unique_id, misfire_grace_time=30) 
```
 
Through this, the scheduler fires the `remind` function daily at `08:00 hours`.  
<hr/>
 
##### Feature 3: Streak tracking feature

<img width="208" alt="image" src="https://user-images.githubusercontent.com/60681330/183230594-5ca301ae-ae6e-4557-986b-e5882d321dfb.png">

Users can track the streaks for each habit and provides a motivation to keep the streak going.

## Learning Points
 
Database Interaction
- Building this telegram bot allowed me to learn more on how to interact safely with databases and apply good coding practices to prevent attacks like SQL injections.
- Points for improvement would include using a database pool and external tools like SQLAlchemy to prevent recreating database connections and instead reuse existing connections 

Use of Utils
- This project made use of loggers, python package management and proper secret management. 
- The use of different modes of loggers (e.g DEBUG, INFO) alongside exception handling allowed for easier (and nicer looking) debugging and understanding the control flow of the programme
 <img width="440" alt="image" src="https://user-images.githubusercontent.com/60681330/180655514-e72a0686-d19d-46fa-89fe-1b2cd5b1d525.png">

- Poetry was also utilized in this project over other management tools like Anaconda and Pip to improve handling of dependency conflicts and reduce the downloading of unnecessary packages.
 
- Secret management was also improved through refactoring the variables into a secret.env file 
 
## Tech Stack
 - Python
 - Heroku 
 - PostgreSQL 
 - Poetry 


