
const addVehicleCategory=(e)=>{
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


    console.log('great')
    fetch('/admin/addNewCategory/', {
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
                alert('Vehicle category added')
                location.reload()
                break
            default:
        }
    })
}