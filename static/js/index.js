

// =% SET BOOKING TYPE
const setBookingType = (e) => {
    let currentType = e.currentTarget.innerHTML.trim()
    document.getElementById('bookingType').value = currentType
    console.log(currentType)
}

// =% BOOK NOW 
const currentBooking = (e) => {
    e.preventDefault()
    let dataToSend = {}
    let formInput = document.querySelectorAll('.formData')
    formInput.forEach((ele) => {
        dataToSend[ele.name] = ele.value
    })
    dataToSend['pickUpLocation'] = JSON.parse(document.getElementById('locationSeggestionDiv').value.trim())
    dataToSend['destinationLocation'] = JSON.parse(document.getElementById('destinationAddressSelectTag').value.trim())

    waitDialog.showModal()

    fetch('/currentBooking/', {
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
                location.assign('/choosePrice/')
                waitDialog.close()
                break
            default:
        }
    })

}