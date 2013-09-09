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



### GET /projects/

get a list of all projects

#### Parameters

todo: implement paging (and filtering?)

#### Returns

200 ok

```json
[
  {
    "name": "string",
    "ref": "uri for the project",
    "started": "iso date",
    "total": "total time on project in seconds"
  },
  ...
]
```


### POST /projects/

create a new project

#### Parameters

  * *name*: a string (required)

#### Returns

303 see other (redirects to the new resource)


### GET /projects/<id>

get project details

#### Parameters

none

#### Returns

200 ok

```json
{
  "name": "string",
  "ref": "uri for the project",
  "started": "iso date",
  "total": "total time on project in seconds"
  "tasks": [
    {
      "ref": "uri to the task",
      "date": "iso date",
      "duration": "duration of the task in seconds",
      "description": "string"
    },
    ...
  ]
}
```


### PUT /projects/<id>

update a project

#### Parameters

  * *name*: a string (required)

#### Returns

200 ok
```json
{
  "name": "string",
  "ref": "uri for the project",
  "started": "iso date",
  "total": "total time on project in seconds"
  "tasks": [
    {
      "ref": "uri to the task",
      "date": "iso date",
      "duration": "duration of the task in seconds",
      "description": "string"
    },
    ...
  ]
}
```


### PATCH /projects/<id>

update part of a task -- redundant with PUT since there is only the `name`.

#### Parameters

  * *replace*: "name" (required)
  * *value*: the new name (required)

note: `add` and `remove` are only valid for the "project" key.

#### Returns

200 ok
```json
{
  "name": "string",
  "ref": "uri for the project",
  "started": "iso date",
  "total": "total time on project in seconds"
  "tasks": [
    {
      "ref": "uri to the task",
      "date": "iso date",
      "duration": "duration of the task in seconds",
      "description": "string"
    },
    ...
  ]
}
```


### DELETE /projects/<id>

delete a project. tasks with this project will have an empty project.

#### Parameters

none

#### Returns

204 no content


## Futures

### Data

Maybe add tags?
