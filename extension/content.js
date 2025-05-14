(async () => {
  const url = window.location.href;
  try {
    const response = await fetch('http://localhost:8000/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    });
    const data = await response.json();
    if (data.warning) {
      alert(data.message);
    }
  } catch (err) {
    console.error('Error checking URL:', err);
  }
})();

