# Lea Record Shop

This project implements a REST API application for a small disc ecommerce, in the project is possible to manage users, products and orders (requests).

The project is implemented using Django Framework with Python 3.9. We decide to use a Postgres database together with project, because it's easier to use together with Django and also a relational DB is more appropriate to project's needs. We also use Docker to make it easier to deploy and also for tests on local environment.

One of the main reasons to choose Docker is the fact that I believe we could use Amazon Elastic Container Service to deploy the application for production, use ECS would be a good fit for problem requirements, since it's easy to deploy and also very easy to scale, adding more tasks (or removing them) when necessary. ECS also allows to control the number of available tasks based on access volumes and predetermined conditions.

Also, a good point to be made is about how we deal with race conditions at our system. In order to prevent to sell users an amount of disc's that will not be able to be delivered we added a `lock` strategy to deal with database updates for the `Disc` model, basically, every time a request order is being created, first thread will acquire a lock of the Dict table, which means that no other thread will be able to manage that disc entry. So we will never have more than one thread updating same disc at same time, as desired to solve our problem. In the case describe at the problem for Hohpe new disc, the other 2500 clients will not be able to buy the disc. 

## Installation

In order to use the project `docker-compose` is probably going to be enough to execute the project. It might be necessary to install the projects dependencies before execute it, what can be done with following command:

```bash
pip install -r requirements.txt
```

One of the used libs, `psycopg2`, might give some problems to install if you don't have a local Postgres installation.

## Usage

After install the dependencies, you can use following commands to execute the Docker instance at your local environment:
1. Build dockerfile : `docker-compose build`
2. Make system up: `docker-compose up`
3. Make system down: `docker-compose down`

You also might wanna create a super used (with administrator access) to use native admin console, which can be done with:
```bash
docker-compose run --rm app python manage.py createsuperuser
```

### Postman Requests
A sample of the possible requests for the system are presented at `record-shop.postman_collection.json` file and can be imported at Postman for local usage.

Now I'm giving a simple explication for the `GET` requests, Django allows to create the requests very simple based on the parameters informed through the request body, for example, if you want to filter product's for a specific client you can make:

```json
{
  "client": "<client_id>"
}
```

If you want the request to be based on a list of client's, you just have to make:
```json
{
  "client__in": "<client_id>"
}
```

Now, if we look for the Disc's only, if you want to filter based on all parameters, just make:
```json
{
  "name": "<name>",
  "artist": "<artist>",
  "release_year": "<release_year>",
  "style": "<style>"
}
```

If you don't want to use any of the parameters just remove it from the request body. Finally, last thing that's important to be informed, you can use comparison parameters to the request by adding expressions like:
1. Values greater or equal: `__gte`
2. Values less or equal: `__lte`
3. Values in list: `__in`


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
