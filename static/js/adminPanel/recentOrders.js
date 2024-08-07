const assignDriver = (e) => {
    let orderId = e.currentTarget.getAttribute('data-orderId')
    let selectedDriver = document.getElementById('selectedDriver').value.trim()

    let dataToSend={
        'orderId':orderId,
        'selectedDriver':selectedDriver
    }
    fetch('/admin/assignDriver/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': document.getElementById('hiddenCsrfToken').value,
        },
        body: JSON.stringify(dataToSend)
    }).then(res => {
        return res.json();
    }).then(data => {
        switch (data.status) {
            case 'success':
                location.reload()
                break
            default:
        }
    })


}
