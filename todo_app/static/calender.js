

function filterTasks() {
    const filterDate = document.getElementById("filterDate").value;
    const ongoingTodos = document.getElementById("ongoingTodos").getElementsByTagName("tr");
    const completedTodos = document.getElementById("completedTodos").getElementsByTagName("tr");

    // Hide all rows initially
    for (let i = 0; i < ongoingTodos.length; i++) {
        ongoingTodos[i].style.display = "none"; 
    }
    for (let i = 0; i < completedTodos.length; i++) {
        completedTodos[i].style.display = "none"; 
    }

    // Show only filtered rows based on the selected date
    for (const todo of ongoingTodos) {
        const deadline = todo.cells[2].innerText.split(' ')[0]; 
        if (filterDate && deadline === filterDate) {
            todo.style.display = ""; 
        }
    }
    for (const todo of completedTodos) {
        const deadline = todo.cells[2].innerText.split(' ')[0]; 
        if (filterDate && deadline === filterDate) {
            todo.style.display = ""; 
        }
    }
}