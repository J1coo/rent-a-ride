


const confirmBooking = (e) => {
    e.preventDefault()
    let status = window.confirm('Do you want to confirm with this car')
    console.log('Submitting...')
    if (status) {
        let carId = document.getElementById('vehicleId').value.trim()
        let bookingConfirmationCode = document.getElementById('modalconfirmationCode').value.trim()
        let dataToSend = {
            'vehicleId': carId,
            'bookingConfirmationCode': bookingConfirmationCode,
            'customerEmail': document.getElementById('confimationEmail').value.trim(),
            'bookingUserName': document.getElementById('orderUserName').value.trim(),
            'orderUserPhone': document.getElementById('orderUserPhone').value.trim(),
            'orderUserAddress': document.getElementById('orderUserAddress').value.trim(),
        }

        fetch('/orderConfirmation/', {
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
                    console.log('succes')
                    location.assign(`/thankyou/`)
                    break
                default:
                    alert('Something went wrong please try again')
            }
        })

    }
}

let emailConfirmationModal = document.getElementById('emailConfirmationModal')

const putDataintoModal = (e) => {
    document.getElementById('vehicleId').value = e.currentTarget.getAttribute('data-carId')
    emailConfirmationModal.showModal()
}


const clearModal = () => {
    emailConfirmationModal.close()
}