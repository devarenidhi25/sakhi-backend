document.addEventListener("DOMContentLoaded", () => {
  // Initialize AOS
  if (typeof AOS !== "undefined") {
    AOS.init({
      duration: 800,
      once: true,
    });
  } else {
    console.warn(
      "AOS is not defined. Make sure it's properly imported or included."
    );
  }

  // Form elements
  const form = document.getElementById("complaintForm");
  const incidentTypeSelect = document.getElementById("incidentType");
  const otherIncidentContainer = document.getElementById(
    "otherIncidentContainer"
  );
  const steps = document.querySelectorAll(".form-step");
  const nextButtons = document.querySelectorAll(".next-step");
  const prevButtons = document.querySelectorAll(".prev-step");
  const progressBar = document.querySelector(".progress-bar");
  const stepIndicators = document.querySelectorAll(".step");

  // New sections for the updated flow
  const checkSeverity = document.getElementById("checkSeverity");
  const lowSeverityRedirect = document.getElementById("lowSeverityRedirect");
  const highSeverityRedirect = document.getElementById("highSeverityRedirect");
  const reportGeneration = document.getElementById("reportGeneration");
  const submissionSuccess = document.getElementById("submissionSuccess");
  const reportIdElement = document.getElementById("reportId");

  // Buttons for the new flow
  const chatbotRedirectBtn = document.getElementById("chatbotRedirectBtn");
  const generateReportBtn = document.getElementById("generateReportBtn");
  const downloadReportBtn = document.getElementById("downloadReportBtn");

  // Review elements
  const reviewLocation = document.getElementById("reviewLocation");
  const reviewIncidentType = document.getElementById("reviewIncidentType");
  const reviewOtherContainer = document.getElementById("reviewOtherContainer");
  const reviewOtherIncident = document.getElementById("reviewOtherIncident");
  const reviewDate = document.getElementById("reviewDate");
  const reviewEvidence = document.getElementById("reviewEvidence");

  // Show "Other" input field when "Other" is selected
  incidentTypeSelect.addEventListener("change", function () {
    if (this.value === "Other") {
      otherIncidentContainer.classList.add("show");
    } else {
      otherIncidentContainer.classList.remove("show");
    }
  });

  // Handle step navigation
  let currentStep = 0;

  function updateProgress() {
    // Update progress bar
    const progress = ((currentStep + 1) / steps.length) * 100;
    progressBar.style.width = `${progress}%`;
    progressBar.setAttribute("aria-valuenow", progress);

    // Update step indicators
    stepIndicators.forEach((step, index) => {
      if (index <= currentStep) {
        step.classList.add("active");
      } else {
        step.classList.remove("active");
      }
    });
  }

  function showStep(stepIndex) {
    steps.forEach((step, index) => {
      if (index === stepIndex) {
        step.classList.add("active");
      } else {
        step.classList.remove("active");
      }
    });

    currentStep = stepIndex;
    updateProgress();

    // Update review information when reaching step 3
    if (stepIndex === 2) {
      updateReviewInfo();
    }
  }

  function updateReviewInfo() {
    // Update the review section with current form values
    const location = document.getElementById("location").value;
    const incidentType = document.getElementById("incidentType").value;
    const otherIncident = document.getElementById("otherIncident").value;
    const incidentDate = document.getElementById("incidentDate").value;
    const evidenceInput = document.getElementById("evidence"); // Get file input

    reviewLocation.textContent = location;
    reviewIncidentType.textContent = incidentType;
    reviewDate.textContent = incidentDate;

    // Display the selected file name if a file is uploaded
    if (evidenceInput.files.length > 0) {
      reviewEvidence.textContent = evidenceInput.files[0].name;
    } else {
      reviewEvidence.textContent = "No file uploaded";
    }

    if (incidentType === "Other" && otherIncident) {
      reviewOtherContainer.style.display = "flex";
      reviewOtherIncident.textContent = otherIncident;
    } else {
      reviewOtherContainer.style.display = "none";
    }
  }

  // Next button event listeners
  nextButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // Simple validation for required fields in current step
      const currentStepElement = steps[currentStep];
      const requiredFields = currentStepElement.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value) {
          field.classList.add("is-invalid");
          isValid = false;
        } else {
          field.classList.remove("is-invalid");
        }
      });

      if (isValid) {
        showStep(currentStep + 1);
      }
    });
  });

  // Previous button event listeners
  prevButtons.forEach((button) => {
    button.addEventListener("click", () => {
      showStep(currentStep - 1);
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    form.style.display = "none";
    checkSeverity.style.display = "block";

    const incidentDetails = {
      incident_text: document.getElementById("incidentDetails").value,
      incident_id: `SK-${Date.now()}`,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/severity/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(incidentDetails),
      });

      if (!response.ok) throw new Error("Failed to classify severity");

      const data = await response.json();
      console.log("Severity Response:", data);

      checkSeverity.style.display = "none";

      if (data.severity === "LOW") {
        lowSeverityRedirect.style.display = "block";
        reportIdElement.textContent = data.incident_id;
      } else {
        highSeverityRedirect.style.display = "block";
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
      form.style.display = "block";
    }
  });

  // Chatbot redirect button
  chatbotRedirectBtn.addEventListener("click", () => {
    try {
      window.location.href = "/chatbot";
    } catch (error) {
      console.error("Redirection error:", error);
      alert("Unable to open chatbot. Please try again.");
    }
  });

  // Generate report button
  generateReportBtn.addEventListener("click", () => {
    highSeverityRedirect.style.display = "none";
    reportGeneration.style.display = "block";
  });

  // Download report button
  downloadReportBtn.addEventListener("click", () => {
    // In a real app, handle the report download
    reportGeneration.style.display = "none";
    submissionSuccess.style.display = "block";
  });

  // Add ripple effect to buttons
  const buttons = document.querySelectorAll(".btn");

  buttons.forEach((button) => {
    button.addEventListener("mousedown", (e) => {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const ripple = document.createElement("span");
      ripple.classList.add("ripple");
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;

      button.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  // Initialize
  showStep(0);

  // Make sure all additional sections are hidden at start
  checkSeverity.style.display = "none";
  lowSeverityRedirect.style.display = "none";
  highSeverityRedirect.style.display = "none";
  reportGeneration.style.display = "none";
  submissionSuccess.style.display = "none";

  // Hide review other container by default
  reviewOtherContainer.style.display = "none";
});
