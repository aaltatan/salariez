export const addHitMessagesEventListeners = () => {
  const elements = document.querySelectorAll("[data-hit-messages]");
  if (elements.length) {
    elements.forEach((element) => {
      element.addEventListener("htmx:afterRequest", () => {
        const messagesElement = document.getElementById("messages");
        if (messagesElement) {
          messagesElement.click();
        }
      });
    });
  }
};
