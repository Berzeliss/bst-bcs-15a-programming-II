this is a repository for a class project collaboration

link to project [roadmap](https://docs.google.com/document/d/1XfyqtyQKthp5_TZCjpjYPQPwJAK3oOlOEh34YXNZkPA/edit?tab=t.0) 

@Vinnie
#### Note:
- all media files moved to static, reference them in html via ```{% static '{relative path}' %}```

  e.g. ```"{% static 'images/history-image.webp' %}"```

- To reference data from the backend, follow these steps:

  *A. for links redirecting to another template:*
  1. go to ```views.py```
  2. check which function is rendering the target html
  3. check the function's parameter
  4. call via ```<a href="{% url '{function_name}' '{parameter}' %}">```
  e.g.
  ```
  index.html:
  
  <div class="card">
    <a href="{% url 'quiz_list' 'History' %}">
        <img src="{% static 'images/history-image.webp' %}" alt="History Quiz">
        <h3>History Quiz</h3>
    </a>
  </div>
  ```
  ```
  views.py:
  
  def quiz_list(request, category):
    context = {'quizzes': Quiz.objects.filter(category=category)}
    return render(request, 'quiz_list.html', context)
  ```
  In this example, ```def quiz_list(request, category)``` is the function to ```quiz_list.html```, and requires the parameter ```category```. So we call it in the ```index.html``` by ```<a href="{% url 'quiz_list' 'History' %}">```


  *B. to extract variables from backend:*
  1. go to ```views.py```
  2. check which function is rendering the target html
  3. check the function's ```context```, which is a dictionary
  4. extract the values like how we normally fo in a dicionary, i.e., ```{{ {key}.{value} }]```

     for reference, check ```quiz.html``` and ```def quiz()``` in ```views.py```
