function deleteForum(forumID) {
    fetch('/delete-forum', {
        method: 'POST',
        body: JSON.stringify({forumID: forumID}),
    }).then((_res) => {
        window.location.href = '/';
    });
}

function deleteTask(taskID) {
    fetch('/delete-task', {
        method: 'POST',
        body: JSON.stringify({taskID: taskID}),
    }).then((_res) => {
        window.location.href = '/task-page'; // Redirect to the task page after deletion
    });
}
