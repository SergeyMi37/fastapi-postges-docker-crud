const API_BASE = 'http://localhost:8000';

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');

    tabs.forEach(tab => tab.classList.remove('active'));
    buttons.forEach(button => button.classList.remove('active'));

    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');

    if (tabName === 'todos') {
        loadTodos();
    } else {
        loadTasks();
    }
}

async function loadTodos() {
    try {
        const response = await fetch(`${API_BASE}/todos`);
        const todos = await response.json();
        displayTodos(todos);
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function displayTodos(todos) {
    const todosList = document.getElementById('todos-list');
    todosList.innerHTML = '';

    todos.forEach(todo => {
        const todoDiv = document.createElement('div');
        todoDiv.className = 'item';
        todoDiv.innerHTML = `
            <h3>${todo.title}</h3>
            <p>${todo.description}</p>
            <button onclick="editTodo(${todo.id})">Edit</button>
            <button onclick="deleteTodo(${todo.id})">Delete</button>
        `;
        todosList.appendChild(todoDiv);
    });
}

function displayTasks(tasks) {
    const tasksList = document.getElementById('tasks-list');
    tasksList.innerHTML = '';

    tasks.forEach(task => {
        const taskDiv = document.createElement('div');
        taskDiv.className = 'item';
        taskDiv.innerHTML = `
            <p>${task.task}</p>
            <button onclick="editTask(${task.id})">Edit</button>
            <button onclick="deleteTask(${task.id})">Delete</button>
        `;
        tasksList.appendChild(taskDiv);
    });
}

document.getElementById('todo-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('todo-title').value;
    const description = document.getElementById('todo-description').value;

    try {
        const response = await fetch(`${API_BASE}/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description }),
        });

        if (response.ok) {
            document.getElementById('todo-form').reset();
            loadTodos();
        }
    } catch (error) {
        console.error('Error creating todo:', error);
    }
});

document.getElementById('task-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const task = document.getElementById('task-task').value;

    try {
        const response = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task }),
        });

        if (response.ok) {
            document.getElementById('task-form').reset();
            loadTasks();
        }
    } catch (error) {
        console.error('Error creating task:', error);
    }
});

async function deleteTodo(id) {
    try {
        const response = await fetch(`${API_BASE}/todo/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            loadTodos();
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

async function deleteTask(id) {
    try {
        const response = await fetch(`${API_BASE}/task/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

function editTodo(id) {
    const newTitle = prompt('Enter new title:');
    const newDescription = prompt('Enter new description:');

    if (newTitle && newDescription) {
        updateTodo(id, newTitle, newDescription);
    }
}

function editTask(id) {
    const newTask = prompt('Enter new task:');

    if (newTask) {
        updateTask(id, newTask);
    }
}

async function updateTodo(id, title, description) {
    try {
        const response = await fetch(`${API_BASE}/todo/${id}?title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}`, {
            method: 'PUT',
        });

        if (response.ok) {
            loadTodos();
        }
    } catch (error) {
        console.error('Error updating todo:', error);
    }
}

async function updateTask(id, task) {
    try {
        const response = await fetch(`${API_BASE}/task/${id}?task=${encodeURIComponent(task)}`, {
            method: 'PUT',
        });

        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
});