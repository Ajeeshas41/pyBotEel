function ShowToast(message, tags) {
    var toast = document.getElementById('liveToast')
    var toastBody = document.getElementById('toast-body')

    toast.className += " " + tags
    toastBody.innerHTML = message

    var toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast)
    toastBootstrap.show()
}

function createToast(message) {
    // Clone the template
    const element = htmx.find("[data-toast-template]").cloneNode(true)
  
    // Remove the data-toast-template attribute
    delete element.dataset.toastTemplate
  
    // Set the CSS class
    element.className += " " + message.tags
  
    // Set the text
    htmx.find(element, "[data-toast-body]").innerText = message.message
  
    // Add the new element to the container
    htmx.find("[data-toast-container]").appendChild(element)
  
    // Show the toast using Bootstrap's API
    const toast = new bootstrap.Toast(element, { delay: 5000 })
    toast.show()
}

htmx.on("messages", (event) => {
    event.detail.value.forEach(createToast)
})