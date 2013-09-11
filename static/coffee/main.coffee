
_.templateSettings = interpolate: /\{\{(.+?)\}\}/

task_template = '' +
  '<span class="task-duration">{{ duration }}</span>' +
  '<span class="task-description">{{ description }}</span>' +
  '<a class="task-project" href="#{{ project.href }}">' +
    '{{ project.name }}' +
  '</a>' +
  '<a class="task-edit" href="#edit-task">e</a>' +
  '<a class="task-remove" href="#remove-task">&times;</a>'


Task = Backbone.Model.extend

  urlRoot: '/tasks/'
  url: () -> this.id or this.urlRoot
  idAttribute: 'href'

  defaults: () ->
    date: new Date()
    description: ''
    duration: 0
    project:
      name: ''

  toJSON: () ->
    full = _.clone(this.attributes);
    full.project = full.project.name
    return full


TaskList = Backbone.Collection.extend

  model: Task

  url: '/tasks/'
  parse: (data) -> data.tasks

  comparator: 'date'


Tasks = new TaskList


TaskView = Backbone.View.extend

  tagName: 'li'

  template: _.template(task_template)

  events:
    'click .task-edit': 'edit'
    'click .task-remove': 'clear'
    'click .task-save': 'close'

  initialize: () ->
    this.listenTo this.model, 'change', this.render
    this.listenTo this.model, 'destroy', this.remove

  render: () ->
    this.$el.html this.template this.model.attributes
    return this

  edit: () ->
    this.$el.addClass 'editing'
    this.$('.task-description').focus()

  close: () ->
    this.model.save
      date: this.$('.task-date').text()
      description: this.$('.task-description').text()
      duration: this.$('.task-duration').text()
      project:
        name: this.$('.task-project').text()

  clear: () ->
    this.model.destroy()


AppView = Backbone.View.extend

  el: $('#trackerapp')

  events:
    'click #save-new-task': 'save_new'

  initialize: () ->
    this.new_form =
      duration: this.$("#new-duration")
      description: this.$("#new-description")
      date: this.$("#new-date")
      project: this.$("#new-project")

    this.listenTo Tasks, 'add', this.add_one
    this.listenTo Tasks, 'reset', this.add_all
    this.listenTo Tasks, 'all', this.render

    this.main = $("#main")

    Tasks.fetch()

  render: () ->
    if Tasks.length
      this.main.show()
    else
      this.main.hide()

  add_one: (task) ->
    view = new TaskView model: task
    this.$("#task-list").append view.render().el

  add_all: () ->
    Tasks.each this.add_one, this

  save_new: () ->
    Tasks.create
      duration: this.new_form.duration.val()
      description: this.new_form.description.val()
      date: this.new_form.date.val()
      project:
        name: this.new_form.project.val()


App = new AppView

