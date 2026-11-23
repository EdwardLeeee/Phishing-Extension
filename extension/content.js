(async () => {
  try {
    const currentUrl = window.location.href;

    const response = await fetch("http://localhost:5000/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: currentUrl })
    });

    if (!response.ok) {
      console.error("後端錯誤：", response.statusText);
      return;
    }

    const data = await response.json();
    const label = data.label;

    if (label === "phishing") {
      alert("⚠️ 警告：此網站可能為釣魚網站！");
    }
  } catch (err) {
    console.error("content.js 發生錯誤：", err);
  }
})();


