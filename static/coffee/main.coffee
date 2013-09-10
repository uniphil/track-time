
_.templateSettings = interpolate: /\{\{(.+?)\}\}/

task_edit_template = '' +
  '<label for="duration">duration</label>
  <input type="number" name="duration" id="duration" />
  <label for="description">description</label>
  <input type="text" name="description" id="description"/>
  <label for="project">project</label>
  <input type="text" name="project" id="project" />
  <label for="date">date</label>
  <input type="date" name="date" id="date" />
  <button type="submit">save</button>'

task_display_template = '' +
  '<span class="task-duration">{{ duration }}</span>' +
  '<span class="task-description">{{ description }}</span>' +
  '<a class="task-project" href="#{{ project.href }}">' +
    '{{ project.name }}' +
  '</a>' +
  '<a class="task-edit" href="#edit-task">e</a>' +
  '<a class="task-remove" href="#remove-task">&times;</a>'


TaskModel = Backbone.Model.extend
  urlRoot: '/tasks/'
  url: () -> this.id or this.urlRoot
  idAttribute: 'href'
  defaults:
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
  model: TaskModel
  url: '/tasks/'
  parse: (data) -> data.tasks


TaskView = Backbone.View.extend
  tagName: 'li'
  initialize: () ->
    _.bindAll this, 'render', 'removeTask'
    this.render()
  events:
    'click a[href="#remove-task"]': 'removeTask'
  removeTask: () ->
    this.model.destroy()
  render: (edit) ->
    template_str = if edit? then task_edit_template else task_display_template
    compiled = _.template template_str
    rendered = compiled this.model.attributes
    this.$el.html rendered


TaskListView = Backbone.View.extend
  tagName: 'ul'
  initialize: () ->
    _.bindAll this, 'render', 'taskRemoved'
    this.collection = new TaskList()
    this.collection.bind 'destroy', this.taskRemoved
    this.collection.fetch success: this.render
  taskRemoved: () ->
    console.log 'task removed?'
    this.render()
  render: () ->
    this.$el.empty()
    self = this
    this.collection.each (task) ->
      view = new TaskView model: task
      self.$el.append view.el


TaskEditView = Backbone.View.extend
  tagName: 'div'
  task: null
  initialize: () ->
    _.bindAll this, 'render', 'addTask'
    this.task_view = new TaskView model: new TaskModel()
    this.render()
  events:
    'click button[type=submit]': 'addTask'
  addTask: () ->
    new_task = new TaskModel
      duration: $('#duration', this.el).val()
      description: $('#description', this.el).val()
      project:
        name: $('#project', this.el).val()
      date: $('#date', this.el).val()
    new_task.save()
    this.old_list.collection.add new_task, at: 0
    this.old_list.render()
  render: () ->
    this.task_view.render(true)
    this.$el.html this.task_view.$el


task_list_view = new TaskListView el: $('.tasks-old ul')
task_edit_view = new TaskEditView el: $('.tasks-new')
task_edit_view.old_list = task_list_view
