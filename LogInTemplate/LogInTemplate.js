//This function outputs a message a the top of the form and adds a success or error class to the message element
//formElement represents which form, account creation of login, is being affected
//type is either success or error, depending if the user inputted what the programmer intended
//message is the text to be output to the user within the message element text box in the HTML
function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form_message");

    messageElement.textContent = message;
    messageElement.classList.remove("form_message_success", "form_message_error");
    messageElement.classList.add(`form_message_${type}`);
}



document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login"); //creates variable for the entire log in form
    const createAccountForm = document.querySelector("#createAccount"); //creates variable for the entire account creating form

    //Shows user the Create Account form
    document.querySelector("#linkCreateAccount").addEventListener("click", e => {
        e.preventDefault(); //prevents the link from trying to connect to another webpage, the default behavior
        loginForm.classList.add("form--hidden");
        createAccountForm.classList.remove("form--hidden"); 
    });

    //Shows user the Login form
    document.querySelector("#linkLogin").addEventListener("click", e => {
        e.preventDefault(); //prevents the link from trying to connect to another webpage, the default behavior
        loginForm.classList.remove("form--hidden");
        createAccountForm.classList.add("form--hidden");
    });

    //Function to determine if the input in password and confirm password match
    function samePassword() {
        let AccountPassword = document.getElementById("createAccountPassword");
        let AccountConfirmPassword = document.getElementById("createAccountConfirmPassword");
    
        //Outputs an error message if the passwords do not match
        if (AccountPassword.value != AccountConfirmPassword.value) {
            setFormMessage(createAccountForm, "error", "Passwords do not match");
        }
    }

    loginForm.addEventListener("submit", e => {
        e.preventDefault();

        // FIX ME: Perform your AJAX/Fetch login

        setFormMessage(loginForm, "error", "Invalid username/password combination");
    });
    createAccountForm.addEventListener("submit", e => {
        e.preventDefault();
        samePassword(); //Checks if passwords match when form is submitted
    });
});