
_.templateSettings = interpolate: /\{\{(.+?)\}\}/


colour_map = _.memoize (name) ->
  hash = 360
  mash = (char) ->
    # sdbm
    n = char.charCodeAt 0
    hash = n + (hash << 6) + (hash << 16) - hash
  mash char for char in name
  $.husl.p.toHex (hash % 360), 100, 58


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

  template: _.template $('#task-template').html()

  events:
    'click .task-edit': 'edit'
    'click .task-remove': 'clear'
    'click .task-update': 'close'

  initialize: () ->
    this.listenTo this.model, 'change', this.render
    this.listenTo this.model, 'destroy', this.remove

  render: () ->
    nice_attributes = _.clone(this.model.attributes)
    nice_attributes.duration /= 60
    this.$el.html this.template nice_attributes
    project_colour = colour_map nice_attributes.project.name
    $('.task-project', this.el).css color: project_colour
    $(':hover', )
    return this

  edit: () ->
    this.$el.addClass 'editing'
    this.$('.task-thing').attr('contenteditable', 'true')
    this.$('.task-description').focus()

  close: () ->
    this.model.save
      date: this.$('.task-date').text()
      description: this.$('.task-description').text()
      duration: this.$('.task-duration').text() * 60
      project:
        name: this.$('.task-project').text()
    this.$el.removeClass 'editing'
    this.$('.task-thing').attr('contenteditable', 'false')

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
      duration: this.new_form.duration.val() * 60
      description: this.new_form.description.val()
      date: this.new_form.date.val()
      project:
        name: this.new_form.project.val()
    _(this.new_form).each (thing) ->
      thing.val ''



App = new AppView

