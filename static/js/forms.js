/**
 * SANSKAR PUBLIC SCHOOL — Forms Handling & Asynchronous API Interactivity
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Admission Application Form Handler
  const admissionForm = document.getElementById('admission-application-form');
  if (admissionForm) {
    admissionForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const submitBtn = admissionForm.querySelector('button[type="submit"]');
      const originalBtnHtml = submitBtn.innerHTML;

      // Collect Form Data
      const formData = new FormData(admissionForm);
      const payload = Object.fromEntries(formData.entries());

      // Client-side quick validation
      if (!payload.student_name || !payload.dob || !payload.grade_applying || !payload.parent_name || !payload.phone || !payload.email || !payload.address) {
        window.showToast('Please complete all required fields (*)', 'error');
        return;
      }

      // Set Loading State
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting Application...';

      try {
        const response = await fetch('/api/admissions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok && result.success) {
          admissionForm.reset();
          showSuccessModal(result.application_number, result.student_name, result.grade_applying);
          window.showToast('Application registered successfully!', 'success');
        } else {
          window.showToast(result.message || 'Submission failed. Please check your details.', 'error');
        }
      } catch (err) {
        console.error(err);
        window.showToast('Network error. Please try submitting again.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
      }
    });
  }

  // 2. Contact Inquiries Form Handler
  const contactForm = document.getElementById('contact-inquiry-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalBtnHtml = submitBtn.innerHTML;

      const formData = new FormData(contactForm);
      const payload = Object.fromEntries(formData.entries());

      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending Inquiry...';

      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok && result.success) {
          contactForm.reset();
          window.showToast(result.message, 'success');
        } else {
          window.showToast(result.message || 'Could not send inquiry.', 'error');
        }
      } catch (err) {
        console.error(err);
        window.showToast('Connection error. Please try again.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
      }
    });
  }

  // Helper: Show Application Success Modal
  function showSuccessModal(appNumber, studentName, grade) {
    const modal = document.createElement('div');
    modal.className = 'admission-success-modal-overlay';
    modal.innerHTML = `
      <div class="admission-success-modal-card">
        <div class="modal-success-icon">
          <i class="fas fa-check-circle"></i>
        </div>
        <h3>Application Submitted Successfully!</h3>
        <p>Thank you for choosing Sanskar Public School. Your application has been logged into our admissions database.</p>
        
        <div class="app-number-box">
          <span class="label">Your Application Reference Number:</span>
          <span class="app-id" id="copy-app-num">${appNumber}</span>
          <button type="button" class="btn-copy-num" onclick="navigator.clipboard.writeText('${appNumber}'); window.showToast('Copied to clipboard!', 'info');">
            <i class="fas fa-copy"></i> Copy
          </button>
        </div>

        <div class="app-summary-details">
          <div><strong>Applicant:</strong> ${studentName}</div>
          <div><strong>Grade Applied:</strong> ${grade}</div>
          <div><strong>Status:</strong> <span class="badge-status-pending">Pending Review</span></div>
        </div>

        <p class="modal-notice-text">Please save your application reference number for tracking your admission status. Our admission counselor will contact you shortly.</p>

        <div class="modal-actions">
          <a href="/admission-status?app_num=${appNumber}" class="btn btn-primary">Track Application Status</a>
          <button type="button" class="btn btn-outline" id="btn-close-app-modal">Close</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const closeBtn = modal.querySelector('#btn-close-app-modal');
    closeBtn.addEventListener('click', () => modal.remove());
  }
});
