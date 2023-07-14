# hey

Hey is a personal relationship manager,
kinda like [Monica](https://github.com/monicahq/monica).

## What is it?
Whereas Monica is a rather full-featured CRM,
Hey is meant to be a simple and tight tool for staying in touch with the people I care about.
I'm sure I'll add more over time,
but for now my main focus is on features related to contact frequency.

## Who is it for?
It's for me, and maybe some friends who also don't use Facebook.

I don't use Facebook for a variety of reasons: privacy, company ethics, demands on my attention, etc.
However, it also does a lot for people as a product:

* Remind you of birthdays
* Suggest friends to reach out to
* Provide information about your friends: employer, partner's name, last name, etc. that can be nice to remember

Hey is meant to fill these gaps, respectfully.
Hey wants to *get* your attention without *monopolizing* it.
You manage your relationships, and then you leave.
There's no content to consume.

## Why not Monica?
To be honest, I haven't used Monica yet!
But I hear great things from friends, and I'd 100% recommend it over Hey in its current state.

I'm building Hey because it's a tool I've wanted for a long time,
and I also wanted an excuse to learn Django and a bit of front-end development.
So I'm taking [some good advice](https://mitchellh.com/writing/building-large-technical-projects#build-for-yourself)
to focus on building things that I personally use.

## Setup

```bash
git clone https://github.com/eenblam/hey
cd hey
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
# Set up your database
./manage.py migrate
# This is on your path after installing, as long as the venv is active
django-admin createsuperuser
# Bundle up static assets into static/
# For example, the Django admin UI.
# I haven't vendored that as a dependency, since I'm not sure how I'll license yet.
./manage.py collectstatic 
```

Now, you can just start the app with `./manage.py runserver`.
