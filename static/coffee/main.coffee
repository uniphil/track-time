
_.templateSettings = interpolate: /\{\{(.+?)\}\}/


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


TaskList = Backbone.Collection.extend
  model: TaskModel
  url: '/tasks/'
  parse: (data) -> data.tasks


TaskInputView = Backbone.View.extend
  el: $ '.tasks-new'
  initialize: () -> this.render()
  render: () ->
    template = _.template(
      '<label for="duration">duration</label>
      <input type="number" name="duration" id="duration" />
      <label for="description">description</label>
      <input type="text" name="description" id="description"/>
      <label for="project">project</label>
      <input type="text" name="project" id="project" />
      <label for="date">date</label>
      <input type="date" name="date" id="date" />
      <button type="submit">save</button>')
    this.$el.html template this.model.attributes
  events:
    'click button[type=submit]': 'addTask'
  addTask: () ->
    new_task = new TaskModel
      duration: $('.duration', this.el).val()
      description: $('.description', this.el).val()
      project: $('.project', this.el).val()
      date: $('.date', this.el).val()
    new_task.save success: () ->
      task_list.add new_task
    console.log task_list


TaskListedView = Backbone.View.extend
  initialize: () -> this.render()
  render: () ->
    template = _.template(
      '<li>' +
        '<span class="task-duration">{{ duration }}</span>' +
        '<span class="task-description">{{ description }}</span>' +
        '<a class="task-project" href="#{{ project.ref }}">' +
          '{{ project.name }}' +
        '</a>' +
        '<a class="task-remove" href="#remove-task">' +
          '&times;' +
        '</a>' +
      '</li>')
    this.$el.html template this.model.attributes


task_list = new TaskList()


task_input_view = new TaskInputView model: TaskModel

task_list.fetch()


#taskview = new TaskView model: task


# modelview.render()
# blah = $('h1').html modelview.el
