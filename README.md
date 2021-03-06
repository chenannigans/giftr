giftr
===================
###Alice Seongyeon Park, Django Back-end (seongyeon.park@capitalone.com)
###Ann Chen, Front-end (ann.chen@capitalone.com)
###Christine Eunji Kim, DevEx API (eunji.kim@capitalone.com)
###Elaine Lee, DevEx API (elaine.lee2@capitalone.com)
A way to take the stress out of choosing gifts. Whether it be for family or coworkers, birthday or an anniversary, we got your back. We crowdsource gift ideas and incorporate the Capital One Developers Exchange API to make paying for your gifts easier.

Set Up
-------------
**May not connect to Capital One while on an enterprise machine.**

- Make sure you are running [Python 2.7](https://www.python.org/downloads/)
- Install [Django](https://docs.djangoproject.com/).
- Install the necessary modules by running the following on the Command Prompt/Terminal:
```
pip install requests
pip install Pillow 
```
- Migrate database on the Command Prompt/Terminal:
```
python manage.py makemigrations
python manage.py migrate
```
- Run the server by running the following on the Command Prompt/Terminal:
```
cd ...\giftr\hackathon (wherever you have giftr saved)
python manage.py runserver
```
- Open http://localhost:8000/ on your browser.

Logging In
-------------
![Alt text](/hackathon/img/login.png)

Log in with ease. You can connect through your giftr account, or set up the link to pull your rewards information into your giftr account.

![Alt text](/hackathon/img/devex_login.png)

Just enter your Capital One credentials and give our app permissions to access your Rewards information.

![Alt text](/hackathon/img/devex_auth.png)

View your cards and reward information at a glance.

![Alt text](/hackathon/img/cards.png)

Gallery
-------------
![Alt text](/hackathon/img/gallery.png)

See all the user-submitted gift ideas at a glance. You can select on any to take you to a vendor page. Notice your Capital One Rewards balance available to you on the top right corner.

Completely out of ideas? Try our randomize button and get a recommendation.

![Alt text](/hackathon/img/randomize.png)

Enter your past gift ideas with one simple form, and see the changes immediately in the gallery and the My Gifts page.

![Alt text](/hackathon/img/new_gift.png)

![Alt text](/hackathon/img/my_gifts.png)

Search
-------------
Our search function enables you to look for exactly what you need.

Have a specific category in mind? Let's say... Electronics?

![Alt text](/hackathon/img/search_elec.png)

What if you want a gift around $15? Give or take a few bucks. 

![Alt text](/hackathon/img/search_price.png)

giftr.
-------------
![Alt text](/hackathon/img/capital-one-logo.png)
