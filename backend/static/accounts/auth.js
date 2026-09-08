"use strict";
// Progressive enhancement. Every form also works without JavaScript.
document.querySelectorAll('input[type="password"]').forEach((input) => {
  const wrap = input.closest(".input-wrap");
  if (!wrap) return;
  wrap.classList.add("has-toggle");
  const button = document.createElement("button");
  button.type = "button";
  button.className = "password-toggle";
  button.textContent = "Pokaż";
  button.setAttribute("aria-controls", input.id);
  button.setAttribute("aria-pressed", "false");
  const fieldLabel = input.labels[0]?.textContent.trim() || "Hasło";
  button.setAttribute("aria-label", "Pokaż: " + fieldLabel);
  button.addEventListener("click", () => {
    const visible = input.type === "password";
    input.type = visible ? "text" : "password";
    button.textContent = visible ? "Ukryj" : "Pokaż";
    button.setAttribute("aria-pressed", String(visible));
    button.setAttribute("aria-label", (visible ? "Ukryj: " : "Pokaż: ") + fieldLabel);
  });
  wrap.append(button);
});
const firstError = document.querySelector('[aria-invalid="true"]');
if (firstError) firstError.focus();
