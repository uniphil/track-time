
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
    full.project = this.get('project').name
    if full.date
      full.date = this.get('date').toISOString()
    return full


TaskList = Backbone.Collection.extend

  model: Task

  url: '/tasks/'
  parse: (data) ->
    tasks = data.tasks
    _(tasks).each (thing) ->
      thing.date = new Date(thing.date)
      thing.recorded = new Date(thing.recorded)
    return tasks

  comparator: (a, b) ->
    a_date = a.get('date').getTime()
    b_date = b.get('date').getTime()
    if a_date > b_date
      return -1
    else if a_date < b_date
      return 1
    else
      a_recorded = a.get('recorded').getTime()
      b_recorded = b.get('recorded').getTime()
      if a_recorded > b_recorded then -1 else 1

  project: (name) ->
    this.filter (task) -> task.get('project').name == name


TaskView = Backbone.View.extend

  tagName: 'li'

  template: _.template $('#task-template').html()

  events:
    'click .task-edit': 'edit'
    'click .task-remove': 'clear'
    'click .task-update': 'close'
    'click .task-project': 'filter'

  initialize: () ->
    this.listenTo this.model, 'change', this.render
    this.listenTo this.model, 'destroy', this.remove

  render: () ->
    nice_attributes = _.clone(this.model.attributes)
    nice_attributes.duration /= 60
    this.$el.html this.template nice_attributes
    project_colour = colour_map nice_attributes.project.name
    $('.task-project', this.el).css color: project_colour
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

  filter: () ->
    App.filter_project this.model.get('project').name


AppView = Backbone.View.extend

  el: $('#trackerapp')

  events:
    'click #save-new-task': 'save_new'
    'keypress form': 'save_on_enter'
    'click .filter-projects': 'unfilter'

  initialize: () ->
    _.bindAll this, 'show_task', 'show_task_list', 'filter_project', 'render'
    this.collection = new TaskList
    this.collection.bind 'sort', this.show_task_list
    this.collection.bind 'remove', this.render
    this.collection.bind 'change:duration', this.render

    this.project_filter = null

    this.new_form =
      duration: this.$("#new-duration")
      description: this.$("#new-description")
      date: this.$("#new-date")
      project: this.$("#new-project")

    this.collection.fetch()

  render: () ->
    if this.project_filter == null
      tasks = this.collection
    else
      tasks = _ this.collection.project this.project_filter
    duration = tasks.reduce ((m, v) -> m + v.attributes.duration), 0
    $('.stats-minutes', this.el).text duration / 60

  show_task: (task) ->
    view = new TaskView model: task
    this.$("#task-list").append view.render().el
    this.render()

  show_task_list: () ->
    if this.project_filter == null
      tasks = this.collection
    else
      tasks = _ this.collection.project this.project_filter
    this.$('#task-list').html ''
    tasks.each this.show_task, this

  save_on_enter: (e) ->
    if e.keyCode == 13
      this.save_new()
      $('#new-duration', this.el).focus()

  save_new: () ->
    this.collection.create
      duration: this.new_form.duration.val() * 60
      description: this.new_form.description.val()
      date: this.new_form.date.val()
      project:
        name: this.new_form.project.val()
    _(this.new_form).each (thing) ->
      thing.val ''

  filter_project: (name) ->
    this.project_filter = name
    this.$('.filter-projects').text name
    this.show_task_list()

  unfilter: () ->
    this.project_filter = null
    this.$('.filter-projects').text 'everything'
    this.show_task_list()


window.App = new AppView

