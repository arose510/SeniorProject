function deleteForum(forumID) {
    fetch('/delete-forum', {
        method: 'POST',
        body: JSON.stringify({forumID: forumID}),
    }).then((_res) => {
        window.location.href = '/';
    });
}