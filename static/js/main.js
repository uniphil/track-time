// Generated by CoffeeScript 1.6.3
(function() {
  var AppView, Task, TaskList, TaskView, colour_map;

  _.templateSettings = {
    interpolate: /\{\{(.+?)\}\}/
  };

  colour_map = _.memoize(function(name) {
    var char, hash, mash, _i, _len;
    hash = 360;
    mash = function(char) {
      var n;
      n = char.charCodeAt(0);
      return hash = n + (hash << 6) + (hash << 16) - hash;
    };
    for (_i = 0, _len = name.length; _i < _len; _i++) {
      char = name[_i];
      mash(char);
    }
    return $.husl.p.toHex(hash % 360, 100, 58);
  });

  Task = Backbone.Model.extend({
    urlRoot: '/tasks/',
    url: function() {
      return this.id || this.urlRoot;
    },
    idAttribute: 'href',
    defaults: function() {
      return {
        date: new Date(),
        description: '',
        duration: 0,
        project: {
          name: ''
        }
      };
    },
    toJSON: function() {
      var full;
      full = _.clone(this.attributes);
      full.project = this.get('project').name;
      if (full.date) {
        full.date = this.get('date').toISOString();
      }
      return full;
    }
  });

  TaskList = Backbone.Collection.extend({
    model: Task,
    url: '/tasks/',
    parse: function(data) {
      var tasks;
      tasks = data.tasks;
      _(tasks).each(function(thing) {
        thing.date = new Date(thing.date);
        return thing.recorded = new Date(thing.recorded);
      });
      return tasks;
    },
    comparator: function(a, b) {
      var a_date, a_recorded, b_date, b_recorded;
      a_date = a.get('date').getTime();
      b_date = b.get('date').getTime();
      if (a_date > b_date) {
        return -1;
      } else if (a_date < b_date) {
        return 1;
      } else {
        a_recorded = a.get('recorded').getTime();
        b_recorded = b.get('recorded').getTime();
        if (a_recorded > b_recorded) {
          return -1;
        } else {
          return 1;
        }
      }
    },
    project: function(name) {
      return this.filter(function(task) {
        return task.get('project').name === name;
      });
    }
  });

  TaskView = Backbone.View.extend({
    tagName: 'li',
    template: _.template($('#task-template').html()),
    events: {
      'click .task-edit': 'edit',
      'click .task-remove': 'clear',
      'click .task-update': 'close',
      'click .task-project': 'filter'
    },
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      return this.listenTo(this.model, 'destroy', this.remove);
    },
    render: function() {
      var nice_attributes, project_colour;
      nice_attributes = _.clone(this.model.attributes);
      nice_attributes.duration /= 60;
      this.$el.html(this.template(nice_attributes));
      project_colour = colour_map(nice_attributes.project.name);
      $('.task-project', this.el).css({
        color: project_colour
      });
      return this;
    },
    edit: function() {
      this.$el.addClass('editing');
      this.$('.task-thing').attr('contenteditable', 'true');
      return this.$('.task-description').focus();
    },
    close: function() {
      this.model.save({
        date: this.$('.task-date').text(),
        description: this.$('.task-description').text(),
        duration: this.$('.task-duration').text() * 60,
        project: {
          name: this.$('.task-project').text()
        }
      });
      this.$el.removeClass('editing');
      return this.$('.task-thing').attr('contenteditable', 'false');
    },
    clear: function() {
      return this.model.destroy();
    },
    filter: function() {
      return App.filter_project(this.model.get('project').name);
    }
  });

  AppView = Backbone.View.extend({
    el: $('#trackerapp'),
    events: {
      'click #save-new-task': 'save_new',
      'keypress form': 'save_on_enter',
      'click .filter-projects': 'unfilter'
    },
    initialize: function() {
      _.bindAll(this, 'show_task', 'show_task_list', 'filter_project', 'render');
      this.collection = new TaskList;
      this.collection.bind('sort', this.show_task_list);
      this.collection.bind('remove', this.render);
      this.collection.bind('change:duration', this.render);
      this.project_filter = null;
      this.new_form = {
        duration: this.$("#new-duration"),
        description: this.$("#new-description"),
        date: this.$("#new-date"),
        project: this.$("#new-project")
      };
      return this.collection.fetch();
    },
    render: function() {
      var duration, tasks;
      if (this.project_filter === null) {
        tasks = this.collection;
      } else {
        tasks = _(this.collection.project(this.project_filter));
      }
      duration = tasks.reduce((function(m, v) {
        return m + v.attributes.duration;
      }), 0);
      return $('.stats-minutes', this.el).text(duration / 60);
    },
    show_task: function(task) {
      var view;
      view = new TaskView({
        model: task
      });
      this.$("#task-list").append(view.render().el);
      return this.render();
    },
    show_task_list: function() {
      var tasks;
      if (this.project_filter === null) {
        tasks = this.collection;
      } else {
        tasks = _(this.collection.project(this.project_filter));
      }
      this.$('#task-list').html('');
      return tasks.each(this.show_task, this);
    },
    save_on_enter: function(e) {
      if (e.keyCode === 13) {
        this.save_new();
        return $('#new-duration', this.el).focus();
      }
    },
    save_new: function() {
      this.collection.create({
        duration: this.new_form.duration.val() * 60,
        description: this.new_form.description.val(),
        date: this.new_form.date.val(),
        project: {
          name: this.new_form.project.val()
        }
      });
      return _(this.new_form).each(function(thing) {
        return thing.val('');
      });
    },
    filter_project: function(name) {
      this.project_filter = name;
      this.$('.filter-projects').text(name);
      return this.show_task_list();
    },
    unfilter: function() {
      this.project_filter = null;
      this.$('.filter-projects').text('everything');
      return this.show_task_list();
    }
  });

  window.App = new AppView;

}).call(this);
