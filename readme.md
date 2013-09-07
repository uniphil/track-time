personal projet-based time tracking

deploys to heroku or dokku


## API

### GET /tasks/

get a list of all tasks

#### Parameters

todo: implement paging (and filtering?)

#### Returns

200 ok

```json
[
  {
    "ref": "uri for this task",
    "recorded": "timestamp",
    "date": "iso date",
    "duration": "time in seconds",
    "description": "string",
    "project": {
      "name": "string",
      "ref": "uri for the project"
    }
  },
  ...
]
```


### POST /tasks/

create a new task

#### Parameters

  * *description*: a string (required)
  * *duration*: the duration of the task in seconds (required)
  * *project*: string (optional)
  * *date*: the iso date of the task (optional)

#### Returns

303 see other (redirects to the new resource)


### GET /tasks/<id>

get task details

#### Parameters

none

#### Returns

404 not found or 200 ok:

```json
{
  "ref": "uri for this task",
  "recorded": "timestamp",
  "date": "iso date",
  "duration": "time in seconds",
  "description": "string",
  "project": {
    "name": "string",
    "ref": "uri for the project"
  }
}
```


### PUT /tasks/<id>

update a task

#### Parameters

  * *description*: a string (required)
  * *duration*: the duration of the task in seconds (required)
  * *project*: string (required, can be blank)

#### Returns

200 ok
```json
{
  "ref": "uri for this task",
  "recorded": "timestamp",
  "date": "iso date",
  "duration": "time in seconds",
  "description": "string",
  "project": {
    "name": "string",
    "ref": "uri for the project"
  }
}
```


### PATCH /tasks/<id>

update part of a task

#### Parameters

  * *(replace|add|remove)*: field key as string (required)
  * *value*: the new value (required)

note: `add` and `remove` are only valid for the "project" key.

#### Returns

200 ok
```json
{
  "ref": "uri for this task",
  "recorded": "timestamp",
  "date": "iso date",
  "duration": "time in seconds",
  "description": "string",
  "project": {
    "name": "string",
    "ref": "uri for the project"
  }
}
```


### DELETE /tasks/<id>

delete a task

#### Parameters

none

#### Returns

204 no content



