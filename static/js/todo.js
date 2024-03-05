// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 0; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
  close[i].onclick = function() {
    var div = this.parentElement;
    div.style.display = "none";
  }
}

// Create a new list item when clicking on the "Add" button
function newElement() {
  var li = document.createElement("li");
  var inputValue = document.getElementById("myInput").value;
  var t = document.createTextNode(inputValue);
  li.appendChild(t);
  if (inputValue === '') {
    alert("You must write something!");
  } else {
    li.classList.add("draggable");
    li.setAttribute("draggable", "true");
    document.getElementById("myUL").appendChild(li); 
   
    // Get the selected course from the dropdown
    var selectedCourseId = document.getElementById("courseSelect").value;

    // Add the new task to the server
    fetch('/add_task', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'title': inputValue,
        'is_done': 'false',
        'course_id': selectedCourseId,
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Task added successfully:', data);
        li.dataset.taskId = data.task_id;
        li.dataset.taskDone = 'false';
    })
      .catch(error => {
        console.error('Error adding task:', error);
      });
    }
  document.getElementById("myInput").value = "";

  // Inside the newElement function
  var closeBtn = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  closeBtn.className = "close";
  closeBtn.appendChild(txt);
  li.appendChild(closeBtn);

  closeBtn.onclick = function () {
    var div = this.parentElement;
    div.style.display = "none";
    var taskId = div.dataset.taskId;
    removeTask(taskId);
  };
}

// Fetch tasks
fetch('/tasks')
  .then(response => response.json())
  .then(data => {
    if (Array.isArray(data) && data.length > 0) {
      // Iterate over tasks
      for (var task of data) {
        // Create a new task item
        var taskItem = document.createElement("li");
        var taskTitle = document.createTextNode(task.title);
        taskItem.appendChild(taskTitle);
        taskItem.dataset.taskId = task.id; // Set the unique ID
        taskItem.dataset.taskDone = task.is_done; // Set the checked state
        document.getElementById("myUL").appendChild(taskItem); 

        // Create a "close" button and append it to the task item
        var span = document.createElement("SPAN");
        var txt = document.createTextNode("\u00D7");
        span.className = "close";
        span.appendChild(txt);
        taskItem.appendChild(span);
        
        // Cross off done tasks
        console.log(task.is_done);
        if (task.is_done === true) {
          taskItem.classList.toggle('checked');
        }

        // Attach a click event to the close button for removal
        span.onclick = function() {
          var taskId = this.parentElement.dataset.taskId;
          removeTask(taskId);
        };

      }
      console.log('Tasks fetched successfully.')
    } else {
      console.log("No tasks to add to container.");
    }
  })
  .catch(error => {
    console.error('Error fetching courses:', error);
});

// Update the task status when clicking on a task
var list = document.querySelector('ul');
list.addEventListener('click', function (ev) {
  if (ev.target.tagName === 'LI') {
    ev.target.classList.toggle('checked');
    var taskId = ev.target.dataset.taskId;
    var isDone = ev.target.classList.contains('checked') ? 'true' : 'false';
    updateTaskStatus(taskId, isDone);
  }
}, false);

// Update the task status when clicking on a task
function updateTaskStatus(taskId, isDone, taskElement) {
  fetch('/update_task_status/' + taskId, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      'is_done': isDone,
    }),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Task status updated successfully:', data);
      taskElement.dataset.taskDone = isDone;
    })
    .catch(error => {
      console.error('Error updating task status:', error);
    });
}
  
// Function to remove a task
function removeTask(taskId) {
  // Remove the task from the server
  fetch('/remove_task/' + taskId, {
    method: 'DELETE',
  })
    .then(response => response.json())
    .then(data => {
      console.log('Task removed successfully:', data);
    })
    .catch(error => {
      console.error('Error removing task:', error);
    });

  // Remove the task from the UI
  var taskItem = document.querySelector('li[data-task-id="' + taskId + '"]');
  if (taskItem) {
    taskItem.remove();
  }
}

// Make list items draggable
var ul = document.getElementById("myUL");
var draggableItems = ul.getElementsByTagName("li");
for (var i = 0; i < draggableItems.length; i++) {
  draggableItems[i].draggable = true;
  draggableItems[i].addEventListener('dragstart', handleDragStart, false);
  draggableItems[i].addEventListener('dragover', handleDragOver, false);
  draggableItems[i].addEventListener('drop', handleDrop, false);
}

function handleDragStart(e) {
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', null);
  draggedItem = this;
  this.style.opacity = '0.4';
}

function handleDragOver(e) {
  if (e.preventDefault) {
    e.preventDefault();
  }
  e.dataTransfer.dropEffect = 'move';
  return false;
}

function handleDrop(e) {
  if (e.stopPropagation) {
    e.stopPropagation();
  }
  if (draggedItem !== this) {
    var tempText = this.innerHTML;
    var tempChecked = this.classList.contains('checked');
    
    this.innerHTML = draggedItem.innerHTML;
    this.classList.toggle('checked', draggedItem.classList.contains('checked'));

    draggedItem.innerHTML = tempText;
    draggedItem.classList.toggle('checked', tempChecked);
  }
  this.style.opacity = '1';
  return false;
}