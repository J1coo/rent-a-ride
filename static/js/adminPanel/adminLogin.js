

const adminLogin=(e)=>{
    e.preventDefault()

    let dataToSend = {
        'adminEmail': document.getElementById('adminEmail').value.trim(),
        'adminPassword': document.getElementById('adminPassword').value.trim(),
    }

    // waitDialog.showModal()

    fetch('/admin/adminLoginFetch/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': document.getElementById('hiddenCsrfToken').value,
        },
        body: JSON.stringify(dataToSend)
    }).then(res => {
        return res.json();
    }).then(res => {
        switch (res.status) {
            case 'success':
                location.assign('/admin/')
                break
            case 'failed1':
                alert('Admin not exist. Please try with different email')
                break
            case 'failed2':
                alert('Wrong password.')
                break
            default:
                alert('Invalid OTP')
                break

        }
    })



}