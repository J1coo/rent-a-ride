const addNewVehicle = (e) => {
    e.preventDefault()

    let formData = new FormData()

    let formInput = document.querySelectorAll('.formInput')
    formInput.forEach((ele) => {
        if (ele.type == 'file') {
            formData.append(ele.name, ele.files[0])
        }
        else {
            formData.append(ele.name, ele.value)
        }
    })

    fetch('/admin/addNewVehicle/', {
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
                alert('Vehicle Added')
                location.reload()
                break
            default:
                alert('Something went wrong please try again')
        }
    })
}