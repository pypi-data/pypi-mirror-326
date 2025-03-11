# DEVELOP WITH POETRY

Install `poetry`. Then
```bash
poetry install
poetry run python manage.py migrate
```

To start the local server:
```bash
poetry run python manage.py runserver
```

# DEPLOY WITH DOCKER

Build:

    docker-compose build

Create superuser or change password:

    docker-compose run web ./manage.py createsuperuser
    docker-compose run web ./manage.py changepassword <username>

Run:

    docker-compose up

# INSTALL PIPRINTS

Install `poetry` then
```
poetry install
```

Customize your instance by setting environment variables 
in `.env`
```
copy .env.example .env
```

*IMPORTANT:* change the `SECRET_KEY` to some other random and secret
value. If anyone knows the secret_key you are using (maybe because you
are using the default), then they are able to log in your site as any
user (including administrators)!

At last execute
```
    poetry run python manage.py collectstatic
```
to collect all static files in a single directory,
```
    poetry run python manage.py migrate
```
to initialize the database and
```
    poetry run python manage.py createsuperuser
```
to create a superuser in the database.

You can start a development server with:
```
poetry run python manage.py runserver
```

When using in production, use the provided WSGI script (you can
configure the virtualenv to use in config.ini).

Once you have a running webserver, you can access the /admin/ page to
configure everything else.

From the /admin/ interface you must create a SiteParameters object to extend
the default Site object (initially called example.com).

You can create new users by filing a user request from the /request/ page
then manage the request (with admin credentials) from the /person_requests/ page.

You can change a user's password with the command
```
    poetry run python manage.py changepassword <username>
```

# DEVELOPMENT SERVER

Per provare il codice develop bisogna dare questi comandi (bisogna avere accesso a cvgmt@cvgmt.sns.it):

    ssh -L 8080:localhost:8080 cvgmt@cvgmt.sns.it
    ./piprints_develop/manage.py runserver 8080

a quel punto si può aprire la pagina tramite un tunnel in locale:

    http://localhost:8080

e si dovrebbe vedere un clone di cvgmt (database clonato, documenti clonati) su cui si possono fare tutte le prove che volete. Premere ctrl-C per fermare il server e ctrl-D per chiudere il tunnel.

# BACKUP

Per fare un dump del database il comando che sembra funzionare e' questo:

da un lato:

    python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission --exclude=admin -o mydump.json

dall'altro lato:
    
    python manage.py flush   ## cancella il database!!
    python manage.py loaddata mydump.json



