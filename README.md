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
Hey wants to *reward* your attention without *monopolizing* it.
You care for your relationships, and then you leave.
There's no content to consume.

## Why not Monica?
To be honest, I haven't used Monica yet!
But I hear great things from friends, and I'd 100% recommend it over Hey in its current state.

I'm building Hey because it's a tool I've wanted for a long time,
and I also wanted an excuse to learn Django and a bit of front-end development.
So I'm taking [some good advice](https://mitchellh.com/writing/building-large-technical-projects#build-for-yourself)
to focus on building things that I personally use.

## Setup
Get the goods:

```bash
git clone https://github.com/eenblam/hey
cd hey
```

### With Poetry+Poe
You'll need a system install of Poetry.

[Poe](https://poethepoet.natn.io/poetry_plugin.html) is installed as a dev dependency
for local development.

```bash
poetry install --sync  # Install current poetry.lock
poetry shell           # Get a shell
poe setup              # Create superuser
poe migrate            # Run database migrations
poe static             # Generate static assets, like Django admin UI
poe test               # Run tests
poe coverage           # See test coverage info
poe run                # Start local server in foreground
```

### With Docker
If you already have a `hey.sqlite3` database from running without a container, then you just need `docker compose up`.

Otherwise, you'll need to jump through a few initial hoops to create the database within Docker:

* Comment out the `volumes` section of `docker-compose.yml`.
* `docker compose up` to start; this will create your DB file
* `docker compose exec hey /bin/bash`
* `poetry shell`
    * (Dev dependencies aren't installed in the image, so no Poe commands.)
    * `./manage.py migrate`
    * `./manage.py createsuperuser`
* Exit the container
* Get the container name (e.g. hey-hey-1) via `docker compose ps`
* `docker cp hey-hey-1:/app/hey.sqlite3 hey.sqlite3`
* Un-comment the `volumes` section of `docker-compose.yml` and restart the composition.
