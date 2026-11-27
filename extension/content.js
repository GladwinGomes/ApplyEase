function setNativeValue(element, value) {
  const prototype =
    element instanceof HTMLTextAreaElement
      ? HTMLTextAreaElement.prototype
      : HTMLInputElement.prototype;

  const descriptor = Object.getOwnPropertyDescriptor(prototype, "value");
  if (descriptor && descriptor.set) {
    descriptor.set.call(element, value);
  } else {
    element.value = value;
  }

  element.dispatchEvent(new Event("input", { bubbles: true }));
  element.dispatchEvent(new Event("change", { bubbles: true }));
}

function scanAndFillForm(profile) {
  const flatData = flattenProfileData(profile);
  const fields = document.querySelectorAll("input, textarea");
  let filledCount = 0;

  fields.forEach((el) => {
    const type = (el.type || "").toLowerCase();
    if (["hidden", "submit", "button", "reset", "file", "checkbox", "radio"].includes(type)) {
      return;
    }
    if (el.disabled || el.readOnly) {
      return;
    }

    const matchedKey = matchFieldKey(el);
    if (matchedKey && flatData[matchedKey]) {
      setNativeValue(el, flatData[matchedKey]);
      filledCount += 1;
    }
  });

  return filledCount;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "FILL_FORM") {
    try {
      const filledCount = scanAndFillForm(message.profile || {});
      sendResponse({ ok: true, filledCount });
    } catch (err) {
      sendResponse({ ok: false, error: err.message || "Error filling form" });
    }
    return true;
  }
});
