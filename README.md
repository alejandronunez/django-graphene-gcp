# django-graphene-gcp

To test functionality implemented in `https://github.com/graphql-python/graphene-django/pull/666` 

### dependency:
- `docker`
- `docker-compose`

### Step to start:
- `docker-compose up` to start the containers
- `docker exec -it django-graphene-gcp-api python manage.py loaddata categories ads` to load fixture data
- go to `http://localhost:8008/dev/` to access to Graphiql.
- your first query:
```
{
  esAds(
    subcategoryName:"Casas", 
    sort:{order:desc, field:price}, 
    first:2, 
    priceGte:1000
  ){
    edges{
      node{
        title
        description
        price
        name
        email
        phone
        subcategory{
          name
          id
        }
      }
    }
  }
}
```

### Explore
This [file](https://github.com/alejandronunez/django-graphene-gcp/blob/graphene-elasticsearch/app/ads/filters.py) has the work with the filters
