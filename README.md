# Cooloc

Cooloc is a website made to simplify a flatshare. I made this website to obtain the **RNCP 37873** : "Concepteur Developpeur d'Applications".

This is the v2 of the project, the v1 (2024) is in the [legacy branch](https://github.com/mathieu-personal-projects/Cooloc/tree/legacy).

There is deeper (and older) documentation in the `docs/` folder.

## Configuration

Create at root a `.docker/` folder. In this folder you will then need to create 2 folders and a file : 
```bash
mkdir -p .docker/db-data && mkdir -p .docker/pgadmin-data
touch .docker/.env
```

And then in the .env paste these values (that you will edit obv) : 
```ini
POSTGRES_USER=you
POSTGRES_PASSWORD=your-pg-passwd
POSTGRES_DB=cooloc
PGADMIN_DEFAULT_EMAIL=you@your-mail.com
PGADMIN_DEFAULT_PASSWORD=your-pgad-passwd
```

Once created you can run `docker compose up -d` to start containers.

When creating the PostgreSQL database, you can see the initialisation file @ docs/v2/db/init.sql.

## Contact

mathieu.audibert@proton.me