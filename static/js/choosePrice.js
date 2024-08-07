

const sendOTP = () => {
    let OTPnumber = document.getElementById('OTPnumber').value
    if (OTPnumber) {
        if (OTPnumber.length == 10) {
            let dataToSend = {
                'OTPnumber': OTPnumber
            }

            waitDialog.showModal()


            fetch('/sendOTP/', {
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
                        document.getElementById('otpModalButton').click()
                        waitDialog.close()

                    default:
                }
            })


        }
        else {
            alert('Please e nter a valid number')
        }
    }
    else {
        alert('Please enter your phone number')
    }
}



const submitOTP = (e) => {
    e.preventDefault()

    let dataToSend = {
        'OTP': document.getElementById('userOTP').value.trim(),
    }

    waitDialog.showModal()

    fetch('/verifyOTP/', {
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
                location.assign('/chooseCar/')
    waitDialog.close()
                break
            default:
                alert('Invalid OTP')
        }
    })

}