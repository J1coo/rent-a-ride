const editUserProfile = (e) => {
    e.preventDefault()

    let formData = new FormData()
    let formInput = document.querySelectorAll('.formInput')
    formInput.forEach((ele) => {
        if (ele.value != '') {
            formData.append(ele.name, ele.value.trim())
        }
    })

    waitDialog.showModal()

    fetch('/updateUserProfile/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': document.getElementById('hiddenCsrfToken').value,
        },
        body: formData
    }).then(res => {
        return res.json();
    }).then(data => {
        switch (data.status) {
            case 'success':
                alert('Profile Updated successfully')
                location.reload()
                break
            default:
        }
    })
}