this is a repository for a class project collaboration

link to project [roadmap](https://docs.google.com/document/d/1XfyqtyQKthp5_TZCjpjYPQPwJAK3oOlOEh34YXNZkPA/edit?tab=t.0) 

@Vinnie
#### Note:
- all media files moved to static, reference them in html via ```{% static '{relative path}' %}```

  e.g. ```"{% static 'images/history-image.webp' %}"```

- To reference data from the backend, follow these steps:

  *for links:*
  1. go to ```views.py```
  2. check which function is rendering the target html
  3. check the function's parameter
  4. call via ```<a href="{% url '{function_name}' '{parameter}' %}">```
  e.g.
  
  https://github.com/TinWanNg/bst-bcs-15a-programming-II/blob/fbec134aef63fb9f29875fab2c68c5dad594bdc9/class_project/quiz_app/templates/index.html#L29C13-L34C19

  https://github.com/TinWanNg/bst-bcs-15a-programming-II/blob/fbec134aef63fb9f29875fab2c68c5dad594bdc9/class_project/quiz_app/views.py#L11C1-L13C54

  In this example, ```def quiz_list(request, category)``` is the function to ```quiz_list.html```, and requires the parameter ```category```. So we call it in the ```index.html``` by ```<a href="{% url 'quiz_list' 'History' %}">```
