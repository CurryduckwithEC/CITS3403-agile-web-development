document.addEventListener('DOMContentLoaded', function() {
    const loginModule = {
        signInBtn: document.getElementById("loginSignIn"),
        signUpBtn: document.getElementById("loginSignUp"),
        container: document.querySelector(".login-container"),

        init: function() {
            console.log("Initializing login module");

            if (this.signInBtn && this.signUpBtn && this.container) {
                // Remove any existing event listeners to avoid conflicts
                this.removeEventListeners();

                // Add event listeners
                this.signInBtn.addEventListener("click", this.handleSignIn.bind(this));
                this.signUpBtn.addEventListener("click", this.handleSignUp.bind(this));
            } else {
                console.error("Sign In or Sign Up buttons or container not found!");
            }
        },

        handleSignIn: function() {
            console.log("Sign In button clicked");
            this.container.classList.remove("right-panel-active");
        },

        handleSignUp: function() {
            console.log("Sign Up button clicked");
            this.container.classList.add("right-panel-active");
        },

        removeEventListeners: function() {
            console.log("Removing existing event listeners");

            this.signInBtn.removeEventListener("click", this.handleSignIn);
            this.signUpBtn.removeEventListener("click", this.handleSignUp);
        }
    };

    loginModule.init();
});
