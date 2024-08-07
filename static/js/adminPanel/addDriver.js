const addNewDriver = (e) => {
    e.preventDefault()

    let formData = new FormData()
    let formInput=document.querySelectorAll('.formData')
    formInput.forEach((ele) => {
        if (ele.type == 'file') {
            formData.append(ele.name, ele.files[0])
        }
        else {
            formData.append(ele.name, ele.value)
        }
    })
    let selectedRadio = document.querySelector('input[name="gender"]:checked').value;
    formData.append('gender', selectedRadio)
    console.log('great')
    fetch('/admin/addNewDriver/', {
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
                alert('Driver added successfully')
                location.reload()
                break
            default:
        }
    })
}