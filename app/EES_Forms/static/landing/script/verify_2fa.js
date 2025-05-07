function resendCode() {
  resendBtn.disabled = true;
  resendBtn.innerText = "Sending...";

  fetch("/resend_2fa_code/")
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        countdown = 60;
        updateButton();
        alert("✅ Verification code sent!");
      } else {
        alert(`❌ ${data.error || "Unexpected error"}`);
        resendBtn.innerText = "Resend Code";
        resendBtn.disabled = false;
      }
    })
    .catch(error => {
      alert("⚠️ Error sending code.");
      console.error(error);
      resendBtn.innerText = "Resend Code";
      resendBtn.disabled = false;
    });
}
